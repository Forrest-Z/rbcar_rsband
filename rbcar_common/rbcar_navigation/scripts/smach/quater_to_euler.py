# I am rotating n 3D shape using Euler angles in the order of XYZ meaning that the object is first rotated along the X axis, then Y and then Z. I want to convert the Euler angle to Quaternion and then get the same Euler angles back from the Quaternion using some [preferably] Python code or just some pseudocode or algorithm. Below, I have some code that converts Euler angle to Quaternion and then converts the Quaternion to get Euler angles. However, this does not give me the same Euler angles.

# I think the problem is I don't know how to associate yaw, pitch and roll to X, Y an Z axes. Also, I don't know how to change order of conversions in the code to correctly convert the Euler angles to Quaternion and then convert the Quaternion to Euler angle so that I am able to get the same Euler angle back. Can someone help me with this?

# And here's the code I used:

# This function converts Euler angles to Quaternions:

import numpy as np

# def euler_to_quaternion(yaw, pitch, roll):

#         qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
#         qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
#         qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
#         qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

#         return [qx, qy, qz, qw]

# a = euler_to_quaternion(1.57, 0, 0)
# print(a)

# And this converts Quaternions to Euler angles:

def quaternion_to_euler(x, y, z, w):

        import math
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        X = math.degrees(math.atan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        Y = math.degrees(math.asin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        Z = math.degrees(math.atan2(t3, t4))

        return X, Y, Z
    
a = quaternion_to_euler(0, 0, 0.657444, 0.7535)
# b = quaternion_to_euler(0, 0, 0.6789, 0.77342)
# c = quaternion_to_euler(0, 0, -0.7316, -0.6816)
# d = quaternion_to_euler(0, 0, 0.9926, 0.116)
print(a)
# print(b)
# print(c)
# print(d)