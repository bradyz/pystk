import argparse
from time import time

import pystk

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--track')
    parser.add_argument('-k', '--kart', default='')
    parser.add_argument('-s', '--step_size', type=float)
    parser.add_argument('-n', '--num_player', type=int, default=1)
    args = parser.parse_args()

    configs = {
        'none': pystk.GraphicsConfig.none(),
        'ld': pystk.GraphicsConfig.ld(),
        'sd': pystk.GraphicsConfig.sd(),
        'hd': pystk.GraphicsConfig.hd(),
    }

    for config_name, config in configs.items():
        print(config_name)

        # works even with pystk.GraphicsConfig.none
        config.screen_width = 320
        config.screen_height = 240

        t0 = time()
        pystk.init(config)
        init_time, t0 = time() - t0, time()

        config = pystk.RaceConfig()
        if args.kart != '':
            config.players[0].kart = args.kart
        if args.track is not None:
            config.track = args.track
        if args.step_size is not None:
            config.step_size = args.step_size
        for i in range(1, args.num_player):
            config.players.append(pystk.PlayerConfig(args.kart, pystk.PlayerConfig.Controller.AI_CONTROL))

        race = pystk.Race(config)
        race_time, t0 = time() - t0, time()

        race.start()
        race.step()
        start_time, t0 = time() - t0, time()

        for it in range(500):
            race.step()
            if len(race.render_data):
                race.render_data[0].image
                race.render_data[0].depth
                race.render_data[0].instance
        step_time, t0 = time() - t0, time()
        for it in range(5):
            race.restart()
        restart_time, t0 = time() - t0, time()

        times = {
            'graphics': init_time,
            'race config': race_time,
            'start': start_time,
            'restart': restart_time / 5.,
            'step FPS': 500. / step_time,
        }
        times = {k: f'{v:.3f}' for k, v in times.items()}
        max_key = max(map(len, times.keys()))
        max_val = max(map(len, times.values()))

        for key, value in times.items():
            print(f"  {key+':':{max_key+2}} {value:>{max_val}}")

        race.stop()
        del race
        pystk.clean()
