import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ikpy.chain
import ikpy.utils.plot as plot_utils
from dynamixel_control import * 
import subprocess

import numpy as np
import time
import math

#system settings 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

angles_in_degrees = []

start_positions = [2000, 2175, 2085, 825, 2090, 1100, 2000, 3100]
# ---------------------------------------------

my_chain = ikpy.chain.Chain.from_urdf_file(
    "robot3.urdf",
    active_links_mask=[False, True, True, True, True, True])

# ---------------------------------------------


angle = -78 #-44 
angle2 = -33 #-15 
angle3 = -86 #-77 

angle4 = -65
max_encoder = 4096 

motor_one_offset = 2025 
motor_two_offset = 2050 
motor_three_offset = 2169 
motor_four_offset = 2066


def start_roscore_in_new_terminal(): 

    command = "roscore"

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])
    print("Success, started roscore!\n") 


# start background progam 
def start_robot_control(): 

    command = "rosrun conformal_ros dynamixel_control.py"

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])




def start_process(): 
    start_roscore_in_new_terminal() 
    start_robot_control() 
    init_dynamixel() 


def move_motors(): 
        

        encoder_output_one = int((angles_in_degrees[1]*max_encoder)/360) + motor_one_offset
        encoder_output_two = int((angles_in_degrees[2]*max_encoder)/360) + motor_two_offset
        encoder_output_three = int((angles_in_degrees[3]*max_encoder)/360) + motor_three_offset
        encoder_output_four = int((angles_in_degrees[4]*max_encoder)/360) + motor_four_offset
        
        print(f"Angle One: {angles_in_degrees[1]}")
        print(f"Angle Two: {angles_in_degrees[2]}")        
        print(f"Angle Three: {angles_in_degrees[3]}")
        print(f"Angle Four: {angles_in_degrees[4]}")

        # set_motor_multiple_position([1,5], [encoder_output_two, encoder_output_four])
        set_motor_multiple_position([0, 1,3, 5], [encoder_output_one, encoder_output_two, encoder_output_three, encoder_output_four])
        time.sleep(3)



def do_calculations(x,y,z): 
    target_position = [x, y, z]
    target_orientation = [0, 0, -1]
    orientation_constraint = np.array([0, 0, -1])  

    ik = my_chain.inverse_kinematics(
        target_position, 
        target_orientation=orientation_constraint
    )

    global angles_in_degrees
    angles_in_degrees = list(map(lambda r: math.degrees(r), ik.tolist()))

    # Compute the forward kinematics using the joint angles from IK
    fk_results = my_chain.forward_kinematics(ik)

    # Extract the position from the forward kinematics result
    fk_position = fk_results[:3, 3]

    # Print and compare the positions
    print("Target position:", target_position)
    print("FK position:", fk_position)


    show_plot(ik, target_position, validate_position(target_position, fk_position))


