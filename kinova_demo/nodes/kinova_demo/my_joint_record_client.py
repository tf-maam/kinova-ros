#! /usr/bin/env python3
"""A test program to test action servers for the JACO and MICO arms."""

import roslib; roslib.load_manifest('kinova_demo')

import rospy

import simpleaudio as sa

import time
import os

from kinova_msgs.srv import *
from robot_control_modules import *

prefix = 'j2s7s300_'
nbJoints = 7
interactive = True
duration_sec = 100



def beep():
    filename = '/'.join(os.path.realpath(__file__).split('/')[:-1]) + '/beep-01a.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing



def initiate_subscriber(prefix_):
    # wait to get current position
    topic_address = '/' + prefix_ + 'driver/out/joint_state'
    rospy.Subscriber(topic_address, kinova_msgs.msg.JointAngles, log_current_joint_angle)
    rospy.wait_for_message(topic_address, kinova_msgs.msg.JointAngles)
    print('position listener obtained message for joint position. ')


def log_current_joint_angle(feedback):
    global joint_command_history
    

    currentJointCommand_str_list = str(feedback).split("\n")
    for index in range(0,len(currentJointCommand_str_list)):
        temp_str=currentJointCommand_str_list[index].split(": ")
        currentJointCommand[index] = float(temp_str[1])


    now = rospy.get_rostime()
    #rospy.loginfo("Current time %i %i", now.secs, now.nsecs)

    print('currentJointCommand is: ')
    print(currentJointCommand, 'at ', now.nsecs, 'nanosecs')
    
    joint_command_history.append([now.nsecs] + currentJointCommand)


joint_state_history = []

if __name__ == '__main__':
    
    joint_positions = []
    try:        
        prefix, nbJoints = argumentParser(None)
        rospy.init_node('my_joint_record_client')
    
        if (interactive == True):
            nb = input('Enter the number of joint positions')
            joints_num = int(nb)
            print(('Setting torques to zero.\n' +
                  'When three signal beeps are made,' +
                  ' you can define the next joint after 10 s.\n'+
                  ' the record is represented by one beep and every 5 sec another redcord is signalised.'))
            time.sleep(10)
            beep()
            beep()
            beep()
            #ZeroTorque(prefix)
            #publishTorqueCmd([0,0,0,0,0,0,0], duration_sec, prefix)
            
            
            
            for i in range(joints_num):    
                print("write another joint")
                beep()
    
        print("Done!")
    except rospy.ROSInterruptException:
        print("program interrupted before completion")
