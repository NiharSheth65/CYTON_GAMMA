# File: robot_operator_gui.py 
# Author: Nihar Sheth
# Description: A Python Tkinter based GUI which enables user input for robot operation.

import tkinter as tk 
import customtkinter
import subprocess
from robot_operater import* 

#system settings 
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

#----------------------------------------ROBOT COMMANDS---------------------------------------------#

# set_position() function used to extract position set point from either entry field or slider 
# function ensures that setpoint is within an acceptable range, and if all conditions are met, it sets the position to the desired motor 
# throws an alert at the user has not selected a motor or has selected a set point out of range 
# updates table after motor position has been set 
def set_position(id, position): 
  
    try: 

        if 950 <= position <= 3100:  

            
            print(f"THE SELECTED MOTOR IS: {motor_selected_val}")
            set_positions[id] = position


            motorGetPointLabel.configure(text=f"Current Position: {position}")
            set_motor_independent(id, position)
            positional_data[int(id)] = "Moving"
            set_positions_in_table(table_frame) 

            
        else: 
            raise ValueError

    except ValueError: 
        show_alert("Input Out Of Range! Enter a value between 950 and 3100")
    
    def get_motor():
        time.sleep(3) 
        get_position()
        motorGetPointLabel.configure(text=f"Current Position: {get_motor_independent(int(get_dropdown()))}")

    # Create a new thread for motor movement
    motor_thread = threading.Thread(target=get_motor)
    motor_thread.start()



# get_position() function used to get the current position of each motor and updates position data list 
# calls function to update table 
def get_position(): 
   
    for x in range(8): 
        positional_data[x] = get_motor_independent(x)
        set_positions[x] = get_motor_independent(x)
        
    set_positions_in_table(table_frame) 




# able_robot() function used disable or enable robot
# immediatley cancels current action and updates user 
def able_robot(): 
    
    current_able_val = able_var.get()

    if current_able_val: 
        able_var.set(False)
        motorStatusLabel.configure(text=f"Motor Status: Disabled", text_color="red")
        button_able.configure(text="Enable", fg_color="#3f9546", hover_color="#43a04b")
        show_alert("Emergency Stop Enabled!")
        emergency_stop_motors(True)

    else: 
        able_var.set(True)
        motorStatusLabel.configure(text=f"Motor Status: Enabled", text_color="#43a04b")
        button_able.configure(text="Disable", fg_color="#A52A2A", hover_color="#800020")
        show_alert("Emergency Stop Disabled!")
        emergency_stop_motors(False)


# home_position() function used reset motor to its home position 
# function first checks if motor is already in home position 
# if not in home position, the robot will set specific motor back to its home position 
def home_position(): 

    if(is_motor_at_home(get_dropdown())): 
        show_alert("Motor Is Already At Home!")

    else: 
        print("SHOULD BE HOMING!")
        motorStatusLabel.configure(text=f"Motor Status: MOTOR {get_dropdown()} IS HOMING", text_color="yellow")
        motorSetPointLabel.configure(text=f"Set Position: {start_positions[get_dropdown()]}")
        home_motor_independent(get_dropdown())

            
        def get_motor():
            time.sleep(3) 
            
            if(is_motor_at_home(get_dropdown())): 
                show_alert(f"Motor {dropdown.get()} Homed Successfully")
                motorStatusLabel.configure(text=f"Motor Status: MOTOR {dropdown.get()} HAS HOMED SUCCESSFULLY", text_color="green")
                motorGetPointLabel.configure(text=f"Current Position: {get_motor_independent(get_dropdown())}")
            else: 
                show_alert(f"Motor {dropdown.get()} Homed Unsuccesfully")
                motorStatusLabel.configure(text=f"Motor Status: MOTOR {dropdown.get()} HAS HOMED UNSUCCESSFULLY", text_color="red")


        # Create a new thread for motor movement
        motor_thread = threading.Thread(target=get_motor)
        motor_thread.start()       


