from info import *
import os
from subprocess import call
import argparse


parser = argparse.ArgumentParser('ROI detection process!')
parser.add_argument('--video_id', type=str, default=None, required=True, help='Absolute path file with video id and paths')
parser.add_argument('--roi_seed', type=int, nargs=2, default=None, help='Seed to found ROI')
parser.add_argument('--cuda_path', default='/usr/local/cuda-11.3/lib64', type=str, help='device for training')
args = parser.parse_args()

vids = load_ids_and_paths(args.video_id)

################################################################################
print('Going to extract mean image for single scenes!')
for vid in vids:
    print('Extracting mean background model for scene:', vid['name'])
    call(['python', '/content/PersonGONE/utils/bckg_subtraction.py',
          os.path.join(inpainting_path, vid['name'], vid['name']+'.mp4'),
          os.path.join(mean_scenes_path, vid['name']+'.jpg')]
          )
################################################################################


################################################################################
print('Going to detect ROI')
for vid in vids:
    print('Detecting ROI for scene:', vid['name'])
    call(['python', '/content/PersonGONE/utils/detect_tray.py',
          '--mean_path', os.path.join(mean_scenes_path, vid['name']+'.jpg'),
          '--out_path', os.path.join(rois_path, vid['name']+'.json')])
################################################################################

