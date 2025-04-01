import numpy as np
import pystk
from tqdm import tqdm
import matplotlib.pyplot as plt

cfg = pystk.GraphicsConfig.ld()
cfg.screen_width = 128
cfg.screen_height = 96

pystk.init(cfg)

print("pystk.inited")

race_cfg = pystk.RaceConfig(track="lighthouse", step_size=0.1)
race_cfg.num_kart = 1

race = pystk.Race(race_cfg)
race.start()

print("pystk.Race started")

state = pystk.WorldState()
print("state")

state.update()
print("state.update()")

track = pystk.Track()
print("track")
track.update()
print("track.update()")

action = pystk.Action()
print("action")

action.acceleration = 0.5
action.steer = 0.1
action.brake = False

for _ in tqdm(range(5)):
    race.step(action)
    state.update()

image = np.array(race.render_data[0].image)

print(f"f{image.mean()=:.2f} should be > 0")
print(f"f{image.std()=:.2f} should be > 0")

plt.imshow(image)
plt.show()
