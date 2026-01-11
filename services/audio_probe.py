import subprocess
import json
from pathlib import Path

from core.models import AudioTrack


def probe_audio(track: AudioTrack) -> None:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=bit_rate,channels",
        "-show_entries", "format=duration",
        "-of", "json",
        str(track.path)
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        return

    data = json.loads(result.stdout)

    track.duration = float(data["format"]["duration"])
    track.bitrate = int(data["streams"][0]["bit_rate"]) // 1000
    track.channels = int(data["streams"][0]["channels"])
    track.audio_format = track.path.suffix.lstrip(".").upper()
