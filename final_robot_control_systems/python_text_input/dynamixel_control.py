
# dynamixel_control.py
import threading
import time
import rospy
from dynamixel_sdk import *  # Uses Dynamixel SDK library
from std_msgs.msg import Int32

# Control table address
ADDR_MX_TORQUE_ENABLE = 24
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36

# Protocol version
PROTOCOL_VERSION = 1.0

# Default setting
DXL_ID = 0                 # Dynamixel ID : 1
BAUDRATE = 1000000            # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/ttyUSB0'    # Check which port is being used on your controller

TORQUE_ENABLE = 1          # Value for enabling the torque
TORQUE_DISABLE = 0         # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE = 950         # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE = 3100        # and this value

# Initialize port handler and packet handler
portHandler = None
packetHandler = None
emergency_stop = False


# Initialize port handler and packet handler
def init_dynamixel():
    global portHandler, packetHandler
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)
   
    # Open port
    if not portHandler.openPort():
        print("Failed to open the port")
        quit()
   
    # Set port baudrate
    if not portHandler.setBaudRate(BAUDRATE):
        print("Failed to change the baudrate")
        quit()
   
    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(f'Error [{dxl_comm_result}]: Failed to enable torque!')
        quit()
    elif dxl_error != 0:
        print(f'Error: Dynamixel error [{dxl_error}]')
        quit()
    
    print("Initalization Succesful!")


# takes in id and position to set one motor at a time 
def set_motor_position(id, position):
    def move_motor():
        if not emergency_stop:
            dxl_goal_position = position
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, id, ADDR_MX_GOAL_POSITION, dxl_goal_position)
            if dxl_comm_result != COMM_SUCCESS:
                print(f'Error [{dxl_comm_result}]: Failed to write goal position!')
            elif dxl_error != 0:
                print(f'Error: Dynamixel error [{dxl_error}]')
            else:
                print(f'Set goal position to: {dxl_goal_position}')
        else:
            print('Emergency stop triggered!')
   
    # Create a new thread for motor movement
    motor_thread = threading.Thread(target=move_motor)
    motor_thread.start()



# takes in a list of ids and list of positions to set multiple motors at once 
def set_motor_multiple_position(ids, positions): 
    def move_motor():
        if not emergency_stop:

            number_of_items = len(ids)

            for x in range(number_of_items): 
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ids[x], ADDR_MX_GOAL_POSITION, positions[x])
   
            if dxl_comm_result != COMM_SUCCESS:
                print(f'Error [{dxl_comm_result}]: Failed to write goal position!')
            elif dxl_error != 0:
                print(f'Error: Dynamixel error [{dxl_error}]')
            else:
                print(f'Set goal position to: {positions[0]}')
        else:
            print('Emergency stop triggered!')
   
    # Create a new thread for motor movement
    motor_thread = threading.Thread(target=move_motor)
    motor_thread.start()


#returns position of a motor based on id that has been passed in 
def get_motor_position(id): 
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, id, ADDR_MX_PRESENT_POSITION)
    return dxl_present_position


# instantly stops motor movement by disabling and renabling torque to hold robot in stopped position
def emergency_stop_motors(state):
    global emergency_stop
    emergency_stop = state
   
    for x in range(8): 

        packetHandler.write1ByteTxRx(portHandler, x, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
        packetHandler.write1ByteTxRx(portHandler, x, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
        print("Emergency stop triggered!")

# return emergency state variable of robobt 
def get_emergency(): 
    global emergency_stop
    return emergency_stop


def disable_motor_torque(id): 
    packetHandler.write1ByteTxRx(portHandler, id, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)

def enable_motor_torque(id): 
    packetHandler.write1ByteTxRx(portHandler, id, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE) 

def disable_robot(): 
    for x in range(8): 
        disable_motor_torque(x)

def enable_robot(): 
    for x in range(8): 
        enable_motor_torque(x)


def close_dynamixel():
    # Disable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(f'Error [{dxl_comm_result}]: Failed to disable torque!')
    elif dxl_error != 0:
        print(f'Error: Dynamixel error [{dxl_error}]')

    # Close port
    portHandler.closePort()

