import json
import sagemaker
import os
from s3_conx import *
from sagemaker.pytorch import PyTorch

def iterate_to_s3(path):
    if os.path.isdir(path):
        for _dir in os.listdir(path):
            iterate_to_s3(path+_dir)
    else:
        s3.upload_file_to_s3(path)
    return

if __name__ == '__main__':
    # Initializes SageMaker session which holds context data
    sagemaker_session = sagemaker.Session()
    role = sagemaker_session.get_caller_identity_arn()
    
    local_path = 'checkpoints'
    estimator = PyTorch(
      # name of the runnable script containing __main__ function (entrypoint)
      entry_point='train.py',
      # path of the folder containing training code. It could also contain a
      # requirements.txt file with all the dependencies that needs
      # to be installed before running
      source_dir='.',
      framework_version='1.5.0',
      train_instance_count=1,
      train_instance_type='ml.p2.xlarge',
       #train_instance_type='ml.m4.xlarge', 
      role=role,
        checkpoint_local_path = local_path+'/',
      # these hyperparameters are passed to the main script as arguments and 
      # can be overridden when fine tuning the algorithm
      hyperparameters={
      'n_epochs': 200 ,
          'n_epochs_decay': 1000,
          'lr':0.0002,
          'dataroot':'datasets/olracle/train',
          'checkpoints_dir':'checkpoints',
          'name':'olracle-pix2pix',
          'model':'pix2pix',
          'print_freq':480,
          'display_freq':480,
          'input_nc':1,
          'output_nc':1,
          'num_threads':0,
          'dataset_mode':'aligned',
          'save_epoch_freq':50,
      'batch_size': 4,
      })
    estimator.fit()