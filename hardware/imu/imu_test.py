import time
import math
import board
import adafruit_bno055

sensor = adafruit_bno055.BNO055_I2C(
    board.I2C(), address=0x28
)

def valid_quaternion(q):
    if q is None or len(q) != 4:
        return False
    if not all(math.isfinite(v) for v in q):
        return False
    return 0.95 <= sum(v * v for v in q) <= 1.05

print("BNO055 connected!")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        try:
            accel = sensor.acceleration
            gyro = sensor.gyro
            euler = sensor.euler
            quat = sensor.quaternion
            calib = sensor.calibration_status

            if valid_quaternion(quat):
                print("Acceleration (m/s²):", accel)
                print("Gyroscope (rad/s):", gyro)
                print("Orientation (degrees):", euler)
                print("Quaternion:", quat)
            else:
                print("WARNING: Invalid quaternion skipped")

            print("Calibration (sys, gyro, accel, mag):", calib)
            print("-" * 40)

        except (OSError, RuntimeError, ValueError) as e:
            print("Sensor reading error:", e)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nIMU test stopped cleanly.")
