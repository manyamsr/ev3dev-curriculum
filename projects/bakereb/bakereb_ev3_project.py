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


def title_screen():
    root = tkinter.Tk()
    root.title("Title Screen")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    main_photo = tkinter.PhotoImage(file='Terminator_logo.gif')

    frame_title_1 = ttk.Label(main_frame, image=main_photo)
    frame_title_1.grid(row=1, column=2)

    play_game = ttk.Button(main_frame, text="Begin")
    play_game.grid(row=2, column=2)

    info_button = ttk.Button(main_frame, text="Information")
    info_button.grid(row=3, column=2)
    info_button['command'] = lambda: info()

    quit_button = ttk.Button(main_frame, text='Quit')
    quit_button.grid(row=4, column=2)
    quit_button['command'] = lambda: quit_game(root)

    root.mainloop()


def quit_game(root):
    root.destroy()


def info():
    info_root = tkinter.Tk()
    info_root.title('Information')

    info_frame = ttk.Frame(info_root, padding=10)
    info_frame.grid()

    main_photo = tkinter.PhotoImage(file='Terminator_info_screen_picture.gif')

    frame_title_1 = ttk.Label(info_frame, image=main_photo)
    frame_title_1.grid(row=1, column=2)

    frame1 = ttk.Label(info_frame, text="The goal of this project was to design a human-robot interaction game in "
                                        "which the human attempts to beat the robot at doing some task.")
    frame1.grid(row=1, column=1)

    frame2 = ttk.Label(info_frame, text="The human will use the GUI and/or physical interaction input commands to "
                                        "the robot and the robot will respond in a unique way.")
    frame2.grid(row=2, column=1)

    frame3 = ttk.Label(info_frame, text="The theme is Terminator. The robot (i.e. the terminator) is trying to capture "
                                        "John Connor (i.e. the Beacon), and your job is to try and prevent this ")
    frame3.grid(row=3, column=1)

    frame4 = ttk.Label(info_frame, text="from happening by hacking into the Terminator's mainframe and drive it away "
                                        "using keyboard inputs.")
    frame4.grid(row=5, column=1)

    frame5 = ttk.Label(info_frame, text="Once hacked, you will have a limited amount of time to try and drive the "
                                        "robot to cross a line of a certain color, which will activate the EMP and "
                                        "destroy ")
    frame5.grid(row=7, column=1)

    frame6 = ttk.Label(info_frame, text="the Terminator. However, if you fail, then the Terminator will capture "
                                        "John Connor and you will lose.")
    frame6.grid(row=8, column=1)

    frame7 = ttk.Label(info_frame,text="This creates alternate endings depending on the player's ability to 'hack' "
                                       "into the robot")
    frame7.grid(row=9, column=1)

    frame8 = ttk.Label(info_frame, text=" ")
    frame8.grid(row=3, column=1)

    frame9 = ttk.Label(info_frame, text=" ")
    frame9.grid(row=6, column=1)

    back_button = ttk.Button(info_frame, text='Back')
    back_button.grid(row=0, column=0)
    back_button['command'] = lambda: close_window(info_root)

    info_root.mainloop()


def close_window(info_frame):
    info_frame.destroy()


title_screen()