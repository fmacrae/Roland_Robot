# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Simple image classification with Inception.
Run image classification with Inception trained on ImageNet 2012 Challenge data
set.
This program creates a graph from a saved GraphDef protocol buffer,
and runs inference on an input JPEG image. It outputs human readable
strings of the top 5 predictions along with their probabilities.
Change the --image_file argument to any jpg image to compute a
classification of that image.
Please see the tutorial and website for a detailed description of how
to use this script to perform image recognition.
https://tensorflow.org/tutorials/image_recognition/
This file has been modified by Sam Abrahams to print out basic run-time
information. These modifications have been surrounded with the comments:
"MODIFICATION BY SAM ABRAHAMS" and "END OF MODIFICATION"
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from shutil import copyfile
from Adafruit_LSM303 import Adafruit_LSM303
import os.path
import re
import sys
import tarfile

# MODIFICATION BY SAM ABRAHAMS
import time
# END OF MODIFICATION

import numpy as np
from six.moves import urllib
import tensorflow as tf

# for dumping properly
import datetime
import json

import subprocess

def do(cmd):
  print(cmd)
  p =subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  for line in p.stdout.readlines():
    print(line)
    retval = p.wait()


FLAGS = tf.app.flags.FLAGS

# classify_image_graph_def.pb:
#   Binary representation of the GraphDef protocol buffer.
# imagenet_synset_to_human_label_map.txt:
#   Map from synset ID to a human readable string.
# imagenet_2012_challenge_label_map_proto.pbtxt:
#   Text representation of a protocol buffer mapping a label to synset ID.
tf.app.flags.DEFINE_string(
    'model_dir', '/tmp/imagenet',
    """Path to classify_image_graph_def.pb, """
    """imagenet_synset_to_human_label_map.txt, and """
    """imagenet_2012_challenge_label_map_proto.pbtxt.""")
tf.app.flags.DEFINE_string('image_file', '',
                           """Absolute path to image file.""")
tf.app.flags.DEFINE_integer('num_top_predictions', 5,
                            """Display this many predictions.""")
# MODIFICATION BY SAM ABRAHAMS
tf.app.flags.DEFINE_integer('warmup_runs', 10,
                            "Number of times to run Session before starting test")
tf.app.flags.DEFINE_integer('num_runs', 25,
                            "Number of sample runs to collect benchmark statistics")
# END OF MODIFICATION

# pylint: disable=line-too-long
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
# pylint: enable=line-too-long


class NodeLookup(object):
  """Converts integer node ID's to human readable labels."""

  def __init__(self,
               label_lookup_path=None,
               uid_lookup_path=None):
    if not label_lookup_path:
      label_lookup_path = os.path.join(
          FLAGS.model_dir, 'imagenet_2012_challenge_label_map_proto.pbtxt')
    if not uid_lookup_path:
      uid_lookup_path = os.path.join(
          FLAGS.model_dir, 'imagenet_synset_to_human_label_map.txt')
    self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

  def load(self, label_lookup_path, uid_lookup_path):
    """Loads a human readable English name for each softmax node.
    Args:
      label_lookup_path: string UID to integer node ID.
      uid_lookup_path: string UID to human-readable string.
    Returns:
      dict from integer node ID to human-readable string.
    """
    if not tf.gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)
    if not tf.gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)

    # Loads mapping from string UID to human-readable string
    proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in proto_as_ascii_lines:
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string

    # Loads mapping from string UID to integer node ID.
    node_id_to_uid = {}
    proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]

    # Loads the final mapping of integer node ID to human-readable string
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      name = uid_to_human[val]
      node_id_to_name[key] = name

    return node_id_to_name

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]


