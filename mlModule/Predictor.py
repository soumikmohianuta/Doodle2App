from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
from datetime import datetime
import os
import tensorflow as tf

import numpy as np
import json
#APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#output_directory = os.path.join(APP_ROOT,'compressedOut')
#export_dir = os.path.join(APP_ROOT,'compressedOut','tb')
num_layers=3
num_nodes=128
num_classes = 20
dropout=0.3
steps=100000
batch_size=2
tfrecord_file = "predict1"

class_names= ['back','camera','cancel','circle','envelope','forward','hamburger','leftarrow'
                 ,'play','plus','search','settings','share','square','star']
#tf.enable_eager_execution()
class Predictor:  
    def __init__(self, export_dir, output_directory):
        self.export_dir = export_dir
        self.output_directory = output_directory
        self.loadPredictor()
        
        
    def parse_features(self,stoke_data):
            """Parse provided stroke data and ink (as np array) and classname."""
            inkarray = json.loads(stoke_data)
            stroke_lengths = [len(stroke[0]) for stroke in inkarray]
            total_points = sum(stroke_lengths)
            np_ink = np.zeros((total_points, 3), dtype=np.float32)
            current_t = 0
            for stroke in inkarray:
                if len(stroke[0]) != len(stroke[1]):
                    print("Inconsistent number of x and y coordinates.")
                    return None
                for i in [0, 1]:
                    np_ink[current_t:(current_t + len(stroke[0])), i] = stroke[i]
                current_t += len(stroke[0])
                np_ink[current_t - 1, 2] = 1  # stroke_end
        # Preprocessing.
        # 1. Size normalization.
            lower = np.min(np_ink[:, 0:2], axis=0)
            upper = np.max(np_ink[:, 0:2], axis=0)
            scale = upper - lower
            scale[scale == 0] = 1
            np_ink[:, 0:2] = (np_ink[:, 0:2] - lower) / scale
            
            np_ink[1:, 0:2] -= np_ink[0:-1, 0:2]
#            print(np_ink)
            np_ink = np_ink[1:, :]
#            return ([np_ink.flatten().tolist(),np_ink.flatten().tolist()],[np_ink.shape[0],np_ink.shape[0]])
            np_ink_flatten = np_ink.flatten()
            
#            self.shapeConstant = tf.constant([list(np_ink.shape),list(np_ink.shape)])
            return ([list(np_ink.shape),list(np_ink.shape)],[np_ink_flatten.tolist(),np_ink_flatten.tolist()])


        
    def example_input_fn(self, generator):
        """ An example input function to pass to predict. It must take a generator as input """

        def _inner_input_fn():
#            dataset = tf.data.Dataset.from_generator(generator, output_types=(tf.int32, tf.float32)).batch(1)
            dataset = tf.data.Dataset.from_generator(generator, (tf.int32, tf.float32),(tf.TensorShape([None, 2]), tf.TensorShape(None))).batch(1)
            iterator = dataset.make_one_shot_iterator()
            features = iterator.get_next()
            return features, None

        return _inner_input_fn
    


    def _get_input_tensors(self, features, labels):

        shapes = features[0]
        shapes = tf.reshape(shapes,[batch_size,-1])
        print(shapes.shape)
