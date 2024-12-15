from humenv import make_humenv
from gymnasium.wrappers import FlattenObservation, TransformObservation
import torch
from metamotivo.fb_cpr.huggingface import FBcprModel
import mediapy
import cv2

device = "cpu"
env, _ = make_humenv(
    num_envs=1,
    wrappers=[
        FlattenObservation,
        lambda env: TransformObservation(
            env, 
            lambda obs: torch.tensor(obs.reshape(1, -1), dtype=torch.float32, device=device),
            None),
    ],
    state_init="Default",
)

# https://huggingface.co/facebook/metamotivo-S-1 
# huggingface-cli download --resume-download facebook/metamotivo-S-1 --local-dir ./
# facebook/metamotivo-M-1  facebook/metamotivo-S-1
model = FBcprModel.from_pretrained("/workspace/metamotivo/weights/metamotivo-M-1")
model.to(device)
z = model.sample_z(1)
observation, _ = env.reset()
frames = [env.render()]
for i in range(10):
    action = model.act(observation, z, mean=True)
    observation, reward, terminated, truncated, info = env.step(action.cpu().numpy().ravel())
    frames.append(env.render())

# mediapy.show_video(frames, fps=30)
for fi,frame in enumerate(frames):
    cv2.imwrite("frames/frame+{:0>5d}.png".format(fi), frame)