# home_all_position() function used reset entire robot to its home position  
# function first confirm is user wants to home robot 
def home_all_position(): 
        
    #alert popup 
    home_window = customtkinter.CTkToplevel(master = app)
    home_window.geometry("300x100")
    home_window.title("Alert")

    #alert text 
    home_label = customtkinter.CTkLabel(master=home_window, text="Are You Sure You Want to Home All Motors?")
    home_label.pack(pady=10)

    #proceed button 
    proceed_button = customtkinter.CTkButton(master=home_window, text="Yes", command=lambda: home_all(home_window))
    proceed_button.pack(pady=5)

    #cancel button 
    cancel_button = customtkinter.CTkButton(master=home_window, text="No", command=home_window.destroy)
    cancel_button.pack(pady=5)

# home_all() function used check if robot is already in home position 
# if robot is not in home position, GUI will update and alert user that robot is homing
# robot will initiate homing sequence  
def home_all(alert): 
    alert.destroy() 

    if(is_robot_at_home()): 
        show_alert("Robot Is Already At Home!")

    else: 
        motorStatusLabel.configure(text=f"Motor Status: ROBOT IS HOMING", text_color="yellow")
        alternate_home_all() 

        def get_motor():
            alternate_home_all() 
            time.sleep(3)

            if(is_robot_at_home()): 
                show_alert("Robot Homed Succesfully")
                motorStatusLabel.configure(text=f"Motor Status: ROBOT HAS HOMED SUCCESFULLY", text_color="green")
            else: 
                show_alert("Robot Homed Unsuccesfully")
                motorStatusLabel.configure(text=f"Motor Status: ROBOT HAS HOMED UNSUCCESFULLY", text_color="red")
            
            get_position()

        # Create a new thread for motor movement
        motor_thread = threading.Thread(target=get_motor)
        motor_thread.start()
   

# alternate_home_all() function simply sets all motors back to home position at the same time, rather than one after the other
def alternate_home_all(): 
    set_motor_multiple_position([0,1,2,3,4,5,6,7], [start_positions[0], start_positions[1], start_positions[2], start_positions[3], start_positions[4], start_positions[5], start_positions[6], start_positions[7]])
     
# run_calibration_independent() function used calibrateentry_widget.focus_get() == entry_widget specific motor 
# if succesful, the table will populate with success 
# inf unsucceful, the table will populate with unsuccesful 
def run_calibration_independent(motor_id): 

    if(is_robot_at_home()): 
        print("ROBOT AT HOME! GOOD TO PROCEED!")

        calibration_data[motor_id] = "IN CALIBRATION"

        set_calibration_in_table(table_frame)   

        motorStatusLabel.configure(text=f"Motor Status: Motor {motor_id} In Calibration", text_color="yellow")

        def calibrate_motor(): 
            
            show_alert("MOTOR IS BEING CALIBRATED")

            time.sleep(1.5)
            motor_calibration = calibrate_motor_independent(motor_id)

            message = ""
            if(motor_calibration): 
                message = "SUCCESS"
                motorStatusLabel.configure(text=f"Motor Status: Motor {motor_id} Calibration Succeeded", text_color="green")
            else: 
                message = "FAILURE"
                motorStatusLabel.configure(text=f"Motor Status: Motor {motor_id} Calibration Failed", text_color="red")

            calibration_data[motor_id] = message
            set_calibration_in_table(table_frame)  

        motor_thread = threading.Thread(target=calibrate_motor)
        motor_thread.start()

    
    else: 
        print("ROBOT HAVING ISSUES, DO NOT PROCEED!")
        show_alert("ROBOT MUST BE HOMED, PLEASE HOME AND TRY AGAIN")

    

# show_alert() function is a general function where a message can be passed in to update something to a user 
# opens a window to display output to user 
def show_alert(message): 
    #alert popup 
    alert_window = customtkinter.CTkToplevel(master = app)
    alert_window.geometry("300x100")
    alert_window.title("Alert")

    #alert text 
    alert_label = customtkinter.CTkLabel(master=alert_window, text=message)
    alert_label.pack(pady=10)

    #close button 
    close_button = customtkinter.CTkButton(master=alert_window, text="OK", command=alert_window.destroy)
    close_button.pack(pady=5)

