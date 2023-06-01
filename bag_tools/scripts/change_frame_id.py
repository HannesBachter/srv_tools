#!/usr/bin/python
"""
Copyright (c) 2012,
Systems, Robotics and Vision Group
University of the Balearican Islands
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Systems, Robotics and Vision Group, University of
      the Balearican Islands nor the names of its contributors may be used to
      endorse or promote products derived from this software without specific
      prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


PKG = 'bag_tools' # this package name

import roslib; roslib.load_manifest(PKG)
import rospy
import rosbag
import argparse

def change_frame_id(inbag_file, outbag_file, frame_id, topics):
  rospy.loginfo('   Processing input bagfile: %s', inbag_file)
  rospy.loginfo('  Writing to output bagfile: %s', outbag_file)
  rospy.loginfo('            Changing topics: %s', topics)
  rospy.loginfo('           Writing frame_id: %s', frame_id)

  outbag = rosbag.Bag(outbag_file, 'w')

  for topic, msg, t in rosbag.Bag(inbag_file,'r').read_messages():
    if topic in topics:
      if msg._has_header:
        msg.header.frame_id = frame_id
    outbag.write(topic, msg, t)
  rospy.loginfo('Closing output bagfile and exit...')
  outbag.close()

if __name__ == "__main__":

  '''
  CALL : python change_frame_id.py -i path/to/in/bagfile -o path/to/out/bagfile -f desired_frame_id -t topic_to_change1 topic_to_change2 topic_to_change3 ...

  '''

  rospy.init_node('change_frame_id')
  parser = argparse.ArgumentParser(
      description='Create a new bagfile from an existing one replacing the frame id of requested topics.')
  parser.add_argument('-o', metavar='OUTPUT_BAGFILE', required=True, help='output bagfile')
  parser.add_argument('-i', metavar='INPUT_BAGFILE', required=True, help='input bagfile')
  parser.add_argument('-f', metavar='FRAME_ID', required=True, help='desired frame_id name in the topics')
  parser.add_argument('-t', metavar='TOPIC', required=True, help='topic(s) to change', nargs='+')
  args = parser.parse_args()

  try:
    change_frame_id(args.i,args.o,args.f,args.t)
  except Exception:
    import traceback
    traceback.print_exc()
