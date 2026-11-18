# BNO055 IMU

## Hardware
- Raspberry Pi 4
- BNO055 9-DoF orientation sensor
- I2C address: 0x28

## Wiring

| BNO055 | Raspberry Pi physical pin |
|--------|---------------------------|
| VIN    | 1 (3.3V)                 |
| GND    | 6 (Ground)               |
| SDA    | 3 (GPIO2)                |
| SCL    | 5 (GPIO3)                |

## Setup

Enable I2C using `sudo raspi-config`.

Install dependencies in a Python virtual environment:

    pip install -r hardware/imu/requirements.txt

## Testing

From the repository root:

    python hardware/imu/imu_test.py

The script reports:
- Acceleration (m/s²)
- Angular velocity (rad/s)
- Euler orientation (degrees)
- Quaternion orientation
- Calibration status

Press Ctrl+C to stop.

## Current status

Hardware communication and motion readings verified.
Calibration has not yet consistently reached (3, 3, 3, 3).
Additional data validation is required before using the IMU
for robot balance control.

## Future integration

Publish validated BNO055 measurements through ROS 2
using sensor_msgs/msg/Imu.
