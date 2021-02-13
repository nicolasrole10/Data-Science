import time
import pickle
import turtle
import numpy as np
from pynput.keyboard import Key, Controller
from sklearn.linear_model import LogisticRegression
from entities.window import window_starter
from entities.elements import ball_starter, player_starter
from settings.game_config import default_wn_config, player_config, ball_config
import random


class World():
    def __init__(self, win_data, ball_data, player_data):
        self.window = window_starter(world=self, **win_data)
        self.ball = ball_starter(world=self, **ball_data)
        self.player_a = player_starter(
            world=self, **player_data.get('player_a_config'))
        self.player_b = player_starter(
            world=self, **player_data.get('player_b_config'))
        self.learning_data = {
            'ball_x': [],
            'ball_y': [],
            'my_position_x': [],
            'my_position_y': [],
            'move': []
        }
        self.score = turtle.Turtle()


    def set_game(self):
        self.window.set_window()
        self.ball.set_element()
        self.player_a.set_element()
        self.player_b.set_element()
        self.player_a.controls_settings(window=self.window)
        self.player_b.controls_settings(window=self.window)
        self.score.hideturtle()
        self.score.speed(0)
        self.score.penup()
        self.score.goto(0,250)
        self.score.write("Nicolas 0 - AI 0", align='center', font=("Courier", 24, "normal"))



# Start the machine learning model

with open('./ml_models/LR.pkl', 'rb') as log:
    model = pickle.load(log)

# Creating the world game and set game configurations
world = World(default_wn_config, ball_config, player_config)
world.set_game()
start = time.time()

keyboard = Controller()

# Main game loop
while True:
    world.window.window.update()
    if random.choice([x for x in range(0, 50)]) == 0:
        predictors = np.array([world.ball.element.xcor(),
                               world.ball.element.ycor(),
                               world.player_b.element.xcor(),
                               world.player_b.element.ycor()]).reshape(1, -1)
        movement_prediction = model.predict(predictors)
        if movement_prediction == 1:
            keyboard.press('i')
        else:
            keyboard.press('k')
    world.ball.ball_movement()
    world.ball.movementvalidator.players_update(player_a=world.player_a,
                                                player_b=world.player_b)
    if time.time() - start >= 360 and time.time() - start < 361:
        with open('training_data.pkl', 'wb') as file:
            pickle.dump(world.learning_data, file,
                        protocol=pickle.HIGHEST_PROTOCOL)
    print(int(time.time() - start))
