import random
import time
from rich import box
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Group

# ---------------------------------------------------------------------------
# Rendering (rich) — remove this block + the live.* lines to go back to plain
# ---------------------------------------------------------------------------

ARROWS = {"up": "↑", "down": "↓", "left": "←", "right": "→"}

def heat(v):
    v = max(0.0, min(1.0, v))
    g = int(40 + 170 * v)
    return f"bold white on rgb(15,{g},{int(g * 0.6)})"

def render(environment, Q_table, episode, step):
    tables = []
    for _ in range(3):
        t = Table(show_header=False, box=box.SQUARE, padding=(0, 1))
        for _ in range(4):
            t.add_column(justify="center", width=5)
        tables.append(t)
    board, vals, pol = tables

    for r in range(4):
        b_row, v_row, p_row = [], [], []
        for c in range(4):
            if environment[r][c] == 1:
                b_row.append("[bold yellow]●[/]")
            elif (r, c) == (0, 0):
                b_row.append("[bold green]★[/]")
            else:
                b_row.append("[dim]·[/]")

            q = Q_table[(r, c)]
            m = max(q.values())
            v_row.append(f"[{heat(m)}]{m:.2f}[/]")

            if (r, c) == (0, 0):
                p_row.append("[bold green]G[/]")
            elif m == 0 or list(q.values()).count(m) > 1:
                p_row.append("[dim]·[/]")
            else:
                p_row.append(f"[bold cyan]{ARROWS[max(q, key=q.get)]}[/]")
        board.add_row(*b_row)
        vals.add_row(*v_row)
        pol.add_row(*p_row)

    panels = Columns([
        Panel(board, title="Board"),
        Panel(vals, title="Max Q"),
        Panel(pol, title="Policy"),
    ])
    return Group(panels, f"[bold]Episode[/] {episode}   [bold]Step[/] {step}")

# ---------------------------------------------------------------------------
# Your Q-learning code
# ---------------------------------------------------------------------------

action_to_movement = {
    "up" : (-1,0),
    "down" : (1,0),
    "left" : (0,-1),
    "right" : (0,1)
}

def reward_return(position):
    if position == (0,0):
        reward = 1
    else:
        reward = 0
    return reward

def Q_learning(current_pos, previous_position, previous_move, Q_table):
    learning_rate = 0.1
    discount_factor = 0.9
    reward = reward_return(current_pos)
    Q_table[previous_position][previous_move] = ((1-learning_rate)*Q_table[previous_position][previous_move] + learning_rate * (reward + (discount_factor*max(Q_table[current_pos].values()))))
    return Q_table


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
    return Q_table


def move_Q_table(position, Q_table):
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
            if Q_table[position][i] == movement:
                direction = i
                match.append(direction)
        direction_final = random.choice(match)

    # print("MOVEMENT " + str(movement) + direction_final)  # off: breaks the live display

    return direction_final

def move_agent(environment, movement_function):

    Q_table = create_Q_table()

    outcomes = []

    live = Live(render(environment, Q_table, 0, 0), refresh_per_second=30)
    live.start()

    for n in range(episodes):
        win = False
        for i in range(max_moves):
            row_count = 0
            for row in environment:
                row_count += 1
                column_count = 0
                for value in row:
                    column_count += 1
                    if value == 1:
                        saved_current_state = (row_count-1, column_count-1)
            directional_move = move_Q_table(saved_current_state, Q_table)
            movement = action_to_movement[directional_move]

            # clear board
            environment[saved_current_state[0]][saved_current_state[1]] = 0

            # move agent according to movement
            new_position_y = saved_current_state[0] + movement[0]
            new_position_x = saved_current_state[1] + movement[1]

            if new_position_y < 0 or new_position_x < 0 or new_position_y > 3 or new_position_x > 3:
                # INVALID MOVE
                environment[saved_current_state[0]][saved_current_state[1]] = 1
                Q_table = Q_learning((saved_current_state),saved_current_state,directional_move, Q_table)
            else:
                # VALID MOVE
                environment[new_position_y][new_position_x] = 1
                Q_table = Q_learning((new_position_y, new_position_x),saved_current_state, directional_move, Q_table)

            # live display: first 5 episodes, every 100th, and the last one
            if n < 5 or n % 100 == 0 or n == episodes - 1:
                live.update(render(environment, Q_table, n, i + 1))
                time.sleep(0.08)

            if new_position_y == 0 and new_position_x == 0:
                win = True
                break

        outcomes.append("Episode: " + str(n) + ", moves: " + str(i + 1) + ", outcome: " + str(win))
        environment = reset()

    live.stop()

    win_count = 0
    for outcome in outcomes:
        if "True" in outcome:
            win_count += 1

    print(str(win_count/episodes * 100) + "%")

    return Q_table

max_moves = 50

Q_table = move_agent(environment, movement_function)