#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Starting autonomous biped ROS 2 sensors..."

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
