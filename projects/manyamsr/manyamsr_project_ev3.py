#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import mqtt_remote_method_calls as com
import math
import time
import robot_controller as robo
touch_sensor = ev3.TouchSensor()


def main():
    ev3.Sound.speak("This is a space mission").wait()
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()
    ev3.Sound.speak("Mission Successful")


main()
