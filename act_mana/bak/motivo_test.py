# 添加metamotivo到Python路径
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from packaging.version import Version
from metamotivo.fb_cpr.huggingface import FBcprModel
from humenv import make_humenv
import gymnasium
from gymnasium.wrappers import FlattenObservation, TransformObservation
import torch
import math
import cv2
import numpy as np


device = 'cpu'

if Version('0.26') <= Version(gymnasium.__version__) < Version('1.0'):
    transform_obs_wrapper = lambda env: TransformObservation(
            env, lambda obs: torch.tensor(obs.reshape(1, -1), dtype=torch.float32, device=device)
        )
else:
    transform_obs_wrapper = lambda env: TransformObservation(
            env, lambda obs: torch.tensor(obs.reshape(1, -1), dtype=torch.float32, device=device), env.observation_space
        )

env, _ = make_humenv(
    num_envs=1,
    wrappers=[
        FlattenObservation,
        transform_obs_wrapper,
    ],
    state_init='Default',
)
observation, _ = env.reset()

model = FBcprModel.from_pretrained('/home/xl/Downloads/models/metamotivo-M-1')
# print(model)
model.to(device)
z = model.sample_z(1)
print(f'embedding size {z.shape}')
print(f'z norm: {torch.norm(z)}')
print(f'z norm / sqrt(d): {torch.norm(z) / math.sqrt(z.shape[-1])}')


frames = [env.render()]
for i in range(30):
    action = model.act(observation, z, mean=True)
    observation, reward, terminated, truncated, info = env.step(action.cpu().numpy().ravel())
    frames.append(env.render())

env.close()

# media.show_video(frames, fps=30)
import cv2  
for i, frame in enumerate(frames):
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(f'frames/frame_{i:04d}.png'), frame_bgr)

print(f'====== Saved {len(frames)} frames to frames/======')
