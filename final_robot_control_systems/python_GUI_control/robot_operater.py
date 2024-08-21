
import subprocess
import threading
from dynamixel_control import* 
import time


# home position for arm 
start_positions = [2000, 2175, 2085, 825, 2090, 1100, 2000, 3100]
set_positions = [2000, 2175, 2085, 825, 2090, 1100, 2000, 3100]

tmp_positions_list = [] 

#SAVED POINTS
save_positions_one = [2000, 2175, 2000, 825, 1900, 1100, 1800, 3100]
save_positions_two = [2000, 2175, 2000, 825, 1900, 1100, 1800, 3100]

#----------------------------------------START COMMANDS---------------------------------------------#

# start ROS 
def start_roscore_in_new_terminal(): 

    command = "roscore"

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])
    print("Success, started roscore!\n") 


# start background progam 
def start_robot_control(): 

    command = "rosrun conformal_ros dynamixel_control.py"

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])



#----------------------------------------INPUT COMMANDS---------------------------------------------#

# numerical input 
def numerical_input(test, min, max, message): 
    val = test
    while(val < min or val > max): 

        val = int(input(f"{message} ({min}-{max}): ")) 
    
    return val


# motor ID Input 
def motor_id_input(): 
    return numerical_input(-1, 0, 7, "Enter Motor ID")



# motor position input 
def motor_position_input(): 
    return  numerical_input(949, 950, 3100, "Enter Motor Position")

# prevents any other inputs other than a yes or no 
def yesNoInput(message): 
    
    userInput = ""
    while True:

        userInput = input(f"{message}(Y/N):  ").upper()

        if(userInput == "Y" or userInput == "N"): 
            break 

    return userInput



#----------------------------------------MOTOR COMMANDS---------------------------------------------#

#sets one specific motor to a position on a new thread 
def set_motor_independent(id, position): 

    def move_motor():
        set_motor_position(id, position)

    # Create a new thread for motor movement
    motor_thread = threading.Thread(target=move_motor)
    motor_thread.start()

#returns position of motor 
def get_motor_independent(id): 
    return get_motor_position(id)


#returns position of all motor on robot 
def get_all_motors(): 
    for x in range(8): 
        get_motor_independent(x)

#homes specific motor through setting motor to its position from start_positions 
def home_motor_independent(id): 
     set_motor_independent(id, start_positions[id])


#homes each motor one after the other, not actually used in GUI
def home_all_motors(): 

    sleepTime = 24

    for x in range(8):
        if(is_motor_at_home(x)): 
            sleepTime -= 3 

    def non_blocking_home_all(): 
        for x in range(8):

            if(is_motor_at_home(x) == False): 
                home_motor_independent(x)
                time.sleep(3)
    

            print(f"check if motor {x} is at home {is_motor_at_home(x)}")

         
    thread = threading.Thread(target=non_blocking_home_all)
    thread.start()  

    print(f"TOTAL SLEEP TIME: {sleepTime}")

    return sleepTime

#simple delay timer 
def non_blocking_delay(seconds): 

    def delayed_function(): 
        time.sleep(seconds)
        # callback() 

    thread = threading.Thread(target=delayed_function)
    thread.start()  


#checks if robot is at home by comparing current position with position in start_positions 
def is_robot_at_home(): 

    isHome = False

    for x in range(0, 8): 
        if(get_motor_independent(x)/start_positions[x] > 0.95 and get_motor_independent(x)/start_positions[x] < 1.05 ): 
            isHome = True 
        else: 
            isHome = False
            break; 

    return isHome

#check if motor is at home by comparing motor position to position set in start_positions 
def is_motor_at_home(id): 

    isHome = False

    if(get_motor_independent(id)/start_positions[id] > 0.95 and get_motor_independent(id)/start_positions[id] < 1.05): 
        isHome = True 
    else: 
        isHome = False

    return isHome

def has_motor_reached_set_point(id): 

    if(abs(1 - get_motor_independent(id)/set_positions[id]) < 0.05): 
        print("MOTOR REACHED POSITION!")
        return True
    else: 
        print('NOT REACHED POSITION!')
        return False


#calibration protocol checks motor position at 3 different set points, if position is within a 
#certain tolerance of set point, it is safe to assume the robot is in the correct place  
def calibrate_motor_independent(id): 

    succesfulCount = 0 
    positions = [1200, 2800, start_positions[id]]                    

    for y in range(3): 
        if(get_emergency() == False): 

            #check positioning
            set_motor_independent(id, positions[y])
            time.sleep(4)

            set_positions[id] = positions[y]
                    
            #step 1
            if(has_motor_reached_set_point(id)): 
                succesfulCount += 1
                print("GREAT MOTOR HAS REACHED!")
            
            else: 
                print('Failed, motor has not reached!')
        else: 
            print("GET OUT OF LOOP")
            break
    print("------------------------------REACHED OUTSIDE-----------------------------")     
    if(succesfulCount == 3): 
        return True 
        
    else: 
        return False       


#----------------------------------------USER COMMANDS---------------------------------------------#

#user control enables this python file to be used as input/output function rather than through a GUI
def user_control(): 
    while True: 
        userChoice = numerical_input(-1, 1, 7, "\n1. Set Motor Position \n2. Get Motor Position \n3. Get Position of All Motors \n4. Home All Motors \n5. Home Specific Motor \n6. Exit  \nChoose one of the following options: ")

        #set position of specific motor 
        if(userChoice == 1): 
            motorID = motor_id_input()
            motorPosition = motor_position_input() 

            set_motor_independent(motorID, motorPosition)
       
        #get position of specific motor 
        elif(userChoice == 2):
            get_motor_independent(motor_id_input())
                   
        #get position of specific motor 
        elif(userChoice == 3): 
            get_all_motors()

        elif(userChoice == 4): 
            home_all_motors()

        elif(userChoice == 5): 
            motor_to_home = motor_id_input() 
            home_motor_independent(motor_to_home)

        elif(userChoice == 6): 
            print('Exiting...')
            break 
    
        elif(userChoice == 7): 
            print("SHOULD ESTOP")
            emergency_stop_motors(True)

        else: 
            print("Please enter a valid input!")



if __name__ == "__main__": 

    start = yesNoInput("Do you want to start the robot? ") 

    if(start == 'Y'): 
        print("Starting Roscore... ")
        start_roscore_in_new_terminal() 

        startRobot = yesNoInput("Do you want to run the robot? ")

        if(startRobot == "Y"): 
            
            start_robot_control() 

            print('GREAT SUCCESS!')
            init_dynamixel() 
            user_control() 
    else: 
        print('Relaunch to try again!')