# slider(value) updates the global set_point_pos_val variable 
# updates motorSetPointLabel to display set point of motor 
def slider(value): 
    global set_point_pos_val
    set_point_pos_val = int(value)
    motorSetPointLabel.configure(text = f'Set Position: {int(value)}')

# update_slider(value) updates a variable which displays which motor has been selected 
# adjusts get point label to display where the motor currently was 
# adjusts slider position 
# updates the table 
def update_slider(value): 
    motorSelectionLabel.configure(text=f"Motor Selected: {value}")
    motorGetPointLabel.configure(text=f"Current Position: {get_motor_independent(int(value))}")
    slider_motor_zero.set(get_motor_independent(int(value)))
    get_position() 


# update_entry(value) updates a variable which displays which motor has been selected 
# adjusts get point label to display where the motor currently was 
# adjusts slider position 
# updates the table 
def update_entry(value):
    global set_point_pos_val
    set_point_pos_val = int(value)
    print(f"MOTOR SET POINT: {set_point_pos_val}")
    slider_motor_zero.set(int(value))
    motorSetPointLabel.configure(text=f"Set Position: {int(value)}")

# get_dropdown() returns which id has been selected in the drop down 
def get_dropdown(): 
    try: 
        if 0 <= int(dropdown.get()) <= 7:  
            return int(dropdown.get())
        
        else: 
            raise ValueError
    except ValueError: 
        show_alert("Pleas ensure drowndown is not empty!")



#random set point which set robot to a specific position 
def set_point_one(): 
    set_motor_multiple_position([0,1,5,6,7], [1500, 1500, 1500, 950, 3100])

#a second random point which sets robot to specific set point 
def set_point_two(): 
    set_motor_multiple_position([0,1,5,6,7], [2500, 2500, 2500, 3100, 1200])

# clawControl() opens and closes the claw by toggling the same button and updating the label 
def clawControl(): 
    current_claw_val = claw_var.get()

    if current_claw_val: 
        set_motor_independent(7, 3100)
        claw_var.set(False)
        claw_position.configure(text="Close Claw")
        

    else: 
        set_motor_independent(7, 1200)
        claw_var.set(True)
        claw_position.configure(text="Open Claw")
        
 


def disable_robot_torque(): 
    print("ROBOT SHOULD DISABLE!")
    disable_robot() 


def enable_robot_torque():
    print('ROBOT SOHULD ENABLE!') 
    enable_robot() 


def save_position(): 
    print(f"SAVING POSITION TO: {get_motor_independent(1)}")

    if(new_setpoint_var.get() == 0): 
        save_positions_one[0] = get_motor_independent(0)
        save_positions_one[1] = get_motor_independent(1)
        save_positions_one[2] = get_motor_independent(2)
        save_positions_one[3] = get_motor_independent(3)
        save_positions_one[4] = get_motor_independent(4)
        save_positions_one[5] = get_motor_independent(5)
        save_positions_one[6] = get_motor_independent(6)
        save_positions_one[7] = get_motor_independent(7)

    else: 
        save_positions_two[0] = get_motor_independent(0)
        save_positions_two[1] = get_motor_independent(1)
        save_positions_two[2] = get_motor_independent(2)
        save_positions_two[3] = get_motor_independent(3)
        save_positions_two[4] = get_motor_independent(4)
        save_positions_two[5] = get_motor_independent(5)
        save_positions_two[6] = get_motor_independent(6)
        save_positions_two[7] = get_motor_independent(7)

    
