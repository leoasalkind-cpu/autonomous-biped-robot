import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

import adafruit_bno055
from adafruit_extended_bus import ExtendedI2C


def valid_vector(values, count):
    return (
        values is not None
        and len(values) == count
        and all(v is not None and math.isfinite(v) for v in values)
    )


class BNO055Node(Node):
    def __init__(self):
        super().__init__("bno055_node")

        self.sensor = adafruit_bno055.BNO055_I2C(
            ExtendedI2C(1), address=0x28
        )

        self.publisher = self.create_publisher(
            Imu, "/imu/data", 10
        )

        self.sample_count = 0
        self.timer = self.create_timer(0.1, self.publish_imu)

        self.get_logger().info("BNO055 ROS 2 node started at 10 Hz")

    def publish_imu(self):
        try:
            accel = self.sensor.acceleration
            gyro = self.sensor.gyro
            quat = self.sensor.quaternion
            calib = self.sensor.calibration_status
        except (OSError, RuntimeError, ValueError, TypeError) as exc:
            self.get_logger().warning(f"Sensor read failed: {exc}")
            return

        if not valid_vector(accel, 3) or not valid_vector(gyro, 3):
            self.get_logger().warning("Invalid IMU data; skipping sample")
            return

        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "imu_link"

        msg.linear_acceleration.x = accel[0]
        msg.linear_acceleration.y = accel[1]
        msg.linear_acceleration.z = accel[2]

        msg.angular_velocity.x = gyro[0]
        msg.angular_velocity.y = gyro[1]
        msg.angular_velocity.z = gyro[2]

        # Covariances left at zero: not yet characterized.
        # Only publish fused orientation when sufficiently calibrated.
        orientation_ok = False

        if valid_vector(quat, 4):
            norm = math.sqrt(sum(v * v for v in quat))

            if (
                0.975 <= norm <= 1.025
                and calib[0] >= 2
                and calib[1] >= 2
                and calib[2] >= 1
                and calib[3] >= 2
            ):
                w, x, y, z = (v / norm for v in quat)
                msg.orientation.w = w
                msg.orientation.x = x
                msg.orientation.y = y
                msg.orientation.z = z
                orientation_ok = True

        if not orientation_ok:
            msg.orientation.w = 1.0
            msg.orientation_covariance[0] = -1.0

        self.publisher.publish(msg)

        self.sample_count += 1
        if self.sample_count % 50 == 0:
            self.get_logger().info(
                f"Publishing /imu/data; calibration={calib}; "
                f"orientation_valid={orientation_ok}"
            )


def main(args=None):
    rclpy.init(args=args)
    node = BNO055Node()

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
