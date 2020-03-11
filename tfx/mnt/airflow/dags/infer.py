from typing import Any, Text 

def preprocessing_fn(inputs):
    """tf.transform's callback function for preprocessing inputs.

    Args:
    inputs: map from feature keys to raw not-yet-transformed features.

     Returns:
     Map from string feature key to transformed feature operations.
    """
    outputs = {}


    """'PassengerId', 'Survived', 'Pclass'"""

    outputs['PassengerId'] = inputs['PassengerId']
    outputs['Survived'] = inputs['Survived'] # label
    outputs['Pclass'] = inputs['Pclass']

    print(f'==============={inputs}')

    print(f'DEBUG OUT: {outputs}')
    return outputs



import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.estimator import model_to_estimator

import tensorflow_transform as tft


def _input_fn(filenames, transform_output):

    transform_feature_spec = (transform_output.transformed_feature_spec().copy())

    dataset = tf.data.experimental.make_batched_features_dataset(filenames, 20, transform_feature_spec)

    return dataset
    

def trainer_fn(trainer_fn_args, schema):


    TRAIN_BATCH_SIZE=20

    tf_transform_output = tft.TFTransformOutput(trainer_fn_args.transform_output)

    
    # get dataset 
    model = Sequential(
        [
            layers.Dense(100),
            layers.Dense(2, activation='sigmoid')
        ]
    )


    model.compile(
        optimizer='adam',
        loss='SGD',
        metrics=['accuracy', 'mse']
    )
    # fit model

    estimator = model_to_estimator(model)

    # Creating train Specification

    train_spec = tf.estimator.TrainSpec(
        _input_fn,
        max_steps=trainer_fn_args.train_steps
    )

    # Create a train function

    train_input_fn = lambda : _input_fn(
        trainer_fn_args.train_files,
        tf_transform_output
    )

    train_spec = tf.estimator.TrainSpec(
        train_input_fn,
        max_steps=trainer_fn_args.train_steps
    )

    # Create a eval function

    eval_input_fn = lambda : _input_fn(
        trainer_fn_args.eval_files,
        tf_transform_output,
        batch_size=TRAIN_BATCH_SIZE
    )

    eval_spec = tf.estimator.EvalSpec(
        eval_input_fn,
        steps=trainer_fn_args.eval_steps
    )
    return {
        'estimator' :  estimator,
        'train_spec' : train_spec,
        'eval_spec' : eval_spec
    }
