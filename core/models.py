from pathlib import Path
from dataclasses import dataclass


@dataclass
class AudioTrack:
    path: Path
    number: str
    title: str
    duration: float | None = None
    bitrate: int | None = None
    audio_format: str | None = None
    channels: int | None = None
