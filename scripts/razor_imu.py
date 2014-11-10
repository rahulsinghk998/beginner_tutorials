__author__ = 'andy'

#!/usr/bin/python

import roslib
roslib.load_manifest('razor_imu')
import rospy
from std_msgs.msg import Header, String
from geometry_msgs.msg import Quaternion, Vector3
from sensor_msgs.msg import Imu, MagneticField

import traceback
import math

import numpy
import serial

g0 = 9.80665				# Gravity constant

# Init ros
rospy.init_node('razor_imu')

# Get some parameters
frame_id = rospy.get_param('~frame_id', '/imu')		# This is the frame in which the imu exist default /imu
port = rospy.get_param('~port', '/dev/razorimu')		# This is the serial port for the imu device default /dev/imu

# Open the serial port w/ baud rate of 57600
s = serial.Serial(port, 57600)

# Setup publishers (Purpose of each explained above)
pub = rospy.Publisher('/imu/data_raw', Imu)
mag_pub = rospy.Publisher('/imu/mag_raw', MagneticField)
raw_pub = rospy.Publisher('/imu/raw', String)

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

        # Parse out the data
        const_P_colon, timestamp, const_mp, mag_x, mag_y, mag_z, const_ap, acc_x, acc_y, acc_z, const_gp, gyro_x, gyro_y, gyro_z = data.split(',')

	# Check to make sure we parsed correctly
        assert const_P_colon == 'P:'
        assert const_mp == 'mp'
        assert const_ap == 'ap'
        assert const_gp == 'gp'

	# Convert to floating points
        timestamp, mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = map(float, [timestamp, mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z])

    # Catch all exceptions
    except Exception:
        print repr(data)
        traceback.print_exc()
        return

    # Scale the data
    mag_x, mag_y, mag_z = [1e-7 * x for x in [mag_x, mag_y, mag_z]]
    acc_x, acc_y, acc_z = [-1e-3 * g0 * x for x in [acc_x, acc_y, acc_z]]
    gyro_x, gyro_y, gyro_z = [110.447762 * x for x in [gyro_x, gyro_y, gyro_z]]

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



tmpdata = ''
while not rospy.is_shutdown():
    # Get the size of the input buffer
    waiting = s.inWaiting()
    # Get current time
    now = rospy.Time.now()
    # Read all data on input buffer
    tmpdata += s.read(waiting) 		# blocking seems to break things, strangely
    # Break up based on new lines
    x = tmpdata.split('\n')
    # Access The last element in X so throw away any data that came prior
    tmpdata = x[-1]
    #Handel data
    for data in x[:-1]:
        handle_line(data, now)