#        shapes = tf.constant([[257, 3], [257, 3]])
        # lengths will be [batch_size]

        inks = tf.reshape(features[1], [batch_size, -1, 3])
        lengths = tf.squeeze(
                tf.slice(shapes, begin=[0, 0], size=[batch_size, 1]))
        if labels is not None:
            labels = tf.squeeze(labels)
        return inks, lengths, labels



    def _add_regular_rnn_layers(self, convolved, lengths):
        """Adds RNN layers."""

        cell = tf.nn.rnn_cell.BasicLSTMCell

        cells_fw = [cell(num_nodes) for _ in range(num_layers)]
        cells_bw = [cell(num_nodes) for _ in range(num_layers)]
        if dropout > 0.0:
            cells_fw = [tf.contrib.rnn.DropoutWrapper(cell) for cell in cells_fw]
            cells_bw = [tf.contrib.rnn.DropoutWrapper(cell) for cell in cells_bw]
        outputs, _, _ = tf.contrib.rnn.stack_bidirectional_dynamic_rnn(
                cells_fw=cells_fw,
                cells_bw=cells_bw,
                inputs=convolved,
                sequence_length=lengths,
                dtype=tf.float32,
                scope="rnn_classification")
        return outputs



    def _add_rnn_layers(self, convolved, lengths):

        outputs = self._add_regular_rnn_layers(convolved, lengths)

    # outputs is [batch_size, L, N] where L is the maximal sequence length and N
    # the number of nodes in the last layer.
        mask = tf.tile(
                tf.expand_dims(tf.sequence_mask(lengths, tf.shape(outputs)[1]), 2),
                [1, 1, tf.shape(outputs)[2]])
        zero_outside = tf.where(mask, outputs, tf.zeros_like(outputs))
        outputs = tf.reduce_sum(zero_outside, axis=1)
        return outputs

    
    def model_fn(self, features, labels, mode):

      inks, lengths, _labels = self._get_input_tensors(features, labels)
#      print(lengths.shape)
#      print(inks.shape)
  
  
      """Adds convolution layers."""  
  
      with tf.name_scope('conv1d_1'):  
          convolved1 = tf.layers.conv1d(
                  inks,
                  filters=48,
                  kernel_size=5,
                  activation=None,
                  strides=1,
                  padding="same",
                  name="conv1d_1")

      with tf.name_scope('conv1d_2'):  
          convolved2 = tf.layers.conv1d(
                  convolved1,
                  filters=64,
                  kernel_size=5,
                  activation=None,
                  strides=1,
                  padding="same",
                  name="conv1d_2")

      with tf.name_scope('conv1d_3'):  
          convolved3 = tf.layers.conv1d(
                  convolved2,
                  filters=96,
                  kernel_size=3,
                  activation=None,
                  strides=1,
                  padding="same",
                  name="conv1d_3")

      final_state = self._add_rnn_layers(convolved3, lengths)
      with tf.name_scope('Final_Layer'):   
          logits = tf.layers.dense(inputs=final_state, units=num_classes, name= 'Final_Layer')
     
 
      predictions = {
              # Generate predictions (for PREDICT and EVAL mode)
              "classes": tf.argmax(input=logits, axis=1),
              # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
              # `logging_hook`.
              "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
              }   
      if mode == tf.estimator.ModeKeys.PREDICT:
          return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

      loss = tf.reduce_mean(
              tf.nn.sparse_softmax_cross_entropy_with_logits(
                      labels=_labels, logits=logits))
      # Configure the Training Op (for TRAIN mode)
      if mode == tf.estimator.ModeKeys.TRAIN:
          optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
          train_op = optimizer.minimize(
                  loss=loss,
                  global_step=tf.train.get_global_step())
          return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

      # Add evaluation metrics (for EVAL mode)
      eval_metric_ops = {
              "accuracy": tf.metrics.accuracy(
                      labels=labels, predictions=predictions["classes"])}
      return tf.estimator.EstimatorSpec(
              mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)
    
 
    def eval_input_fn(self, features, labels, batch_size):
        features=dict(features)
        if labels is None:
            inputs = features
        else:
            inputs = (features, labels)
        dataset = tf.data.Dataset.from_tensor_slices(inputs)

        dataset = dataset.batch(batch_size)
        return dataset
    
    def predict(self, predict_for_data):
      """Creates an Experiment configuration based on the estimator and input fn."""
#      self.create_tfrecord_for_prediction(predict_for_data)
      
      config = tf.estimator.RunConfig()
      config = config.replace(model_dir=self.export_dir)
      estimator = self.classifier
      features = self.parse_features(predict_for_data)
      print(features["shape"])
      predict_input_fn = tf.estimator.inputs.numpy_input_fn(
              x=features, shuffle=False)
      result = estimator.predict(input_fn=predict_input_fn)
      print(result)
      for r in result:
        print(r)


 
    def loadPredictor(self):
        self.classifier = tf.estimator.Estimator(
                model_fn=self.model_fn,
                model_dir=os.path.join(self.output_directory, "tb"))

