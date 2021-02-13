import turtle

x_velocity = 0.30
y_velocity = 0.20

default_wn_config = {
    'turtle_screen': turtle.Screen(),
    'title': 'Pong - Game',
    'bgcolor': 'green',
    'width': 800,
    'height': 600
}

player_config = {
    'player_a_config': {
        'type': 'player',
        'turtle_element': turtle.Turtle(),
        'color': 'black',
        'shape': 'square',
        'stretch_wid': 5,
        'stretch_len': 1,
        'speed': 0,
        'initial_position': (-350, 0),
        'controls': {
            'Up': 'w',
            'Down': 's'
        },
        'velocity': 30

    },

    'player_b_config': {
        'type': 'ai',
        'turtle_element': turtle.Turtle(),
        'color': 'red',
        'shape': 'square',
        'stretch_wid': 5,
        'stretch_len': 1,
        'speed': 0,
        'initial_position': (350, 0),
        'controls': {
            'Up': 'i',
            'Down': 'k'
        },
        'velocity': 30
        

    }
}

ball_config = {
    'turtle_element': turtle.Turtle(),
    'color': 'blue',
    'shape': 'square',
    'speed': 0,
    'initial_position': (0, 0)
}


game_limits = {
    'x_limit': 350,
    'y_limit': 260
}

movement_settings = {
    'right_up': {
        'direction':(x_velocity, y_velocity),
        'board_limit_direction':['right_down', 'right_down'],
        'player_contact_direction':['left_down', 'left_up']
        },
    'right_down': {
        'direction':(x_velocity, -y_velocity),
        'board_limit_direction': ['right_up', 'right_up'],
        'player_contact_direction':['left_down', 'left_up']
        },
    'left_up': {
        'direction':(-x_velocity, y_velocity),
        'board_limit_direction': ['left_down', 'left_down'],
        'player_contact_direction':['right_up', 'right_down']
        },
    'left_down': {
        'direction':(-x_velocity, -y_velocity),
        'board_limit_direction': ['left_up', 'left_up'],
        'player_contact_direction':['right_down', 'right_up']
        }
}
