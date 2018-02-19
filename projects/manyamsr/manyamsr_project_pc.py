#!/usr/bin/env python3

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import math
import time
import ev3dev.ev3 as ev3
import robot_controller as robo


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
    root.title("Space Ship")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    orbit_button = ttk.Button(main_frame, text="Orbit Earth")
    orbit_button.grid(row=2, column=1)
    orbit_button['command'] = lambda: send_orbit(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<o>', lambda event: send_forward(mqtt_client, left_speed_entry, right_speed_entry))

    travel_button = ttk.Button(main_frame, text="Travel to Mars")
    travel_button.grid(row=3, column=0)
    travel_button['command'] = lambda: send_left(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: send_left(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<s>', lambda event: send_stop(mqtt_client))

    up_button = ttk.Radiobutton(main_frame, text="Find Probe", variable=variable3, value=4)
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Radiobutton(main_frame, text="Return to Mars", variable=variable3, value=5)
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))
    root.bind('<q>', lambda event: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))
    root.bind('<e>', lambda event: quit_program(mqtt_client, True))

    root.mainloop()


def f1(mqtt_client):
    mqtt_client.send_message('stop')


def send_orbit(mqtt_client, color):
    print("Orbiting the Earth")
    mqtt_client.send_message("line_follow", [2])


def send_backward(mqtt_client, left_speed_entry, right_speed_entry):
    print("backward")
    mqtt_client.send_message("backward", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("left")
    mqtt_client.send_message("left", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("right")
    mqtt_client.send_message("right", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def send_stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
