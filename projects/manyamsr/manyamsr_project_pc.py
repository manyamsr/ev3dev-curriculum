#!/usr/bin/env python3

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import math
import time
import ev3dev.ev3 as ev3
import robot_controller as robo
variable1 = 0
variable2 = 0
variable3 = 0


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, button_name):
        print("Received: " + button_name)
        message_to_display = "{} was pressed.".format(button_name)
        self.display_label.configure(text=message_to_display)


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Space Ship Controls")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    orbit_earth_button = ttk.Button(main_frame, text="Orbit Earth")
    orbit_earth_button.grid(row=2, column=1)
    orbit_earth_button['command'] = lambda: send_orbit_earth(mqtt_client, ev3.ColorSensor.COLOR_BLUE,
                                                             ev3.ColorSensor.COLOR_BLACK)
    root.bind('<o>', lambda event: send_orbit_earth(mqtt_client, ev3.ColorSensor.COLOR_BLUE,
                                                    ev3.ColorSensor.COLOR_BLACK))

    travel_button = ttk.Button(main_frame, text="Travel to Mars")
    travel_button.grid(row=3, column=0)
    travel_button['command'] = lambda: send_travel(mqtt_client, ev3.ColorSensor.COLOR_BLACK,
                                                   ev3.ColorSensor.COLOR_RED)
    root.bind('<t>', lambda event: send_travel(mqtt_client, ev3.ColorSensor.COLOR_BLACK,
                                               ev3.ColorSensor.COLOR_RED))

    find_probe_button = ttk.Button(main_frame, text="Find Probe")
    find_probe_button.grid(row=5, column=0)
    find_probe_button['command'] = lambda: send_find_probe(mqtt_client)
    root.bind('<f>', lambda event: send_find_probe(mqtt_client))

    pickup_probe_button = ttk.Button(main_frame, text="Pickup Probe")
    pickup_probe_button.grid(row=3, column=3)
    pickup_probe_button['command'] = lambda: send_pickup_probe(mqtt_client)
    root.bind('<p>', lambda event: send_pickup_probe(mqtt_client))

    return_button = ttk.Radiobutton(main_frame, text="Return to Mars", variable=variable3, value=5)
    return_button.grid(row=6, column=0)
    return_button['command'] = lambda: send_return(mqtt_client, ev3.ColorSensor.COLOR_RED, 200, 100)
    root.bind('<r>', lambda event: send_return(mqtt_client, ev3.ColorSensor.COLOR_RED, 200, 100))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))
    root.bind('<q>', lambda event: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))
    root.bind('<e>', lambda event: quit_program(mqtt_client, True))

    root.mainloop()


def send_orbit_earth(mqtt_client, start_color, end_color):
    print("Orbiting the Earth")
    mqtt_client.send_message("speak", ["Now Orbiting the Earth"])
    mqtt_client.send_message("line_follow", [start_color, end_color])


def send_travel(mqtt_client, start_color, end_color):
    print("Traveling to Mars")
    mqtt_client.send_message("speak", ["Now traveling to Mars"])
    mqtt_client.send_message("line_follow", [start_color, end_color])


def send_find_probe(mqtt_client):
    print("Locating Probe")
    mqtt_client.send_message("speak", ["Now Locating the probe"])
    mqtt_client.send_message("seek_beacon")


def send_pickup_probe(mqtt_client):
    print("Picking up the Probe")
    mqtt_client.send_message("speak", ["Picking up the probe"])
    mqtt_client.send_message("arm_up")


def send_return(mqtt_client, color_to_seek, degrees, turn_speed):
    print("Returning to Mars")
    mqtt_client.send_message("speak", ["Now Returning to Mars"])
    mqtt_client.send_message("turn_degrees", [degrees, turn_speed])
    mqtt_client.send_message("drive_to_color", [color_to_seek])
    mqtt_client.send_message("arm_down")
    print("Mission Successful")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