def move_to_position_one(): 

    if new_setpoint_var.get() == 0: 
        set_motor_multiple_position([0,1, 2, 3, 4, 5, 6, 7], [save_positions_one[0], save_positions_one[1], save_positions_one[2], save_positions_one[3], save_positions_one[4], save_positions_one[5], save_positions_one[6], save_positions_one[7]])
    else: 
        set_motor_multiple_position([0,1, 2, 3, 4, 5, 6, 7], [save_positions_two[0], save_positions_two[1], save_positions_two[2], save_positions_two[3], save_positions_two[4], save_positions_two[5], save_positions_two[6], save_positions_two[7]])


def update_setpoints(value): 
    print(f"Working on setpoint: {value}")



#----------------------------------------TABLE COMMANDS---------------------------------------------#

# set_table() function sets the headers for a table 
# calls three more functions responsible for setting motor ids, motor positions and calibration data 
def set_table(): 

    for x in range(3): 
        header_label = customtkinter.CTkLabel(table_frame, text=table_headers[x], font=("Arial", 12, "bold"), padx=10, pady=5)
        header_label.grid(row=0, column=x, sticky='nsew')

    set_identification_in_table(table_frame)
    set_positions_in_table(table_frame) 
    set_calibration_in_table(table_frame) 
   

# set_identification_in_table() function sets the ids of each motor into the table 
def set_identification_in_table(table_frame): 
    for x in range(8):
        cell_label = customtkinter.CTkLabel(table_frame, text=x, padx=10, pady=5)
        cell_label.grid(row=x+1, column=0, stick='nswe')


# set_positions_in_table() function sets current positions of all motors in rable 
def set_positions_in_table(table_frame): 
    for y in range(8):
        cell_label = customtkinter.CTkLabel(table_frame, text=positional_data[y], padx=10, pady=5)
        cell_label.grid(row=y+1, column=1, stick='nswe')


# set_calibration_in_table() function sets calibration status of motors in table  
def set_calibration_in_table(table_frame): 
    
    for z in range(8):
        cell_label = customtkinter.CTkLabel(table_frame, text=calibration_data[z], padx=10, pady=5)
        cell_label.grid(row=z+1, column=2, stick='nswe')

# set table positions with current motor positions on load 
def initial_table_update(): 
    #set positions 
    for x in range(8): 
        positional_data[x] = get_motor_independent(x)
        set_positions[x] = get_motor_independent(x)

    set_table() 

def entry_on_change(): 
    print(entry_var.get())

#----------------------------------------KEY PRESS---------------------------------------------#



motor_selected_id = 0
increment_amount = 10 

def on_key_press(event): 
    
    global increment_amount
    global motor_selected_id

    key = event.keysym 

    focused_widget = str(app.focus_get()) 
    print(f"THE FOCUS IS CURRENLTY ON: {focused_widget}")

    if focused_widget == ".": 

        if key == 'space': 
            motor_selected_id = "" 


            for x in range(8): 
                set_positions[x] = get_motor_independent(x)

            print("DISABLE HAS BEEN ACTIVATED!")
            able_robot() 
        
        if(get_emergency() == False): 

                if key == "plus" or key == "KP_Add": 
                    increment_amount += 10 

                elif key == "minus" or key == "KP_Subtract": 
                    increment_amount -= 10       

                if increment_amount >= 100: 
                    increment_amount = 100 

                elif increment_amount <= 1: 
                    increment_amount = 1 

                print(f"INCREMENT AMOUNT: {increment_amount}")

                if key in ['0', '1', '2', '3', '4', '5', '6', '7']: 
                    motor_selected_id = key 
                    motor_selected_val = key

                elif key == 'Up': 
                    set_positions[int(motor_selected_id)] += increment_amount  

                elif key == 'Down': 
                    set_positions[int(motor_selected_id)] -= increment_amount
                
                elif key == 'H' or key == 'h': 
                    print("SHOULD TRY TO HOME!")
                    set_positions[int(motor_selected_id)] = start_positions[int(motor_selected_id)] 

                elif key == 'C' or key == 'c': 
                    # clawControl() 
                    motor_selected_id = 7

                    if(set_positions[int(motor_selected_id)] == 3100): 
                        set_positions[int(motor_selected_id)] = 950; 
                    else: 
                        set_positions[int(motor_selected_id)] = 3100

                elif key == 'T' or key == 't': 
                    home_all_position() 


                elif key == "G" or key == "g": 
                    get_position() 

                elif key == "R" or key == 'r': 
                    run_calibration_independent(int(motor_selected_id)) 


                if(set_positions[int(motor_selected_id)] >= 3100): 
                    set_positions[int(motor_selected_id)] = 3100 

                elif(set_positions[int(motor_selected_id)] <= 950): 
                    set_positions[int(motor_selected_id)] = 950 

                print(f"SET MOTOR {int(motor_selected_id)} TO: {set_positions[int(motor_selected_id)]}")

                motorSelectionLabel.configure(text=f"Motor Selected: {int(motor_selected_id)}")
                motorGetPointLabel.configure(text=f"Current Position: {set_positions[int(motor_selected_id)]}")
                motorSetPointLabel.configure(text=f"Set Position: {set_positions[int(motor_selected_id)]}")
                dropdown_var.set(int(motor_selected_id))
                set_motor_independent(int(motor_selected_id), set_positions[int(motor_selected_id)])

        
    
