#!/usr/bin/python
#__author__ = 'andy'



#import roslib
#roslib.load_manifest('razor_imu')
import rospy
from std_msgs.msg import Header, String
from geometry_msgs.msg import Quaternion, Vector3
from sensor_msgs.msg import Imu, MagneticField

import traceback
import math

import numpy
import serial
import string

g0 = 9.80665				# Gravity constant

# Init ros
rospy.init_node('razor_imu')

# Get some parameters
frame_id = rospy.get_param('~frame_id', '/imu')		# This is the frame in which the imu exist default /imu
port = rospy.get_param('~port', '/dev/razorimu')		# This is the serial port for the imu device default /dev/imu

# Open the serial port w/ baud rate of 57600
s = serial.Serial(port, 57600)

# Setup publishers (Purpose of each explained above)
pub = rospy.Publisher('/imu/data_raw', Imu, queue_size=10)
mag_pub = rospy.Publisher('/imu/mag_raw', MagneticField, queue_size=10)
raw_pub = rospy.Publisher('/imu/raw', String, queue_size=10)

# Function to handle the output of the imu device
# Input: Data - comma seperated string from imu
#	 now - the current time
# Output: Publishes imu parsed and raw
def handle_line(data, now):
    #Try to get data from string
    try:
	# Format example:
        # P:,257925,mp,168.249969,23.194071,479.150848,ap,40.882568,-248.846878,970.272583,gp,0.000050,0.000001,0.000019,T,27.56
        # Publish the raw data for debug purposes
        raw_pub.publish(data)
        acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z = data.split(',')
        rospy.loginfo(data)
        acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z = map(float, [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z])


    # Catch all exceptions
    except Exception:
        print repr(data)
        #rospy.loginfo("Error!!!!!!!!")
        traceback.print_exc()
        return


    acc_x = float(acc_x)*0.03646840148
    acc_y = float(acc_y)*0.03646840148
    acc_z = float(acc_z)*0.03646840148
    gyro_x = (float(gyro_x)/14.375)*0.0174532925
    gyro_y = (float(gyro_y)/14.375)*0.0174532925
    gyro_z = (float(gyro_z)/14.375)*0.0174532925
    mag_x = (float(mag_x)*.00256)/10000
    mag_y = float(mag_y)/230
    mag_z = float(mag_z)/230

    # Publish the IMU data
    pub.publish(Imu(
        header=Header(
            stamp=now,
            frame_id=frame_id,
        ),
        orientation=Quaternion(0, 0, 0, 0),
        orientation_covariance=[-1] + [0]*8,
        angular_velocity=Vector3(gyro_x, gyro_y, gyro_z),
        angular_velocity_covariance=[.03**2,0,0, 0,.03**2,0, 0,0,.03**2], # XXX
        linear_acceleration=Vector3(acc_x, acc_y, acc_z),
        linear_acceleration_covariance=[.02**2,0,0, 0,.02**2,0, 0,0,.02**2], # XXX
    ))

    # Publish magnetic field vector
    mag_pub.publish(MagneticField(
        header=Header(
            stamp=now,
            frame_id=frame_id,
        ),
        magnetic_field=Vector3(mag_x, mag_y, mag_z),
    ))

while not rospy.is_shutdown():

  now = rospy.Time.now()

  line = s.readline()
  line = line.replace("$","")
  line = line.replace("#","")
  line = line.replace("\r","")
  words = line.replace("\n","")
  #words = string.split(words,",")

  handle_line(words, now)