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
import random
import traceback

mqtt_client = com.MqttClient()
mqtt_client.connect_to_ev3()

root = tkinter.Tk()
root.title("Title Screen")
robot = robo.Snatch3r

touch_sensor = ev3.TouchSensor()

# left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
# right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
#
#
# assert left_motor.connected
# assert right_motor.connected


class GuessingNumber(object):
    def __init__(self):
        self.answer = str(random.randint(1, 3)) + str(random.randint(1, 3)) + str(random.randint(1, 3))
        self.input_number = None
        self.input_build = 0
        self.input_label = None
        self.state = False
        self.count_guess = 0

# Title Screen


def title_screen():
    root.title('Title Screen')
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    main_photo = tkinter.PhotoImage(file='Terminator_logo.gif')

    frame_title_1 = ttk.Label(main_frame, image=main_photo)
    frame_title_1.grid(row=1, column=2)

    play_game_button = ttk.Button(main_frame, text="Begin")
    play_game_button.grid(row=2, column=2)
    play_game_button['command'] = lambda: play_game(main_frame, root)

    info_button = ttk.Button(main_frame, text="Information")
    info_button.grid(row=3, column=2)
    info_button['command'] = lambda: info(main_frame, root)

    quit_button = ttk.Button(main_frame, text='Quit')
    quit_button.grid(row=4, column=2)
    quit_button['command'] = lambda: quit_game(root)

    root.mainloop()


# Quit game function
def quit_game(root):
    root.destroy()


# Information Screen
def info(main_frame, root):
    main_frame.destroy()
    main_frame = ttk.Frame(root, padding=10)
    root.title('Information')
    main_frame.grid()

    photo = tkinter.PhotoImage(file='Terminator_info_screen_picture.gif')
    frame_title_1 = ttk.Label(main_frame, image=photo)
    frame_title_1.grid(row=1, column=1)
    frame_title_1.image = photo

    frame1 = ttk.Label(main_frame, text="The goal of this project was to design a human-robot interaction game in "
                                        "which the human attempts to beat the robot at doing some task.")
    frame1.grid(row=2, column=1)

    frame2 = ttk.Label(main_frame, text="The human will use the GUI and/or physical interaction input commands to "
                                        "the robot and the robot will respond in a unique way.")
    frame2.grid(row=3, column=1)

    frame3 = ttk.Label(main_frame, text="The theme is Terminator. The robot (i.e. the terminator) is trying to capture "
                                        "John Connor (i.e. the Beacon), and your job is to try and prevent this ")
    frame3.grid(row=5, column=1)

    frame4 = ttk.Label(main_frame, text=" ")
    frame4.grid(row=4, column=1)

    frame5 = ttk.Label(main_frame, text="from happening by hacking into the Terminator's mainframe and drive it away "
                                        "using keyboard inputs.")
    frame5.grid(row=6, column=1)

    frame6 = ttk.Label(main_frame, text="Once hacked, you will have a limited amount of time to try and drive the "
                                        "robot to cross a line of a certain color, which will activate the EMP and "
                                        "destroy ")
    frame6.grid(row=8, column=1)

    frame7 = ttk.Label(main_frame, text=" ")
    frame7.grid(row=7, column=1)

    frame8 = ttk.Label(main_frame, text="the Terminator. However, if you fail, then the Terminator will capture "
                                        "John Connor and you will lose.")
    frame8.grid(row=9, column=1)

    frame9 = ttk.Label(main_frame,text="This creates alternate endings depending on the player's ability to 'hack' "
                                       "into the robot.")
    frame9.grid(row=10, column=1)

    back_button = ttk.Button(main_frame, text='Back')
    back_button.grid(row=0, column=0)
    back_button['command'] = lambda: back_to_main(main_frame)

    root.mainloop()


def close_window(window):
    window.destroy()


def back_to_main(frame):
    frame.destroy()
    title_screen()


