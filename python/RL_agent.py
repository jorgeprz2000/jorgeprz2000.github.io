import random


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

def move_agent(environment, movement_function):
    outcomes = []
    for n in range(episodes):
        win = False
        for i in range(max_moves):
            movement = movement_function()
            row_count = 0
            # print(environment)
            for row in environment:
                row_count += 1
                column_count = 0
                for value in row:
                    column_count += 1
                    if value == 1:
                        saved_current_state = (row_count-1, column_count-1)
            
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
        outcomes.append("Episode: " + str(n) + ", moves: " + str(i) + ", outcome: " + str(win))
        environment = reset()
    
    win_count = 0
    for outcome in outcomes:
        print(outcome)
        if "True" in outcome:
            win_count += 1

    print(str(win_count/episodes * 100) + "%")

max_moves = 50

move_agent(environment, movement_function)
