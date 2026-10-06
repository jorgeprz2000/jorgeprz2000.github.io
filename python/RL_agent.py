environment = [[0,0,0,0], 
               [0,0,0,0], 
               [0,0,1,0], 
               [0,0,0,0]]


def record_position_and_clear_env():
    row_count = 0
    for row in environment:
        row_count += 1
        column_count = 0
        for value in row:
            column_count += 1
            if value == 1:
                saved_current_state = (row_count-1, column_count-1)
    environment[saved_current_state[0]][saved_current_state[1]] = 0
    print(environment)
    print(saved_current_state)


record_position_and_clear_env()

def move_up(current_state):
    current_state[1] = current_state[1] + 1
    
# # def update_environment():



# # move_up()