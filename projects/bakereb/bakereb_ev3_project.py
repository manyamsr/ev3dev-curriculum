"""
    The goal of this project will be to design a human-robot interaction game in which the human attempts to beat the
    robot at doing some task. The human will use the GUI and/or physical interaction input commands to the robot and
    the robot will respond in a unique way.

    The theme is Terminator. The robot (i.e. the terminator) is trying to capture John Connor (i.e. the Beacon), and
    your job is to try and prevent this from happening by hacking into the Terminator's mainframe and drive it away
    using keyboard inputs. Once hacked, you will have a limited amount of time to try and drive the robot to cross a
    line of a certain color, which will activate the EMP and destroy the Terminator. However, if you fail, then the
    Terminator will capture John Connor and you will lose. This creates alternate endings depending on the player's
    ability to "hack" into the robot.

Author: Ethan Baker
"""
import ev3dev.ev3 as ev3
import time
import math
import tkinter
from tkinter import ttk
import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    root = tkinter.Tk()
    root.title("Title Screen")
    root.geometry("1280x720")

    main_frame = ttk.Frame(root, padding=200)
    main_frame.grid()

    main_photo = tkinter.PhotoImage(file='Terminator_logo.gif')

    frame_title_1 = ttk.Label(main_frame, image=main_photo)
    frame_title_1.image = main_photo
    frame_title_1.grid()

    

    root.mainloop()


main()