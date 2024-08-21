import pybullet as p
import pybullet_data
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import customtkinter as ctk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk 


def init_3d_figure(): 
    fig = plt.figure() 
    ax = fig.add_subplot(111, projection='3d')
    return fig, ax


# Connect to PyBullet in DIRECT mode (no GUI needed)
physicsClient = p.connect(p.DIRECT)

# Load URDF model for the robot
p.setAdditionalSearchPath(pybullet_data.getDataPath())
robot_id = p.loadURDF("robot3.urdf")

# Define the target position for the end-effector
target_position = [11.0, 11.5, 0.25]  # Change this to your target position

# Get the number of joints in the robot
num_joints = p.getNumJoints(robot_id)
print(f"Number of joints: {num_joints}")

# Define which joints to use for IK (e.g., first 4 joints)
ik_joints = [0, 1, 3, 5]  # Adjust this based on which joints you want to use

# Set the positions of the remaining joints to fixed values
fixed_joint_angles = [0] * num_joints
for i in range(len(fixed_joint_angles)):
    if i not in ik_joints:
        p.resetJointState(robot_id, i, fixed_joint_angles[i])

# Compute inverse kinematics for the end-effector link
end_effector_link_index = num_joints - 1  # Usually the last link
try:
    joint_angles = p.calculateInverseKinematics(
        robot_id, end_effector_link_index,
        target_position
    )

    # Apply the calculated angles only to the IK joints
    print("Calculated joint angles for IK joints:")
    for i in ik_joints:
        print(f"Joint {i}: {joint_angles[i]}")

    # ---------- random chat gpt part start 
    


    # fig, ax = init
    # fig.set_figheight(2)
    # fig.set_figwidth(3)
    # my_chain.plot(ik, ax, target=pos)
    # plt.xlim(-0.5, 0.5)
    # plt.ylim(-0.5, 0.5)
    # ax.set_zlim(0, 0.6)
    # # plt.ion()
    # # plt.show()

    # plot_window = ctk.CTkToplevel()
    # plot_window.geometry("300x300")
    # plot_window.title("Matplotlib Plot")

    # popup_frame = ctk.CTkFrame(master=plot_window) 
    # popup_frame.pack(fill="both", expand="True")

    # # # Create a canvas to display the plot
    # canvas = FigureCanvasTkAgg(fig, master=popup_frame)
    # canvas.draw()
    # canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    for i, joint_index in enumerate(ik_joints): 
        p.resetJointState(robot_id, joint_index, joint_angles[i])

    joint_positions = [] 

    for joint_index in ik_joints: 
        link_state = p.getLinkState(robot_id, joint_index)
        joint_positions.append(link_state[0])


    x = [pos[0] for pos in joint_positions]
    y = [pos[1] for pos in joint_positions]
    z = [pos[2] for pos in joint_positions]


    fig, ax = init_3d_figure()
    fig.set_figheight(4)
    fig.set_figwidth(6)
    

    ax.plot(x,y,z, color='blue')
    ax.scatter(x,y,z, color='red', s=100)

    plt.xlim(-0.5, 0.5)
    plt.ylim(-0.5, 0.5)
    ax.set_zlim(0, 0.6)


    plot_window = ctk.CTkToplevel() 
    plot_window.geometry('600x400')

    popup_frame = ctk.CTkFrame(master=plot_window)
    popup_frame.pack(fill='both', expand=True)

    canvas = FigureCanvasTkAgg(fig, master=popup_frame)
    canvas.draw() 
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True) 

    # plt.show() 

    plot_window.mainloop() 
    # ---------- random chat gpt part start 

except Exception as e:
    print(f"An error occurred during IK computation: {e}")

# Disconnect from the PyBullet server
p.disconnect()