def show_plot(ik, pos, valid):


    fig, ax = plot_utils.init_3d_figure()
    fig.set_figheight(2)
    fig.set_figwidth(3)
    my_chain.plot(ik, ax, target=pos)
    plt.xlim(-0.5, 0.5)
    plt.ylim(-0.5, 0.5)
    ax.set_zlim(0, 0.6)
    # plt.ion()
    # plt.show()

    plot_window = ctk.CTkToplevel()
    plot_window.geometry("300x300")
    plot_window.title("Matplotlib Plot")

    popup_frame = ctk.CTkFrame(master=plot_window) 
    popup_frame.pack(fill="both", expand="True")

    # # Create a canvas to display the plot
    canvas = FigureCanvasTkAgg(fig, master=popup_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    if valid: 

        #alert text 
        home_label = ctk.CTkLabel(master=popup_frame, text="Position Is Valid:")
        home_label.pack(pady=10)
        

        button_frame = ctk.CTkFrame(master=plot_window) 
        button_frame.pack()

        #proceed button 
        proceed_button = ctk.CTkButton(master=button_frame, text="Move to Position", command=send_to_motors)
        proceed_button.pack(side="left", pady=10, padx=10)

        #proceed button 
        cancel_button = ctk.CTkButton(master=button_frame, text="Cancel", command=plot_window.destroy)
        cancel_button.pack(side="right", pady=10, padx=10)

    else: 
            #alert text 
        home_label = ctk.CTkLabel(master=popup_frame, text="Position Is Invalid:")
        home_label.pack(pady=10) 




    

def validate_position(target, forward):
    
    is_position_valid = False

    for x in range(3): 
        print(f"Target: {target[x]}") 

        if(abs(forward[x]-target[x]) < 0.01): 
            is_position_valid = True
        
        else: 
            is_position_valid = False
            break

    return is_position_valid


def send_to_motors():   
    move_motors()


def send_angles(): 
    return angles_in_degrees

def home_all_position(): 


        
    #alert popup 
    home_window = ctk.CTkToplevel(master = app)
    home_window.geometry("300x100")
    home_window.title("Alert")

    #alert text 
    home_label = ctk.CTkLabel(master=home_window, text="Are You Sure Re-centre Robot?")
    home_label.pack(pady=10)

    #proceed button 
    proceed_button = ctk.CTkButton(master=home_window, text="Yes", command=lambda: home_all(home_window))
    proceed_button.pack(pady=5)

    #cancel button 
    cancel_button = ctk.CTkButton(master=home_window, text="No", command=home_window.destroy)
    cancel_button.pack(pady=5)

# home_all() function used check if robot is already in home position 
# if robot is not in home position, GUI will update and alert user that robot is homing
# robot will initiate homing sequence  
def home_all(alert): 

    print('SHOULD BE READY TO HOME!')
    alert.destroy() 


    def get_motor():
        alternate_home_all() 
        time.sleep(3)

        if(is_robot_at_home()): 
            show_alert("Robot Homed Succesfully")
        else: 
            show_alert("Robot Homed Unsuccesfully")

            

    # Create a new thread for motor movement
    motor_thread = threading.Thread(target=get_motor)
    motor_thread.start()
       

# alternate_home_all() function simply sets all motors back to home position at the same time, rather than one after the other
def alternate_home_all(): 
    set_motor_multiple_position([0,1,2,3,4,5,6,7], [start_positions[0], start_positions[1], start_positions[2], start_positions[3], start_positions[4], start_positions[5], start_positions[6], start_positions[7]])
     

def is_robot_at_home(): 

    isHome = False

    for x in range(0, 8): 
        if(get_motor_independent(x)/start_positions[x] > 0.95 and get_motor_independent(x)/start_positions[x] < 1.05 ): 
            isHome = True 
        else: 
            isHome = False
            break; 

    return isHome

def get_motor_independent(id): 
    return get_motor_position(id)

def show_alert(message): 
    #alert popup 
    alert_window = ctk.CTkToplevel(master = app)
    alert_window.geometry("300x100")
    alert_window.title("Alert")

    #alert text 
    alert_label = ctk.CTkLabel(master=alert_window, text=message)
    alert_label.pack(pady=10)

    #close button 
    close_button = ctk.CTkButton(master=alert_window, text="OK", command=alert_window.destroy)
    close_button.pack(pady=5)
# ---------------------------------------------

# Initialize the application
app = ctk.CTk()

# Set the title and size of the window
app.title("Coordinate GUI")
app.geometry("700x480")

#ui elements 
title = ctk.CTkLabel(master=app, text="Coordinate Control", font=("Arial", 20, "bold")) 
title.pack(pady=20)


# Create and place three entry widgets
input_x = ctk.CTkLabel(master=app, text="X: Value")
input_x.pack(pady=10)

entry_x = ctk.CTkEntry(app, placeholder_text="Ex...0.25")
entry_x.pack(pady=10)

input_y = ctk.CTkLabel(master=app, text="Y: Value")
input_y.pack(pady=10)

entry_y = ctk.CTkEntry(app, placeholder_text="Ex...0.25")
entry_y.pack(pady=10)

input_z = ctk.CTkLabel(master=app, text="Z: Value")
input_z.pack(pady=10)

entry_z = ctk.CTkEntry(app, placeholder_text="Ex...0.25")
entry_z.pack(pady=10)

# Define the callback function for the button
def on_proceed():
    do_calculations(float(entry_x.get()), float(entry_y.get()), float(entry_z.get()))


# Create and place the "Proceed" button
proceed_button = ctk.CTkButton(app, text="Proceed", command=on_proceed)
proceed_button.pack(pady=20)

# Create and place the "Proceed" button
home_button = ctk.CTkButton(app, text="Re-centre", command=home_all_position)
home_button.pack(pady=20)

#start stuff 
start_process() 

# Run the application
app.mainloop()