def create_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  # Creates graph from saved graph_def.pb.
  with tf.gfile.FastGFile(os.path.join(
      FLAGS.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(image):
  """Runs inference on an image.
  Args:
    image: Image file name.
  Returns:
    Nothing
  """
  if not tf.gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)
  image_data = tf.gfile.FastGFile(image, 'rb').read()


  #find out the directory to log to
  with open('run_data_directory.txt') as f:
    sLogDir=f.read()
  sLogDir=sLogDir.rstrip()

  # Creates graph from saved GraphDef.
  start_time = time.time()
  create_graph()
  graph_time = time.time() - start_time

  node_lookup = NodeLookup()
  with tf.Session() as sess:
    # Some useful tensors:
    # 'softmax:0': A tensor containing the normalized prediction across
    #   1000 labels.
    # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
    #   float description of the image.
    # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
    #   encoding of the image.
    # Runs the softmax tensor by feeding the image_data as input to the graph.
    softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
    # MODIFICATION BY SAM ABRAHAMS
    image_data = tf.gfile.FastGFile(image, 'rb').read()
    for i in range(FLAGS.warmup_runs):
      predictions = sess.run(softmax_tensor,
                             {'DecodeJpeg/contents:0': image_data})
    runs = []
    # object we will dump to json for analysis
    results_list = []
    # store all the things roland has seen (i.e top inception result)
    things_roland_has_seen = []
    # after every inception result, find the size of the set of 
    # things roland has seen
    num_unique_things_roland_has_seen = []
    # if roland hasn't seen anything new this time, counter will go up
    num_times_not_seen_anything_new = 0
    # if roland has seen anything new this number of times he wants to stop
    max_num_times_not_seen_anything_new = 20
    #create connection to the compass
    oOrientation = Adafruit_LSM303()
    inception_file = open(sLogDir+'Observations.txt', 'w')
    for i in range(FLAGS.num_runs):
      start_time = time.time()
      curOrientation = oOrientation.read()  
      timestr = time.strftime("%Y%m%d-%H%M%S")

      copyfile('/dev/shm/mjpeg/cam.jpg',sLogDir+timestr+'.jpg')
      if not tf.gfile.Exists(image):
        tf.logging.fatal('File does not exist %s', image)
      image_data = tf.gfile.FastGFile(image, 'rb').read()
      predictions = sess.run(softmax_tensor,
                             {'DecodeJpeg/contents:0': image_data})
      predictions = np.squeeze(predictions)
      top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
      counter=0

      human_strings = []
      probabilities = []

      for node_id in top_k:
        human_string = node_lookup.id_to_string(node_id)
        score = predictions[node_id]

        human_strings.append(human_string)
        probabilities.append(float(score))

        print('%s (score = %.5f)' % (human_string, score))
        print(curOrientation)
        inception_file.write(str(human_string)+'\n')
        inception_file.write(str(score)+'\n')
        inception_file.write(str(curOrientation))
        inception_file.write('\n')
        inception_file.write(sLogDir+timestr+'.jpg\n')

        if counter == 0:
          do('echo "I think I see ah '+human_string+'" | flite -voice slt')
          counter = 2
          

          # have I been here before?
	  things_roland_has_seen.append(human_string)
	  num_unique_things_roland_has_seen.append(len(set(things_roland_has_seen)))
	  
          print('Have seen %.1f unique things this run' % num_unique_things_roland_has_seen[-1]) 
          
          if (len(num_unique_things_roland_has_seen) > 2 and
              num_unique_things_roland_has_seen[-1] == num_unique_things_roland_has_seen[-2]):
              num_times_not_seen_anything_new = num_times_not_seen_anything_new + 1    	  
              print('Have not seen anything new %.1f times' % num_times_not_seen_anything_new)
          if num_times_not_seen_anything_new > max_num_times_not_seen_anything_new:
	          do('echo "I can not see anything new please disable me" | flite -voice slt')
          if num_times_not_seen_anything_new > 2*max_num_times_not_seen_anything_new:
              do('echo "Please I am so bored kill me now" | flite -voice slt')

      results_list.append({'human_strings': human_strings, 'probabilities':probabilities})
      
      runs.append(time.time() - start_time)
    for i, run in enumerate(runs):
      print('Run %03d:\t%0.4f seconds' % (i, run))
    print('---')
    print('Best run: %0.4f' % min(runs))
    print('Worst run: %0.4f' % max(runs))
    print('Average run: %0.4f' % float(sum(runs) / len(runs)))
    print('Build graph time: %0.4f' % graph_time)
    print('Number of warmup runs: %d' % FLAGS.warmup_runs)
    print('Number of test runs: %d' % FLAGS.num_runs)
    #print(results_list)
    with open('dump.json', 'w') as f:
        json.dump(results_list, f)

    # END OF MODIFICATION

def maybe_download_and_extract():
  """Download and extract model tar file."""
  dest_directory = FLAGS.model_dir
  if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)
  filename = DATA_URL.split('/')[-1]
  filepath = os.path.join(dest_directory, filename)
  if not os.path.exists(filepath):
    def _progress(count, block_size, total_size):
      sys.stdout.write('\r>> Downloading %s %.1f%%' % (
          filename, float(count * block_size) / float(total_size) * 100.0))
      sys.stdout.flush()
    filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath,
                                             reporthook=_progress)
    print()
    statinfo = os.stat(filepath)
    print('Succesfully downloaded', filename, statinfo.st_size, 'bytes.')
  tarfile.open(filepath, 'r:gz').extractall(dest_directory)


def main(_):
  maybe_download_and_extract()
  image = (FLAGS.image_file if FLAGS.image_file else
           os.path.join(FLAGS.model_dir, 'cropped_panda.jpg'))
  run_inference_on_image(image)


if __name__ == '__main__':
  tf.app.run()

