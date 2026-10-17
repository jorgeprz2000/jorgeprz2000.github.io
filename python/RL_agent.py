import random

action_to_movement = {
    "up" : (-1,0),
    "down" : (1,0),
    "left" : (0,-1),
    "right" : (0,1)
}

def reward(position):
    if position == (0,0):
        reward = 1
    else: 
        reward = 0 
    return reward 

def Q_learning(current_position, previous_position):
    # Work on this next !

episodes = 1000

environment = [["*",0,0,0], 
               [0,0,0,0], 
               [0,0,0,0], 
               [0,0,0,1]]

def reset():
    reset_environment = [["*",0,0,0], 
               [0,0,0,0], 
               [0,0,0,0], 
               [0,0,0,1]]
    return reset_environment

def movement_function():

    move_set = [(-1,0), (0,1), (0,-1), (1,0)]
    
    movement = random.choice(move_set)
    # print(movement)
    return movement


def create_Q_table():
    Q_table = {}
    for x in range(4):
        for y in range(4):
            Q_table[(x,y)] = {
                "up":0,
                "down":0,
                "left":0,
                "right":0
            }
    # print(Q_table)
    return Q_table

Q_table = create_Q_table()

def move_Q_table(position):
    move_set = ["up", "down", "left", "right"]
    epsilon = 0.1
    n = random.random()
    if n < epsilon:
        direction_final = random.choice(move_set)
        movement = Q_table[position][direction_final]
    else:
        match = []
        movement = max(Q_table[position].values())
        for i in Q_table[position]:
            # print("HERE" + str(Q_table[position][i]))
            if Q_table[position][i] == movement:
                direction = i
                match.append(direction)
                # print(direction)
        direction_final = random.choice(match)
    
    print("MOVEMENT " + str(movement) + direction_final)

    return direction_final

def move_agent(environment, movement_function):
    outcomes = []
    for n in range(episodes):
        win = False
        for i in range(max_moves):
            row_count = 0
            # print(environment)
            for row in environment:
                row_count += 1
                column_count = 0
                for value in row:
                    column_count += 1
                    if value == 1:
                        saved_current_state = (row_count-1, column_count-1)
            movement = action_to_movement[move_Q_table(saved_current_state)]
            # clear board
        
            environment[saved_current_state[0]][saved_current_state[1]] = 0
            
            # move agent according to movement 
            
            new_position_y = saved_current_state[0] + movement[0]
            new_position_x = saved_current_state[1] + movement[1]

            # print(saved_current_state)
            # print(new_position)
            
            if new_position_y < 0 or new_position_x < 0 or new_position_y > 3 or new_position_x > 3:
                # print("INVALID MOVE")
                environment[saved_current_state[0]][saved_current_state[1]] = 1
                # print(environment)
            else:
                # print("VALID MOVE")
                environment[new_position_y][new_position_x] = 1
                # print(environment)
            if  new_position_y == 0 and new_position_x == 0:
                # print("YOU WIN")
                win = True
                break
        outcomes.append("Episode: " + str(n) + ", moves: " + str(i + 1) + ", outcome: " + str(win))
        environment = reset()
    
    win_count = 0
    for outcome in outcomes:
        # print(outcome)
        if "True" in outcome:
            win_count += 1

    print(str(win_count/episodes * 100) + "%")

max_moves = 50

move_agent(environment, movement_function)










# print(Q_table)
