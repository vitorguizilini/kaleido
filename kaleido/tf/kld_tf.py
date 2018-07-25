
import numpy as np
import tensorflow as tf
import kaleido as kld

### SESSION
def Session():
    return tf.Session()

### SHAPE
def shape( tensor ):
    shape1 , shape2 = tensor.get_shape().as_list() , tf.shape( tensor )
    for i in range( len( shape1 ) ):
        if shape1[i] is None: shape1[i] = shape2[i]
    return shape1

### NUM TRAINABLE PARAMS
def num_trainable_params():
    return np.sum( [ np.prod( v.get_shape().as_list() ) for v in tf.trainable_variables() ] )

### ALL TENSORS
def all_tensors():
    return [ n for n in tf.get_default_graph().as_graph_def().node ]

### PRINT ALL TENSOR NAMES
def print_all_tensor_names():
    tensors = all_tensors()
    for t in tensors: print( t.name )

### GLOBAL VARS
def global_vars( scope = None ):
    return tf.get_collection( tf.GraphKeys.GLOBAL_VARIABLES , scope = scope )

### TRAINABLE VARS
def trainable_vars( scope = None ):
    return tf.get_collection( tf.GraphKeys.TRAINABLE_VARIABLES , scope = scope )

### UPDATE OPS
def update_ops():
    return tf.get_collection( tf.GraphKeys.UPDATE_OPS )

### INIT_OP
def init_op( vars = None ):
    if vars is None: return tf.global_variables_initializer()
    else: return tf.variables_initializer( vars )

### INITIALIZE
def initialize( sess = None , vars = None ):
    if sess is None: sess = tf.Session()
    sess.run( init_op( vars ) )
    return sess


