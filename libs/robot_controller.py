"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    def __init__(self):
        # Construct the robot
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.btn = ev3.Button()
        self.Leds = ev3.Leds
        self.running = True

        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        assert self.left_motor.connected
        assert self.right_motor.connected

    def drive_inches(self, inches_target, speed_deg_per_second):
        # Make the robot to go to certain position with certain speed
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = inches_target * degrees_per_inch
        self.left_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=speed_deg_per_second)
        self.right_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=speed_deg_per_second)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        # Make the robot to turn certain degrees with certain speed
        self.right_motor.run_to_rel_pos(position_sp=degrees_to_turn * 5, speed_sp=turn_speed_sp)
        self.left_motor.run_to_rel_pos(position_sp=-degrees_to_turn * 5, speed_sp=turn_speed_sp)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        # Moves the robot arm up to highest position, then back down to lowest position
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()
        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range * 360)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        self.arm_motor.position = 0

    def arm_up(self):
        # Moves the robot arm up to the highest position
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

    def arm_down(self):
        # Moves the robot arm down to the lowest position
        self.arm_motor.run_to_abs_pos(position_sp=0)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

    def shutdown(self):
        self.running = False
        self.left_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE
        self.right_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE
        self.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        self.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    # Drives forward
    def forward(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    # Drives backward
    def backward(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    # Turns left
    def left(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    # Turns right
    def right(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    # Stops the motors
    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
