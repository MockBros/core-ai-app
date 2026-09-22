"""VieNeu-TTS v3 Turbo adapter for the LiveKit audio path.

VieNeu is OpenAI-compatible, but its resampling contract is not part of the
OpenAI plugin request.  The adapter keeps the LiveKit ``TTS`` lifecycle and
sentence-at-a-time ``StreamAdapter`` integration while adding VieNeu's explicit
``sample_rate=24000`` request field and raw PCM response checks.
"""

from __future__ import annotations

from typing import Any

import httpx
import openai
from livekit.agents import APIConnectOptions, tts
from livekit.agents.types import DEFAULT_API_CONNECT_OPTIONS
from livekit.agents.utils import shortuuid

VIENEU_SAMPLE_RATE = 24000
VIENEU_NUM_CHANNELS = 1
VIENEU_RESPONSE_FORMAT = "pcm"
VIENEU_STREAM_FORMAT = "audio"


class VieNeuTTS(tts.TTS):
    """Non-streaming LiveKit TTS backed by VieNeu's streaming HTTP response."""

    def __init__(
        self,
        *,
        base_url: str,
        model: str = "vieneu-v3-turbo",
        voice: str = "Mai Anh",
        response_format: str = VIENEU_RESPONSE_FORMAT,
        sample_rate: int = VIENEU_SAMPLE_RATE,
        api_key: str = "local",
        client: openai.AsyncClient | None = None,
    ) -> None:
        base_url = (base_url or "").strip().rstrip("/")
        if not base_url:
            raise ValueError("VIENEU_BASE_URL is required when TTS_PROVIDER=vieneu")
        if not model.strip():
            raise ValueError("VIENEU_MODEL must not be blank")
        if not voice.strip():
            raise ValueError("VIENEU_VOICE is required when TTS_PROVIDER=vieneu")
        if response_format.lower() != VIENEU_RESPONSE_FORMAT:
            raise ValueError("VIENEU_RESPONSE_FORMAT must be 'pcm' for the LiveKit raw-audio path")
        if sample_rate != VIENEU_SAMPLE_RATE:
            raise ValueError("VIENEU_SAMPLE_RATE must be 24000 for the LiveKit raw-audio path")
        if not api_key:
            raise ValueError(
                "VIENEU_API_KEY or LOCAL_API_KEY must be non-empty for the OpenAI client"
            )

        super().__init__(
            capabilities=tts.TTSCapabilities(streaming=False),
            sample_rate=VIENEU_SAMPLE_RATE,
            num_channels=VIENEU_NUM_CHANNELS,
        )
        self.vieneu_base_url = base_url
        self.vieneu_model = model.strip()
        self.vieneu_voice = voice.strip()
        self.vieneu_response_format = response_format.lower()
        self.vieneu_sample_rate = sample_rate
        self._owns_client = client is None
        self._client = client or openai.AsyncClient(
            max_retries=0,
            api_key=api_key,
            base_url=base_url,
            http_client=httpx.AsyncClient(
                timeout=httpx.Timeout(connect=15.0, read=30.0, write=30.0, pool=30.0),
                follow_redirects=True,
                limits=httpx.Limits(
                    max_connections=50,
                    max_keepalive_connections=50,
                    keepalive_expiry=120,
                ),
            ),
        )

    @property
    def model(self) -> str:
        return self.vieneu_model

    @property
    def provider(self) -> str:
        return "vieneu"

    def _request_kwargs(self, text: str) -> dict[str, Any]:
        """Return the exact VieNeu speech request body and transport options."""
        return {
            "input": text,
            "model": self.vieneu_model,
            "voice": self.vieneu_voice,
            "response_format": self.vieneu_response_format,
            "stream_format": VIENEU_STREAM_FORMAT,
            # VieNeu's OpenAI-compatible extension.  This is the resampling
            # mechanism that makes the returned s16le bytes match LiveKit's
            # 24 kHz emitter metadata.
            "extra_body": {"sample_rate": self.vieneu_sample_rate},
        }

    def synthesize(
        self,
        text: str,
        *,
        conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS,
    ) -> tts.ChunkedStream:
        return VieNeuChunkedStream(tts=self, input_text=text, conn_options=conn_options)

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.close()


class VieNeuChunkedStream(tts.ChunkedStream):
    """Read VieNeu's raw PCM body without using the OpenAI plugin's model switch."""

    async def _run(self, output_emitter: tts.AudioEmitter) -> None:
        request_kwargs = self._tts._request_kwargs(self._input_text)
        request_kwargs["timeout"] = httpx.Timeout(
            30.0,
            connect=self._conn_options.timeout,
        )
        response_stream = self._tts._client.audio.speech.with_streaming_response.create(
            **request_kwargs
        )

        async with response_stream as response:
            media_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
            if media_type != "audio/pcm":
                raise ValueError(
                    "VieNeu returned {!r}; expected audio/pcm for VIENEU_RESPONSE_FORMAT=pcm".format(
                        media_type or "<missing content type>"
                    )
                )

            response_rate = response.headers.get("x-sample-rate")
            if response_rate and response_rate != str(self._tts.vieneu_sample_rate):
                raise ValueError(
                    f"VieNeu returned X-Sample-Rate={response_rate!r}; "
                    f"expected {self._tts.vieneu_sample_rate}"
                )

            output_emitter.initialize(
                request_id=getattr(response, "request_id", None) or shortuuid(),
                sample_rate=self._tts.sample_rate,
                num_channels=self._tts.num_channels,
                mime_type="audio/pcm",
            )

            total_bytes = 0
            async for chunk in response.iter_bytes():
                if chunk:
                    total_bytes += len(chunk)
                    output_emitter.push(chunk)

            # VieNeu promises signed 16-bit PCM.  An odd byte count would mean
            # the response cannot be decoded as complete PCM samples.
            if total_bytes % 2:
                raise ValueError("VieNeu returned an odd number of PCM bytes")

        output_emitter.flush()
