import random
import numpy as np
import matplotlib.pyplot as plt

# ----- Config -----
SEED = 42               # set to None for non-deterministic runs
NUM_PLAYERS = 10_00
ITERATIONS = 10000     # spins per player
BET_SIZE = 5.0

if SEED is not None:
    random.seed(SEED)
    np.random.seed(SEED)

class Gambler:
    def __init__(self):
        self.balance = 0.0
        self.record = [0.0]  # balance after 0 spins

    def slap(self):
        """
        One $5 spin with low-volatility outcomes (RTP = 90% → EV payout = $4.50).
        Probabilities sum to 1 exactly.
        """
        outcomes = [
            (0.0,   0.4213),   # 42.13%
            (2.5,   0.20),     # 20.00%
            (5.0,   0.25),     # 25.00%
            (10.0,  0.08),     # 8.00%
            (20.0,  0.03),     # 3.00%
            (50.0,  0.014),    # 1.40%
            (100.0, 0.004),    # 0.40%
            (250.0, 0.0006),   # 0.06%
            (1000.0,0.0001),   # 0.01%
        ]

        r = random.random()
        cum = 0.0
        payout = 0.0
        for x, p in outcomes:
            cum += p
            if r < cum:
                payout = x
                break

        # pay for the spin, receive payout
        self.balance += (payout - BET_SIZE)
        self.record.append(self.balance)
        return payout

def main():
    PROFIT_RECORDS = []

    # Simulate players
    for _ in range(NUM_PLAYERS):
        g = Gambler()
        for _ in range(ITERATIONS):
            g.slap()
        # Defensive: force exact length ITERATIONS+1
        target_len = ITERATIONS + 1
        if len(g.record) < target_len:
            g.record.extend([g.record[-1]] * (target_len - len(g.record)))
        elif len(g.record) > target_len:
            del g.record[target_len:]
        PROFIT_RECORDS.append(g.record)

    # Stack safely into a 2D array
    records = np.stack(PROFIT_RECORDS, axis=0).astype(float)  # shape: (NUM_PLAYERS, ITERATIONS+1)

    # Fraction of players profitable every 10 spins
    spins_checkpoints = list(range(1, ITERATIONS + 1))
    profit_by_tens = []
    for idx in spins_checkpoints:
        frac = np.mean(records[:, idx] > 0.0)
        profit_by_tens.append(frac)

    # Print summary
    for spins, frac in zip(spins_checkpoints, profit_by_tens):
        print(f"After {spins:4d} spins: {frac:.3%} of players are profitable")

    # Sanity check: empirical RTP over all spins
    # Average loss per spin should be ≈ $0.50 (10% of $5)
    total_end_bal = records[:, -1].mean()
    avg_loss_per_spin = -(total_end_bal) / ITERATIONS  # negative of avg ending balance per spin
    print(f"\nEmpirical avg end balance per player: ${total_end_bal:,.2f}")
    print(f"Empirical avg loss per spin:          ${avg_loss_per_spin:,.4f} (theory: $0.5000)")

    # Plot fraction profitable vs spins
    plt.figure()
    plt.plot(spins_checkpoints, profit_by_tens, marker='o')
    plt.title('Fraction of Players Profitable vs Number of Spins')
    plt.xlabel('Spins')
    plt.ylabel('Fraction Profitable')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Optional: plot mean/median balance trajectory
    mean_bal = records.mean(axis=0)
    median_bal = np.median(records, axis=0)
    plt.figure()
    plt.plot(mean_bal, label='Mean balance')
    plt.plot(median_bal, label='Median balance')
    plt.title('Bankroll Trajectory')
    plt.xlabel('Spins')
    plt.ylabel('Balance ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()