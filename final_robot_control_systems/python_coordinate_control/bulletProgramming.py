import pybullet as p
import pybullet_data 

# Connect to PyBullet
physicsClient = p.connect(p.DIRECT)  # Use p.DIRECT to avoid GUI for just calculations

# Load a robot (example: a URDF file)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
robot_id = p.loadURDF("robot3.urdf")

# Define a target position for the end-effector
target_position = [0.5, 0.0, 0.5]
target_orientation = p.getQuaternionFromEuler([0, 0, 0])

# Perform IK
end_effector_link_index = 3  # Change to your robot's end-effector link index
joint_poses = p.calculateInverseKinematics(robot_id, end_effector_link_index, target_position, target_orientation)

# Print the computed joint angles
print("Computed joint angles:")
print(joint_poses)

# Disconnect from PyBullet
p.disconnect()
