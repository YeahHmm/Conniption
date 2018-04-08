import os
from datetime import datetime
from logging import getLogger
from time import time
from copy import deepcopy

from conniption_zero.agent.alphazero_AI import AlphaZeroAI
from conniption_zero.config import Config
from conniption_zero.env.connect4_env import Connect4Env, Winner, Player
from conniption_zero.lib import tf_util
from conniption_zero.lib.data_helper import get_game_data_filenames, write_game_data_to_file
from conniption_zero.lib.model_helpler import load_best_model_weight, save_as_best_model, \
    reload_best_model_weight_if_changed

logger = getLogger(__name__)

from resources.resource import SystemState

def start(config: Config):
    tf_util.set_session_config(per_process_gpu_memory_fraction=0.2)
    return SelfPlayWorker(config, env=SystemState()).start()


class SelfPlayWorker:
    def __init__(self, config: Config, env=None, model=None):
        """

        :param config:
        :param Connect4Env|None env:
        :param connect4_zero.agent.model_connect4.Connect4Model|None model:
        """
        self.config = config
        self.model = model
        self.env = env     # type: Connect4Env
        self.black = None  # type: Connect4Player
        self.white = None  # type: Connect4Player
        self.buffer = []

    def start(self):
        if self.model is None:
            self.model = self.load_model()

        self.buffer = []
        idx = 1

        while True:
            start_time = time()
            env = self.start_game(idx)
            end_time = time()
            logger.debug(f"game {idx} time={end_time - start_time} sec, "
                         f"turn={env._num_placed}:{env.observation} - Winner:{env.done()[1]}")
            if (idx % self.config.play_data.nb_game_in_file) == 0:
                reload_best_model_weight_if_changed(self.model)
            idx += 1

    def start_game(self, idx):
        self.env = SystemState()
        self.black = AlphaZeroAI('ALPHAZERO1', self.config, self.model)
        self.white = AlphaZeroAI('ALPHAZERO2', self.config, self.model)

        while not self.env.done()[0]:
            if self.env._player == 0:
                action = self.black.choose_move(deepcopy(self.env))
            else:
                action = self.white.choose_move(deepcopy(self.env))
            print('back in the loop')
            print (action)
            self.env = self.env.update(action)
            print(self.env)
        self.finish_game()
        self.save_play_data(write=idx % self.config.play_data.nb_game_in_file == 0)
        self.remove_play_data()
        return self.env

    def save_play_data(self, write=True):
        data = self.black.moves + self.white.moves
        self.buffer += data

        if not write:
            return

        rc = self.config.resource
        game_id = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        path = os.path.join(rc.play_data_dir, rc.play_data_filename_tmpl % game_id)
        logger.info(f"save play data to {path}")
        write_game_data_to_file(path, self.buffer)
        self.buffer = []

    def remove_play_data(self):
        files = get_game_data_filenames(self.config.resource)
        if len(files) < self.config.play_data.max_file_num:
            return
        for i in range(len(files) - self.config.play_data.max_file_num):
            os.remove(files[i])

    def finish_game(self):
        _, winner = self.env.done()
        if winner == 0:
            black_win = 1
        elif winner == 1:
            black_win = -1
        else:
            black_win = 0

        self.black.finish_game(black_win)
        self.white.finish_game(-black_win)

    def load_model(self):
        from conniption_zero.agent.model_connect4 import Connect4Model
        model = Connect4Model(self.config)
        if self.config.opts.new or not load_best_model_weight(model):
            model.build()
            save_as_best_model(model)
        return model
