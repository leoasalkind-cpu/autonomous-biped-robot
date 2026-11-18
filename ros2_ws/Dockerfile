FROM ros:jazzy-ros-base

# Install Python virtual environment support
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-venv alsa-utils ros-jazzy-audio-common-msgs && \
    rm -rf /var/lib/apt/lists/*

# Install BNO055 libraries without modifying ROS Python packages
RUN python3 -m venv --system-site-packages /opt/robot-venv && \
    /opt/robot-venv/bin/pip install --no-cache-dir \
    adafruit-circuitpython-bno055 \
    adafruit-extended-bus

ENV PATH="/opt/robot-venv/bin:${PATH}"
