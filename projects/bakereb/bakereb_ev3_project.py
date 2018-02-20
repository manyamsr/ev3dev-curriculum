import ev3dev.ev3 as ev3
import mqtt_remote_method_calls as com
import math
import time
import robot_controller as robo

left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

touch_sensor = ev3.TouchSensor()


class MyDelegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()

    def arm_up(self):
        self.robot.arm_up()

    def arm_down(self):
        self.robot.arm_down()


def main():
    my_delegate = MyDelegate()
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    while not touch_sensor.is_pressed:
        robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.





# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
