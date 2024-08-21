# import math
# from robot_operater import * 
# from dynamixel_control import * 
# # from calculate_angle import* 

# # Motor 0 at position 2262
# # Motor 1 at position 1982
# # Motor 2 at position 2048
# # Motor 3 at position 2169
# # Motor 4 at position 2080
# # Motor 5 at position 2066
# # Motor 6 at position 1925
# # Motor 7 at position 3096y

# angle = -78 #-44 
# angle2 = -33 #-15 
# angle3 = -86 #-77 

# angle4 = -65
# max_encoder = 4096 

# motor_one_offset = 2025 
# motor_two_offset = 2050 
# motor_three_offset = 2169 
# motor_four_offset = 2066



# def start_process(): 
#     start_roscore_in_new_terminal() 
#     start_robot_control() 
#     init_dynamixel() 
#     get_all_motors() 


# def move_motors(): 
        
#         angles = send_angles() 

#         encoder_output_one = int((angles[1]*max_encoder)/360) + motor_one_offset
#         encoder_output_two = int((angles[2]*max_encoder)/360) + motor_two_offset
#         encoder_output_three = int((angles[3]*max_encoder)/360) + motor_three_offset
#         encoder_output_four = int((angles[4]*max_encoder)/360) + motor_four_offset
        
#         print(f"Angle One: {angles[1]}")
#         print(f"Angle Two: {angles[2]}")        
#         print(f"Angle Three: {angles[3]}")
#         print(f"Angle Four: {angles[4]}")

#         # set_motor_multiple_position([1,5], [encoder_output_two, encoder_output_four])
#         set_motor_multiple_position([0, 1,3, 5], [encoder_output_one, encoder_output_two, encoder_output_three, encoder_output_four])
#         time.sleep(3)

