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
import math
import mqtt_remote_method_calls as com


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    def __init__(self):
        # Constructs the robot
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.btn = ev3.Button()
        self.Leds = ev3.Leds
        self.running = True
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

        # Checks to make sure everything is connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.color_sensor.connected
        assert self.ir_sensor.connected
        assert self.pixy.connected

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
        self.arm_motor.run_forever(speed_sp=600)
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
        # Stops the robot, sets both Leds to green, prints and says Goodbye
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

    def forward(self, left_speed, right_speed):
        # Drives forward forever
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def backward(self, left_speed, right_speed):
        # Drives backward forever
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def left(self, left_speed, right_speed):
        # Spins the robot left
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def right(self, left_speed, right_speed):
        # Spins the robot right
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def stop(self):
        # Stops both motors
        self.left_motor.stop()
        self.right_motor.stop()

    def seek_beacon(self):
        """
        Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.

        """

        # Create a BeaconSeeker object on channel 1.

        forward_speed = 100
        turn_speed = 100
        beacon_seeker = ev3.BeaconSeeker(sensor=self.ir_sensor, channel=1)

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)

            # Use the beacon_seeker object to get the current heading and distance.
            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                while current_distance == -128:
                    self.left(turn_speed, turn_speed)
            else:
                # Implement the following strategy to find the beacon.
                # If the absolute value of the current_heading is less than 2, you are on the right heading.
                #     If the current_distance is 0 return from this function, you have found the beacon!  return True
                #     If the current_distance is greater than 0 drive straight forward (forward_speed, forward_speed)
                # If the absolute value of the current_heading is NOT less than 2 but IS less than 10, you need to spin
                #     If the current_heading is less than 0 turn left (-turn_speed, turn_speed)
                #     If the current_heading is greater than 0 turn right  (turn_speed, -turn_speed)
                # If the absolute value of current_heading is greater than 10, then stop and print Heading too far off
                #
                # It is recommended that you always print
                # something each pass through the loop to help you debug what is going on.  Examples:
                #    print("On the right heading. Distance: ", current_distance)
                #    print("Adjusting heading: ", current_heading)
                #    print("Heading is too far off to fix: ", current_heading)

                # Here is some code to help get you started
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if current_distance == 0:
                        time.sleep(1)
                        self.stop()
                        return True
                    else:
                        self.forward(forward_speed, forward_speed)
                elif 2 <= math.fabs(current_heading) <= 10:
                    print("Adjusting heading: ", current_heading)
                    if current_heading < 0:
                        self.left(turn_speed, turn_speed)
                    elif current_heading > 0:
                        self.right(turn_speed, turn_speed)
                else:
                    print("Heading too far off to fix: ", current_heading)
                    while math.fabs(current_heading) > 10:
                        self.right(turn_speed, turn_speed)
                        print("current heading = ", current_heading)
            time.sleep(0.02)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False

    def auto_drive(self):
        mqtt_client = com.MqttClient(self)
        mqtt_client.connect_to_pc()
        while not self.touch_sensor.is_pressed:
            self.forward(200, 200)
            time.sleep(0.1)

            if self.color_sensor.color == 6:
                self.turn_degrees(180, turn_speed_sp= 200)
                time.sleep(0.5)
                ev3.Sound.speak('object found')
                self.forward(200, 200)
                time.sleep(0.1)
                break
            if self.color_sensor.color == 3:
                self.turn_degrees(90, turn_speed_sp= 200)
                time.sleep(0.5)
                ev3.Sound.speak('Turning left')
                self.forward(200, 200)
                time.sleep(0.1)
                break
        self.stop()
        ev3.Sound.speak('Goodbye')
        self.stop()

    def line_follow_left(self, start_color, end_color):
        print("we are here", start_color, end_color)
        while not self.touch_sensor.is_pressed:
            self.left_motor.run_forever(speed_sp=300)
            self.right_motor.run_forever(speed_sp=300)
            time.sleep(0.01)
            while True:
                c = self.color_sensor.color
                print(c)
                if c != start_color:
                    break
                time.sleep(0.01)
            self.left(300, 300)
            time.sleep(0.01)
            c = self.color_sensor.color
            print("after turning", c)
            if c == end_color:
                break
        self.stop()

    def line_follow_right(self, start_color, end_color):
        print("we are here", start_color, end_color)
        while not self.touch_sensor.is_pressed:
            self.left_motor.run_forever(speed_sp=300)
            self.right_motor.run_forever(speed_sp=300)
            time.sleep(0.01)
            while True:
                c = self.color_sensor.color
                print(c)
                if c != start_color:
                    break
                time.sleep(0.01)
            self.right(300, 300)
            time.sleep(0.01)
            c = self.color_sensor.color
            print("after turning", c)
            if c == end_color:
                break
        self.stop()

    def drive_to_color(self, color_to_seek):
            self.left_motor.run_forever(speed_sp=300)
            self.right_motor.run_forever(speed_sp=300)
            while self.color_sensor.color is not color_to_seek:
                time.sleep(0.01)
            self.left_motor.stop()
            self.right_motor.stop()

    def speak(self, string_to_speak):
        ev3.Sound.speak(string_to_speak).wait()