#----------------------------------------RESETTING FOCUS ---------------------------------------------#

def switch_mode(mode): 
    
    print(f"REQUESTED MODE: {mode}")
    focused_widget = str(app.focus_get()) 

    if mode == "entry": 
        entry.focus_set()  
        mode_switch_button.configure(text="Keyboard Mode")
        mode_switch_label.configure(text="Current Mode: Entry Mode")

    else:  
   


        if focused_widget == '.!ctkframe.!ctkframe2.!ctkentry.!entry': 
            app.focus_set()
            mode_switch_button.configure(text="Entry Mode")
            mode_switch_label.configure(text="Current Mode: Keyboard Mode")

        elif focused_widget == '.':
            entry.focus_set()  
            mode_switch_button.configure(text="Keyboard Mode")
            mode_switch_label.configure(text="Current Mode: Entry Mode")
   

    
    print(f"THE FOCUS IS CURRENLTY ON: {focused_widget}")


#----------------------------------------USER INTERFACE ---------------------------------------------#

#app frame 
app = customtkinter.CTk() 
app.geometry("700x480")
app.title("Robot Control")

#---------------------------------------- TKINTER Variables ---------------------------------------------#

#tkinter variables 
entry_var = tk.StringVar() 
entry_var.trace_add("write", entry_on_change)

dropdown_var = tk.StringVar() 
claw_var = tk.BooleanVar(value=False) 
able_var = tk.BooleanVar(value=True)
slider_motor_zero_var = tk.IntVar() 
motor_output_var = tk.Variable()  
new_setpoint_var = tk.IntVar()


set_point_pos_val = 0 
motor_selected_val = 0


#---------------------------------------- TOP TITLE ---------------------------------------------#

#ui elements 
title = customtkinter.CTkLabel(master=app, text="Robot Control", font=("Arial", 20, "bold")) 
title.pack(pady=20)

#---------------------------------------- TOP CONTROL FRAME --------------------------------------------#

#top control frame 
top_control_frame = customtkinter.CTkFrame(master=app) 
top_control_frame.pack(fill="both", expand="True")


#---------------------------------------- Execute Command Panel ---------------------------------------------#


#features frame 
execeute_command_frame = customtkinter.CTkFrame(master=top_control_frame)
execeute_command_frame.pack(fill="both", side="left", expand="True")


#button frame 
button_frame = customtkinter.CTkFrame(master=execeute_command_frame) 
button_frame.place(relx=0.5, rely=0.5, anchor="center")

#motor selection label
execute_label = customtkinter.CTkLabel(master=button_frame, text="Execute Commands: ", font=("Arial", 15, "bold")) 
execute_label.pack(pady=10)

#button_frame_bottom
button_frame_top = customtkinter.CTkFrame(master=button_frame) 
button_frame_top.pack() 


