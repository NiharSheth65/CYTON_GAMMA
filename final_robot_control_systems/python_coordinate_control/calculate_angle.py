# import ikpy.chain
# import ikpy.utils.plot as plot_utils

# import numpy as np
# import time
# import math


# import ipywidgets as widgets
# import serial

# my_chain = ikpy.chain.Chain.from_urdf_file(
#     "robot3.urdf",
#     active_links_mask=[False, True, True, True, True, True])



# angles_in_degrees = []

# def make_calculations(x, y, z): 

#       target_position = [x, y, z]
#       target_orientation = [0, 0, -1]
#       initial_guess = [0, 0.1,]
#       orientation_constraint = np.array([0, 0, -1])  

#     #   ik = my_chain.inverse_kinematics(target_position,
#     #                                 target_orientation,
#     #                                 orientation_mode="Y")

#       ik = my_chain.inverse_kinematics(
#            target_position, 
#            target_orientation=orientation_constraint
#       )

#       global angles_in_degress
#       angles_in_degress = list(map(lambda r: math.degrees(r), ik.tolist()))

#       import matplotlib.pyplot as plt

#       fig, ax = plot_utils.init_3d_figure()
#       fig.set_figheight(9)
#       fig.set_figwidth(13)
#       my_chain.plot(ik, ax, target=target_position)
#       plt.xlim(-0.5, 0.5)
#       plt.ylim(-0.5, 0.5)
#       ax.set_zlim(0, 0.6)
#       plt.ion()
#       plt.show()

# def send_angles(): 
#     return angles_in_degress

# # input("Press [enter] to continue.")

