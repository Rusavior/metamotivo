import base64
from PIL import Image
import io
import os
import sys
import numpy as np
import torch
import cv2
import math

# 添加metamotivo到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from packaging.version import Version
import gymnasium
from gymnasium.wrappers import FlattenObservation, TransformObservation
from humenv import make_humenv
from metamotivo.fb_cpr.huggingface import FBcprModel

class MotivoHandler:
    def __init__(self):
        self.device = 'cpu'
        self.env = None
        # init gymnasium TransformObservation 
        if Version('0.26') <= Version(gymnasium.__version__) < Version('1.0'):
            self.transform_obs_wrapper = lambda env: TransformObservation(
                env, lambda obs: torch.tensor(obs.reshape(1, -1), dtype=torch.float32, device=self.device)
            )
        else:
            self.transform_obs_wrapper = lambda env: TransformObservation(
                env, lambda obs: torch.tensor(obs.reshape(1, -1), dtype=torch.float32, device=self.device), 
                env.observation_space
            )
        self.model = FBcprModel.from_pretrained('/home/xl/Downloads/models/metamotivo-M-1')
        self.model.to(self.device)
        
    def process_step(self, step_text, frame_callback=None):
        try:
            print('Processing step:', step_text)

            # init env and model
            self.env, _ = make_humenv(
                num_envs=1,
                wrappers=[
                    FlattenObservation,
                    self.transform_obs_wrapper,
                ],
                state_init='Default',
            )
            observation, _ = self.env.reset()
            z = self.model.sample_z(1)         

            # action inference and gen image stream
            for i in range(31):
                frame = self.env.render()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                action = self.model.act(observation, z, mean=True)
                observation, reward, terminated, truncated, info = self.env.step(action.cpu().numpy().ravel())
                
                _, buffer = cv2.imencode('.png', frame)
                img_str = base64.b64encode(buffer).decode()
                yield img_str
                
        except Exception as e:
            print(f'Error in process_step: {str(e)}')
    
    def __del__(self):
        if hasattr(self, 'env'):
            self.env.close()


if __name__=='__main__':
    motivo_handler = MotivoHandler()
    print('ok')