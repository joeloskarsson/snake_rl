import scipy.linalg as lin
import os
from keras import models, layers, optimizers, utils

from constants import *

# REINFORCE AGENT
class RFAgent:
    def __init__(self, gamma=1.0, lr=0.001, weights_file=None):
        self.gamma = gamma
        self.network = models.Sequential([
            layers.Conv2D(filters=32, input_shape=(7,7,2), kernel_size=(3,3),
                padding="same"),
            # (7,7,32,)
            layers.Conv2D(filters=32, kernel_size=(3,3), padding="valid"),
            # (5,5,32)
            layers.Conv2D(filters=32, kernel_size=(3,3), padding="valid"),
            # (3,3,32)
            layers.MaxPooling2D(pool_size=(3,3)),
            # (1,1,32)
            layers.Flatten(),
            # (32)
            layers.Dense(16),
            # (16)
            layers.Dense(4),
            # (4)
            layers.Softmax(),
            # (4)
        ])

        opt = optimizers.SGD(learning_rate=lr) # Keep learning rate at 0.001
        self.network.compile(optimizer=opt, loss="categorical_crossentropy")

        if weights_file:
            self.network.load_weights(weights_file)

    def translate_state(self, board):
        # Takes batches
        token_state = (board == TOKEN).astype(float)
        snake_state = (board == SNAKE).astype(float)
        state = np.stack([token_state, snake_state], axis=3)

        # Shape (B,7,7,2)
        return state

    def act(self, board):
        state = self.translate_state(np.expand_dims(board, axis=0))
        action_dist = self.network.predict(state)[0]

        # Sample from categorical distribution
        action = np.random.choice(np.arange(4), p=action_dist)
        return action

    def train(self, trajectory):
        T = trajectory.rewards.shape[0] # Trajectory length

        discounting = np.power(self.gamma, np.arange(T))
        disc_rewards = trajectory.rewards*discounting

        G = np.cumsum(disc_rewards[::-1])[::-1]

        inputs = self.translate_state(trajectory.states)
        targets = utils.to_categorical(trajectory.actions, num_classes=4)

        self.network.train_on_batch(x=inputs, y=targets, sample_weight=G)

    def save(self, directory):
        file_name = os.path.join(directory, PARAM_FILE)
        self.network.save_weights(file_name)

