import argparse
import subprocess
import wave
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Test Raspberry Pi USB microphone"
)
parser.add_argument("--device", default="plughw:3,0")
parser.add_argument("--duration", type=int, default=5)
parser.add_argument("--output", default="/tmp/mic_test.wav")
args = parser.parse_args()

if args.duration <= 0:
    parser.error("Duration must be positive")

output = Path(args.output)

print(f"Recording {args.duration} seconds...")
print(f"Microphone: {args.device}")

command = [
    "arecord",
    "-D", args.device,
    "-f", "S16_LE",
    "-r", "48000",
    "-c", "2",
    "-d", str(args.duration),
    str(output),
]

try:
    subprocess.run(
        command,
        check=True,
        timeout=args.duration + 10
    )

    with wave.open(str(output), "rb") as audio:
        frames = audio.getnframes()
        rate = audio.getframerate()
        duration = frames / rate

    if frames == 0:
        raise RuntimeError("Audio recording is empty")

    print("\nRecording successful!")
    print(f"File: {output}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Size: {output.stat().st_size} bytes")

except (subprocess.SubprocessError, OSError,
        RuntimeError, EOFError) as error:
    print(f"Recording failed: {error}")
    raise SystemExit(1)