def play_game(main_frame, root):
    root.title('Prepare yourself')
    main_frame.destroy()
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    frame1 = ttk.Label(main_frame, text="The Terminator has found you. Do not let him get to John Connor!")
    frame1.grid(row=0, column=1)

    frame2 = ttk.Label(main_frame, text=' ')
    frame2.grid(row=1, column=1)

    frame3 = ttk.Label(main_frame, text="The aim of the game is to attempt to hack into the Terminator and force it"
                                        "away from you.")
    frame3.grid(row=2, column=1)

    frame4 = ttk.Label(main_frame, text=' ')
    frame4.grid(row=3, column=1)

    frame5 = ttk.Label(main_frame, text="There will be a series of puzzles that you must solve in order to achieve a "
                                        "successful hack. Once you've hacked into the Terminator, use the arrow keys")
    frame5.grid(row=4, column=1)

    frame6 = ttk.Label(main_frame, text='to drive it away. Once it crosses the white piece of paper, the EMP will'
                                        ' activate and the Terminator will be destroyed.')
    frame6.grid(row=5, column=1)

    frame7 = ttk.Label(main_frame, text=' ')
    frame7.grid(row=6, column=1)

    frame8 = ttk.Label(main_frame, text='However, fail to solve the puzzles in time and the robot will capture John'
                                        ' and you will lose.')
    frame8.grid(row=7, column=1)

    frame9 = ttk.Label(main_frame, text=' ')
    frame9.grid(row=8, column=1)

    frame10 = ttk.Label(main_frame, text='Good Luck!')
    frame10.grid(row=9, column=1)

    back_button = ttk.Button(main_frame, text='Back')
    back_button.grid(row=0, column=0)
    back_button['command'] = lambda: back_to_main(main_frame)

    play_button = ttk.Button(main_frame, text='Play')
    play_button.grid(row=0, column=2)
    play_button['command'] = lambda: game(main_frame, root, robot)


def game(main_frame, root, robot):
    guess_num = GuessingNumber()
    root.title('Terminator Game')
    main_frame.destroy()
    main_frame = ttk.Frame(root, padding=50)
    main_frame.grid()
    root.geometry('720x200')
    state = guess_num.state

    # mqtt_client.send_message("seek_beacon")

    explain_frame = ttk.Label(main_frame, text='Enter the Code!')
    explain_frame.grid(row=0, column=0)

    space_frame_row_1 = ttk.Label(root, width=5)
    space_frame_row_1.grid(row=0, column=9)

    # space_frame_row_2 = ttk.Label(root, width=5)
    # space_frame_row_2.grid(row=0, column=1)

    input_button_1_1 = ttk.Button(root, text='1')
    input_button_1_1.grid(row=0, column=3)
    input_button_1_1['command'] = lambda: guessing_number(guess_num, 1)

    input_button_1_2 = ttk.Button(root, text='2')
    input_button_1_2.grid(row=0, column=4)
    input_button_1_2['command'] = lambda: guessing_number(guess_num, 2)

    input_button_1_3 = ttk.Button(root, text='3')
    input_button_1_3.grid(row=0, column=5)
    input_button_1_3['command'] = lambda: guessing_number(guess_num, 3)

    number_text = guess_num.input_build
    number_label = ttk.Label(main_frame, text=number_text, background="white")
    number_label.grid(row=0, column=2)
    guess_num.input_label = number_label

    reset_input_1 = ttk.Button(root, text='Reset')
    reset_input_1.grid(row=0, column=7)
    reset_input_1['command'] = lambda: reset_input(guess_num)

    test_input_1 = ttk.Button(root, text='Test')
    test_input_1.grid(row=0, column=8)
    test_input_1['command'] = lambda: check_input(guess_num)

    quit_button = ttk.Button(root, text='Quit')
    quit_button.grid(row=0, column=10)
    quit_button['command'] = lambda: quit_mid_game(root, main_frame, mqtt_client)

    print(guess_num.answer)

    # robot.left_motor.run_forever()
    # robot.right_motor.run_forever()
    # while robot.color_sensor.color is not "white":
    #     time.sleep(0.01)


def guessing_number(guess_numb, delta):
    if guess_numb.count_guess < 3:
        if guess_numb.input_build is 0:
            guess_numb.input_build = str(delta)
            label = guess_numb.input_build
            guess_numb.input_label['text'] = '{}'.format(label)
            guess_numb.count_guess += 1
        else:
            guess_numb.input_build = str(guess_numb.input_build) + str(delta)

            guess_numb.input_label['text'] = '{}'.format(guess_numb.input_build)
            guess_numb.count_guess += 1


def reset_input(guess_num):
    if guess_num.input_build != 0:
        guess_num.input_build = 0
        guess_num.input_label['text'] = guess_num.input_build
        guess_num.count_guess = 0


