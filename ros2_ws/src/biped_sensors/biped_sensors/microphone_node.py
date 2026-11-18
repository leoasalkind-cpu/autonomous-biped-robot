import os
import subprocess

import rclpy
from rclpy.node import Node
from audio_common_msgs.msg import AudioDataStamped


class MicrophoneNode(Node):
    SAMPLE_RATE = 16000
    CHANNELS = 1
    BYTES_PER_SAMPLE = 2
    CHUNK_MS = 100
    CHUNK_BYTES = SAMPLE_RATE * CHANNELS * BYTES_PER_SAMPLE * CHUNK_MS // 1000

    def __init__(self):
        super().__init__("microphone_node")

        self.declare_parameter("device", "plughw:3,0")
        device = self.get_parameter("device").value

        self.publisher = self.create_publisher(
            AudioDataStamped, "/audio/raw", 10
        )

        self.process = subprocess.Popen(
            [
                "arecord",
                "-q",
                "-D", device,
                "-t", "raw",
                "-f", "S16_LE",
                "-r", str(self.SAMPLE_RATE),
                "-c", str(self.CHANNELS),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )

        os.set_blocking(self.process.stdout.fileno(), False)

        self.buffer = bytearray()
        self.message_count = 0

        self.timer = self.create_timer(0.02, self.publish_audio)

        self.get_logger().info(
            f"Microphone started: {device}, "
            "16 kHz mono, 100 ms chunks"
        )

    def publish_audio(self):
        try:
            while True:
                data = os.read(self.process.stdout.fileno(), 8192)
                if not data:
                    break
                self.buffer.extend(data)
        except BlockingIOError:
            pass
        except OSError as error:
            self.get_logger().error(f"Audio read error: {error}")
            self.timer.cancel()
            return

        while len(self.buffer) >= self.CHUNK_BYTES:
            chunk = bytes(self.buffer[:self.CHUNK_BYTES])
            del self.buffer[:self.CHUNK_BYTES]

            msg = AudioDataStamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = "microphone_link"
            msg.audio.data = list(chunk)

            self.publisher.publish(msg)
            self.message_count += 1

            if self.message_count % 50 == 0:
                self.get_logger().info(
                    f"Published {self.message_count} audio chunks"
                )

        if self.process.poll() is not None:
            error = self.process.stderr.read().decode(
                errors="replace"
            ).strip()
            self.get_logger().error(
                f"arecord stopped: {error or self.process.returncode}"
            )
            self.timer.cancel()

    def destroy_node(self):
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        self.process.stdout.close()
        self.process.stderr.close()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = MicrophoneNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
