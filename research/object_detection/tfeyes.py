import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

if tf.__version__ < '1.4.0':
    raise ImportError(
        'Please upgrade your tensorflow installation to v1.4.* or later!')


# ## Env setup

# ## Object detection imports
# Here are the imports from the object detection module.

sys.path.append("..")
from utils import label_map_util
from utils import visualization_utils as vis_util


print("Model preparation")
# ## Variables
#
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.
#
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.


# What model to download.
MODEL_NAME = 'training_output'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
LABELS_PBTXT = 'object-detection.pbtxt'
NUM_CLASSES = 2
PATH_TO_LABELS = os.path.join('data', LABELS_PBTXT)


print("Load a (frozen) Tensorflow model into memory.")
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


print("Loading label map")
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

import cv2
from mss import mss
from PIL import Image
import pyautogui
import re

def process_label(label):
    try:
        pattern = r'(.+): ([0-9]+)%'
        result = re.search(pattern, label)
        groups = result.groups()
        if type(groups) == tuple and len(groups) == 2:
            return groups
    except Exception as e:
        #print("Returning None: ", e)
        pass
    return (None, None)

class TFEyes:
    def __init__(self):
        self.data_points = []
        self.do_print = False
        self.do_live_view = False

    def process_labelled_boxes(self, labelled_boxes, orig_size):
        #print(labelled_boxes)
        fx, fy = orig_size
        self.data_points = []
        for box, label in labelled_boxes.items():
            ymin, xmin, ymax, xmax = box
            midpoint = (round(fx * (xmax + xmin) / 2), round(fy * (ymax + ymin) / 2))
            name, confidence = process_label(label[0])
            self.data_points += [((name, confidence), midpoint)]

        if self.do_print:
            print(self.data_points)
            print("Mouse position: {}".format(pyautogui.position()))

    def start_watching(self):
        with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:
                with mss() as sct:
                    while (True):
                        try:
                            sct_img = sct.grab(sct.monitors[0]) 
                            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
                            image_np = np.array(img)
            
                            # Definite input and output Tensors for detection_graph
                            image_tensor = detection_graph.get_tensor_by_name(
                                'image_tensor:0')
                            # Each box represents a part of the image where a particular object was detected.
                            detection_boxes = detection_graph.get_tensor_by_name(
                                'detection_boxes:0')
                            # Each score represent how level of confidence for each of the objects.
                            # Score is shown on the result image, together with the class label.
                            detection_scores = detection_graph.get_tensor_by_name(
                                'detection_scores:0')
                            detection_classes = detection_graph.get_tensor_by_name(
                                'detection_classes:0')
                            num_detections = detection_graph.get_tensor_by_name(
                                'num_detections:0')
                            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                            image_np_expanded = np.expand_dims(image_np, axis=0)
                            # Actual detection.
                            (boxes, scores, classes, num) = sess.run(
                                [detection_boxes, detection_scores,
                                    detection_classes, num_detections],
                                feed_dict={image_tensor: image_np_expanded})
                            # Visualization of the results of a detection.
                            box_limit = 4
                            labelled_boxes = {}
                            vis_util.visualize_boxes_and_labels_on_image_array(
                                image_np,
                                np.squeeze(boxes),
                                np.squeeze(classes).astype(np.int32),
                                np.squeeze(scores),
                                category_index,
                                max_boxes_to_draw=box_limit, ###
                                box_str_dict_ref=labelled_boxes, ###
                                use_normalized_coordinates=True,
                                line_thickness=8)
                            self.process_labelled_boxes(labelled_boxes, img.size)
                            
                            if self.do_live_view:
                                shrink_factor = 0.5
                                display_image = image_np
                                display_image = cv2.resize(display_image, None, fx=shrink_factor, fy=shrink_factor)
                                display_image = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
                                cv2.imshow('live_detection', display_image)
                                if cv2.waitKey(25) & 0xFF == ord('q'):
                                    break
                                    cv2.destroyAllWindows()
                                    cap.release()
                        except KeyboardInterrupt as e:
                            import code; code.interact(local=dict(globals(), **locals()))

if __name__ == "__main__":
    my_eyes = TFEyes()
    my_eyes.do_live_view = True
    my_eyes.do_print = True
    my_eyes.start_watching()