#button_frame_bottom
button_frame_bottom = customtkinter.CTkFrame(master=button_frame) 
button_frame_bottom.pack() 

#button_frame_left
button_frame_left = customtkinter.CTkFrame(master=button_frame_bottom) 
button_frame_left.pack(fill="both", side="left", expand="True", padx=5, pady=5) 

#button_frame_left
button_frame_right = customtkinter.CTkFrame(master=button_frame_bottom) 
button_frame_right.pack(fill="both", side="left", expand="True", padx=5, pady=5) 

# -------------------------------- Execute Command BUTTONS -------------------------------- #



#enable/disable button 
button_able = customtkinter.CTkButton(master=button_frame_top, text="Disable", command=able_robot, fg_color="#A52A2A", hover_color="#800020", width=200)
button_able.pack(pady=5) 


#motor calibration protocol button 
button_run_motor_calibration = customtkinter.CTkButton(master=button_frame_left, text="Calibrate Motor", fg_color="#A52A2A", hover_color="#800020", command=lambda: run_calibration_independent(get_dropdown()))
button_run_motor_calibration.pack(pady = 5) 

#set position button 
button_set_position = customtkinter.CTkButton(master=button_frame_left, text="Set Position", command=lambda: set_position(get_dropdown(), set_point_pos_val))
button_set_position.pack(pady=5) 

#get position button 
button_get_position = customtkinter.CTkButton(master=button_frame_left, text="Get Position", command=get_position)
button_get_position.pack(pady=5) 

#home position button 
button_home_position = customtkinter.CTkButton(master=button_frame_right, text="Home Position", command=home_position)
button_home_position.pack(pady=5) 

# home all position button
button_home_all_position = customtkinter.CTkButton(master=button_frame_right, text="Home All", command=home_all_position)
button_home_all_position.pack(pady=5) 

# claw button
claw_position = customtkinter.CTkButton(master=button_frame_right, text="Open Claw: ", command=clawControl)
claw_position.pack(pady=5) 


# ----------------------------------------------------- Status Frame  ----------------------------------------------------

#status frame
status_frame = customtkinter.CTkFrame(master=top_control_frame)
status_frame.pack(fill="both", side="left", expand="True") 

#motor status 
motorStatusLabel = customtkinter.CTkLabel(master=status_frame, text="Motor Status: Enabled", font=("Arial", 20, "bold"))
motorStatusLabel.pack(pady=20)

#input bar
entry = customtkinter.CTkEntry(
    master=status_frame, 
    placeholder_text="Enter Position(950-3100)", 
    width=300, 
    textvariable=entry_var, 
)


entry.pack(pady=5)

entry.bind("<Return>", lambda event: update_entry(entry_var.get()))

#motor selection label
motorSelectionLabel = customtkinter.CTkLabel(master=status_frame, text="Motor Selection: ", font=("Arial", 15, "bold")) 
motorSelectionLabel.pack(pady=10)

#motor position label 
motorSetPointLabel = customtkinter.CTkLabel(master=status_frame, text="Set Position: ", font=("Arial", 15, "bold")) 
motorSetPointLabel.pack(pady=10)

#motor current position label 
motorGetPointLabel = customtkinter.CTkLabel(master=status_frame, text="Current Position: ", font=("Arial", 15, "bold")) 
motorGetPointLabel.pack(pady=10)

#slider bar 
slider_motor_zero = customtkinter.CTkSlider(
    master=status_frame, 
    from_=950, 
    to=3100, 
    variable=slider_motor_zero_var, 
    command=slider
) 

slider_motor_zero.pack(pady=10) 

#drop down 
options = [str(i) for i in range(8)]
dropdown = customtkinter.CTkOptionMenu(master=status_frame, values=options, width=200, variable=dropdown_var, command=update_slider)
dropdown.pack() 

#mode switch button 
mode_switch_button = customtkinter.CTkButton(master=status_frame, text="Entry Mode", command=lambda: switch_mode(None), fg_color="#A52A2A", hover_color="#800020")
mode_switch_button.pack(pady=10) 

