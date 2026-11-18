# Autonomous Biped Robot — ROS 2

ROS 2 Jazzy running in Docker on Raspberry Pi 4.

## Working sensors

| Sensor | Topic | Message |
|--------|-------|---------|
| BNO055 IMU | /imu/data | sensor_msgs/msg/Imu |
| USB microphone | /audio/raw | audio_common_msgs/msg/AudioDataStamped |

## Hardware interfaces

- BNO055: /dev/i2c-1, address 0x28
- USB microphone: /dev/snd
- Camera: pending
- LiDAR: pending

## Microphone format

- 16 kHz
- Mono
- Signed 16-bit PCM, little-endian
- 100 ms chunks (3200 bytes)
- 10 Hz nominal publication rate

Audio encoding is a topic convention; the message
does not include format metadata.

## Build Docker image

From the repository root:

    sudo docker build -t biped-ros2:jazzy -f ros2_ws/Dockerfile .

## Build ROS 2 package

    sudo docker run --rm \
      --user "$(id -u):$(id -g)" \
      -e HOME=/tmp \
      -v "$PWD/ros2_ws:/workspace" \
      -w /workspace \
      biped-ros2:jazzy \
      bash -c 'source /opt/ros/jazzy/setup.bash && /opt/robot-venv/bin/python -m colcon build --packages-select biped_sensors --symlink-install --executor sequential'

## Launch sensors

    sudo docker run --rm -it \
      --network host \
      --ipc host \
      --device /dev/i2c-1:/dev/i2c-1 \
      --device /dev/snd:/dev/snd \
      -e ROS_DOMAIN_ID=0 \
      -v "$PWD/ros2_ws:/workspace" \
      -w /workspace \
      biped-ros2:jazzy \
      bash -lc 'source /opt/ros/jazzy/setup.bash && source /workspace/install/setup.bash && ros2 launch biped_sensors sensors.launch.py'

## Current limitations

- IMU fused orientation requires further calibration.
- IMU covariance and robot frame alignment are not validated.
- Microphone ALSA card number may change after reboot.
- Camera and LiDAR integration are pending.