def check_input(guess_num):
    if guess_num.input_build == guess_num.answer:
        print('Correct:', guess_num.answer)
        guess_num.state = True
        print('Hack Successful!')
        hack(guess_num, robot)
        guess_num.count_guess = 0

    elif guess_num.input_build != guess_num.answer:
        print('Incorrect:', guess_num.input_build)
        guess_num.input_build = 0
        guess_num.input_label['text'] = 0
        print('Hack Failed')
        guess_num.count_guess = 0


def quit_mid_game(root, main_frame, mqtt_client):
    mqtt_client.send_message("stop")
    root.destroy()


def hack(guess_num, robot):
    print('Hacked!')
    guess_num.answer = str(random.randint(1, 3)) + str(random.randint(1, 3)) + str(random.randint(1, 3))
    print(guess_num.answer)

    def main():
        mqtt_client = com.MqttClient()
        mqtt_client.connect_to_ev3()

        control_root = tkinter.Tk()
        control_root.title("MQTT Remote")

        main_frame = ttk.Frame(control_root, padding=20, relief='raised')
        main_frame.grid()

        left_speed_label = ttk.Label(main_frame, text="Left")
        left_speed_label.grid(row=0, column=0)
        left_speed_entry = ttk.Entry(main_frame, width=8)
        left_speed_entry.insert(0, "600")
        left_speed_entry.grid(row=1, column=0)

        right_speed_label = ttk.Label(main_frame, text="Right")
        right_speed_label.grid(row=0, column=2)
        right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
        right_speed_entry.insert(0, "600")
        right_speed_entry.grid(row=1, column=2)

        forward_button = ttk.Button(main_frame, text="Forward")
        forward_button.grid(row=2, column=1)
        # forward_button and '<Up>' key is done for your here...
        forward_button['command'] = lambda: send_forward(mqtt_client, left_speed_entry, right_speed_entry)
        control_root.bind('<Up>', lambda event: send_forward(mqtt_client, left_speed_entry, right_speed_entry))

        left_button = ttk.Button(main_frame, text="Left")
        left_button.grid(row=3, column=0)
        # left_button and '<Left>' key
        left_button['command'] = lambda: send_left(mqtt_client, left_speed_entry, right_speed_entry)
        control_root.bind('<Left>', lambda event: send_left(mqtt_client, left_speed_entry, right_speed_entry))

        stop_button = ttk.Button(main_frame, text="Stop")
        stop_button.grid(row=3, column=1)
        # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
        stop_button['command'] = lambda: send_stop(mqtt_client)
        control_root.bind('<space>', lambda event: send_stop(mqtt_client))

        right_button = ttk.Button(main_frame, text="Right")
        right_button.grid(row=3, column=2)
        # right_button and '<Right>' key
        right_button['command'] = lambda: send_right(mqtt_client, left_speed_entry, right_speed_entry)
        control_root.bind('<Right>', lambda event: send_right(mqtt_client, left_speed_entry, right_speed_entry))

        back_button = ttk.Button(main_frame, text="Back")
        back_button.grid(row=4, column=1)
        # back_button and '<Down>' key
        back_button['command'] = lambda: send_backward(mqtt_client, left_speed_entry, right_speed_entry)
        control_root.bind('<Down>', lambda event: send_backward(mqtt_client, left_speed_entry, right_speed_entry))

        control_root.after(10000, lambda: close_control_root(mqtt_client, control_root))
        control_root.mainloop()

    def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
        mqtt_client.send_message("forward", [int(left_speed_entry.get()), int(right_speed_entry.get())])

    def send_backward(mqtt_client, left_speed_entry, right_speed_entry):
        mqtt_client.send_message("backward", [int(left_speed_entry.get()), int(right_speed_entry.get())])

    def send_left(mqtt_client, left_speed_entry, right_speed_entry):
        mqtt_client.send_message("left", [int(left_speed_entry.get()), int(right_speed_entry.get())])

    def send_right(mqtt_client, left_speed_entry, right_speed_entry):
        mqtt_client.send_message("right", [int(left_speed_entry.get()), int(right_speed_entry.get())])

    def send_stop(mqtt_client):
        mqtt_client.send_message("stop")

    def close_control_root(mqtt_client, control_root):
        mqtt_client.send_message("stop")
        # mqtt_client.send_message("seek_beacon")
        control_root.destroy()

    # ----------------------------------------------------------------------
    # Calls  main  to start the ball rolling.
    # ----------------------------------------------------------------------
    main()




title_screen()