#mode switch label 
mode_switch_label = customtkinter.CTkLabel(master=status_frame, text="Current Mode: Keyboard Mode ", font=("Arial", 15, "bold")) 
mode_switch_label.pack(pady=10) 

# ----------------------------------------------------- Positional Control Frame  ----------------------------------------------------


#coordinate frame
positional_control_frame = customtkinter.CTkFrame(master=top_control_frame)
positional_control_frame.pack(fill="both", side="left", expand="True") 


#feature button container 
positional_control_frame_sub_container = customtkinter.CTkFrame(master=positional_control_frame)
positional_control_frame_sub_container.place(relx=0.5, rely=0.5, anchor="center")


#motor selection label
position_control_label = customtkinter.CTkLabel(master=positional_control_frame_sub_container, text="Positional Control: ", font=("Arial", 15, "bold")) 
position_control_label.pack(pady=5)

#drop down 
set_point_options = [str(i) for i in range(2)]
dropdown_setpoints = customtkinter.CTkOptionMenu(master=positional_control_frame_sub_container, values=set_point_options, width=200, variable=new_setpoint_var, command=update_setpoints)
dropdown_setpoints.pack(fill="both", side="bottom", expand="True", padx=5, pady=5) 



#coordinate position button frame 
positional_button_frame = customtkinter.CTkFrame(master=positional_control_frame_sub_container)
positional_button_frame.pack(pady=10) 


#coordinate position button frame 
positional_save_button_frame = customtkinter.CTkFrame(master=positional_button_frame)
positional_save_button_frame.pack(fill="both", side="left", expand="True", padx=5, pady=5) 

#save position 
positional_button_save_position = customtkinter.CTkButton(master=positional_save_button_frame, text="Save Position", command=save_position, fg_color="#A52A2A", hover_color="#800020")
positional_button_save_position.pack(pady=5) 

#move to position one
positional_button_move_to_position = customtkinter.CTkButton(master=positional_save_button_frame, text="Move to Position", command=move_to_position_one, fg_color="#A52A2A", hover_color="#800020")
positional_button_move_to_position.pack(pady=5) 

#coordinate position button frame 
positional_torque_button_frame = customtkinter.CTkFrame(master=positional_button_frame)
positional_torque_button_frame.pack(fill="both", side="left", expand="True", padx=5, pady=5) 

#disable torque
positional_button_disable_torque = customtkinter.CTkButton(master=positional_torque_button_frame, text="Disable Torque", command=disable_robot_torque, fg_color="#52307c", hover_color="#3c1361")
positional_button_disable_torque.pack(pady=5) 

#enable torque
positional_button_enable_torque = customtkinter.CTkButton(master=positional_torque_button_frame, text="Enable Torque", command=enable_robot_torque, fg_color="#A52A2A", hover_color="#800020")
positional_button_enable_torque.pack(pady=5) 







# ----------------------------------------------------- Information Table ----------------------------------------------------

#information table 
table_frame = customtkinter.CTkFrame(master=app)
table_frame.pack(fill="both", expand=True, padx=10, pady=5) 

table_headers = ["Motor ID: ", "Position: ", "Calibration Status: "]

# ----------------------------------------------------- CONTROL/START PROCESS ----------------------------------------------------

#start stuff 
start_roscore_in_new_terminal() 
start_robot_control() 
init_dynamixel() 

#set positional data and calibation data to preset values 
positional_data = [0]*8
calibration_data = ["not calibrated"]*8

table_frame.grid_columnconfigure((0, 1, 2), weight=1)        
table_frame.grid_rowconfigure(tuple(range(len(positional_data) + 1)), weight=1)

get_position() 
set_table() 

# Bind clicks within the entry field to focus_entry
app.bind('<KeyPress>', on_key_press)
entry.bind("<FocusIn>", switch_mode("entry"))



#run app
app.mainloop() 
