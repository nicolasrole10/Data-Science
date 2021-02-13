from settings.game_config import game_limits, movement_settings
import random


class GameLimits():
    def __init__(self, **kwargs):
        self.x_limit = kwargs.get('x_limit')
        self.y_limit = kwargs.get('y_limit')
        self.x2_limit = kwargs.get('x_limit') * -1
        self.y2_limit = kwargs.get('y_limit') * -1


limits = GameLimits(**game_limits)


class LimitsMovement():
    def __init__(self):
        self.right_up = movement_settings.get('right_up')
        self.right_down = movement_settings.get('right_down')
        self.left_up = movement_settings.get('left_up')
        self.left_down = movement_settings.get('left_down')

    def limits_direction(self, direction):
        movements = getattr(self, direction).get('board_limit_direction')
        selection = random.choice(movements)
        return selection

    def paddle_direction(self, direction):
        movements = getattr(self, direction).get('player_contact_direction')
        selection = random.choice(movements)
        return selection


class MovementValidator():
    def __init__(self, limits, ball):
        self.ball = ball
        self.x_limit = limits.x_limit
        self.y_limit = limits.y_limit
        self.x2_limit = limits.x2_limit
        self.y2_limit = limits.y2_limit
        self.player_a = None
        self.player_b = None
        self.limit_movement = LimitsMovement()

    def right_up(self, x, y):
        if x < self.x_limit and y < self.y_limit:
            return True
        elif y > self.y_limit:
            self.ball.direction = self.limit_movement.limits_direction(
                'right_up')
            return False
        else:
            if y > self.player_b[0] and y < self.player_b[1]:
                self.ball.direction = self.limit_movement.paddle_direction(
                    'right_up')
                return False
            else:
                self.ball.world.player_a.points += 1
                return 'reset'

    def right_down(self, x, y):
        if x < self.x_limit and y > self.y2_limit:
            return True
        elif y < self.y2_limit:
            self.ball.direction = self.limit_movement.limits_direction(
                'right_down')
            return False
        else:
            if y > self.player_b[0] and y < self.player_b[1]:
                self.ball.direction = self.limit_movement.paddle_direction(
                    'right_down')
                return False
            else:
                self.ball.world.player_a.points += 1
                return 'reset'

    def left_up(self, x, y):
        if x > self.x2_limit and y < self.y_limit:
            return True
        elif y > self.y_limit:
            self.ball.direction = self.limit_movement.limits_direction(
                'left_up')
            return False
        else:
            if y > self.player_a[0] and y < self.player_a[1]:
                self.ball.direction = self.limit_movement.paddle_direction(
                    'left_up')
                return False
            else:
                self.ball.world.player_b.points += 1
                return 'reset'

    def left_down(self, x, y):
        if x > self.x2_limit and y > self.y2_limit:
            return True
        elif y < self.y_limit:
            self.ball.direction = self.limit_movement.limits_direction(
                'left_down')
            return False
        else:
            if y > self.player_a[0] and y < self.player_a[1]:
                self.ball.direction = self.limit_movement.paddle_direction(
                    'left_down')
                return False
            else:
                self.ball.world.player_b.points += 1
                return 'reset'

    def players_update(self, player_a, player_b):
        self.player_a = set_ysize(player_a.element.ycor())
        self.player_b = set_ysize(player_b.element.ycor())


class player_starter():
    def __init__(self, world, **kwargs):
        self.world = world
        self.type = kwargs.get('type')
        self.element = kwargs.get('turtle_element')
        self.color = kwargs.get('color')
        self.shape = kwargs.get('shape')
        self.stretch_wid = kwargs.get('stretch_wid')
        self.stretch_len = kwargs.get('stretch_len')
        self.speed = kwargs.get('speed')
        self.initial_position = kwargs.get('initial_position')
        self.up = kwargs.get('controls').get('Up')
        self.down = kwargs.get('controls').get('Down')
        self.velocity = kwargs.get('velocity')
        self.points = 0

    def set_element(self):
        self.element.shape(self.shape)
        self.element.shapesize(stretch_wid=self.stretch_wid,
                               stretch_len=self.stretch_len)
        self.element.penup()
        self.element.goto(self.initial_position)
        self.element.color(self.color)

    def controls_settings(self, window):
        # Up_control
        window.window.onkeypress(self.move_up, self.up)

        # Down_control
        window.window.onkeypress(self.move_down, self.down)

    def move_up(self):
        y = self.element.ycor() + self.velocity
        if y < limits.y_limit:
            self.element.sety(y)
            if self.type == 'ai':
                self.world.learning_data['ball_x'].append(self.world.ball.element.xcor())
                self.world.learning_data['ball_y'].append(self.world.ball.element.ycor())
                self.world.learning_data['my_position_x'].append(self.world.player_b.element.xcor())
                self.world.learning_data['my_position_y'].append(self.world.player_b.element.ycor())
                self.world.learning_data['move'].append('Up')

    def move_down(self):
        y = self.element.ycor() - self.velocity
        if y > limits.y2_limit:
            self.element.sety(y)
            if self.type == 'ai':
                self.world.learning_data['ball_x'].append(self.world.ball.element.xcor())
                self.world.learning_data['ball_y'].append(self.world.ball.element.ycor())
                self.world.learning_data['my_position_x'].append(self.world.player_b.element.xcor())
                self.world.learning_data['my_position_y'].append(self.world.player_b.element.ycor())
                self.world.learning_data['move'].append('Down')


class ball_starter():
    def __init__(self, world, **kwargs):
        self.world = world
        self.element = kwargs.get('turtle_element')
        self.color = kwargs.get('color')
        self.shape = kwargs.get('shape')
        self.speed = kwargs.get('speed')
        self.initial_position = kwargs.get('initial_position')
        self.direction = 'right_up'
        self.movementvalidator = MovementValidator(limits=limits, ball=self)

    def set_element(self):
        self.element.shape(self.shape)
        self.element.penup()
        self.element.goto(self.initial_position)
        self.element.color(self.color)

    def ball_movement(self):
        delta_x, delta_y = movement_settings.get(
            self.direction).get('direction')

        # Move in the right direction
        x = self.element.xcor() + delta_x
        y = self.element.ycor() + delta_y

        # Check the boundaries
        if self.direction == 'right_up':
            validation = self.movementvalidator.right_up(x, y)

        elif self.direction == 'right_down':
            validation = self.movementvalidator.right_down(x, y)

        elif self.direction == 'left_up':
            validation = self.movementvalidator.left_up(x, y)

        else:
            validation = self.movementvalidator.left_down(x, y)

        if validation == True:
            self.element.setx(x)
            self.element.sety(y)
        elif validation == 'reset':
            self.world.score.clear()
            self.world.score.write("Nicolas {} - AI {}".format(self.world.player_a.points, self.world.player_b.points), align='center', font=("Courier", 24, "normal"))

            self.element.setx(0)
            self.element.sety(0)
        else:
            pass


def set_ysize(y):
    return (y-60, y+60)
