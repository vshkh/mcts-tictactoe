import matplotlib.pyplot as plt
import os

def plot_mcts_summary(children, move_number=0):
    moves = [str(child.move) for child in children]
    visits = [child.visits for child in children]
    win_rates = [child.wins / child.visits if child.visits > 0 else 0 for child in children]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Moves')
    ax1.set_ylabel('Visits', color='tab:blue')
    ax1.bar(moves, visits, color='tab:blue', alpha=0.6)
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Win Rate', color='tab:green')
    ax2.plot(moves, win_rates, color='tab:green', marker='o')
    ax2.tick_params(axis='y', labelcolor='tab:green')

    plt.title(f'MCTS Summary – Move #{move_number}')
    fig.tight_layout()
    
    os.makedirs("mcts_charts", exist_ok=True)
    plt.savefig(f"mcts_charts/move_{move_number}.png")
    plt.close()

