import random
import math
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Rules:
    start: int = 100          # starting bankroll
    bet: int = 1              # bet size per flip
    p: float = 0.5            # prob of winning a flip
    stop_loss: int = 0        # hard floor
    take_profit: int = 10**10 # hard ceiling

class Bettor:
    def __init__(self, rules: Rules, seed: int | None = None):
        self.r = rules
        self.money = rules.start
        self.bets_taken = 0
        self.money_record = [self.money]
        if seed is not None:
            random.seed(seed)

    def can_bet(self) -> bool:
        return (self.money > self.r.stop_loss and
                self.money < self.r.take_profit and
                self.money >= self.r.bet)

    def step(self):
        # 1 = win, 0 = loss
        win = 1 if random.random() < self.r.p else 0
        self.money += self.r.bet if win else -self.r.bet
        self.bets_taken += 1
        self.money_record.append(self.money)

    def run(self):
        while self.can_bet():
            self.step()
        return {
            "final_money": self.money,
            "bets_taken": self.bets_taken,
            "hit_tp": self.money >= self.r.take_profit,
            "hit_sl": self.money <= self.r.stop_loss or self.money < self.r.bet,
            "path": self.money_record
        }

def simulate_many(rules: Rules, n_runs: int = 5000, seed: int = 42):
    rng = np.random.default_rng(seed)
    results = []
    # independent seeds per run for reproducibility without correlation
    seeds = rng.integers(0, 2**31 - 1, size=n_runs)
    for s in seeds:
        b = Bettor(rules, seed=int(s))
        results.append(b.run())
    return results

def summarize(results, rules: Rules):
    finals = np.array([r["final_money"] for r in results])
    tp_rate = np.mean([r["hit_tp"] for r in results])
    sl_rate = np.mean([r["hit_sl"] for r in results])
    steps = np.array([r["bets_taken"] for r in results])
    out = {
        "n_runs": len(results),
        "mean_final": float(finals.mean()),
        "median_final": float(np.median(finals)),
        "tp_rate": float(tp_rate),
        "sl_rate": float(sl_rate),
        "mean_steps": float(steps.mean()),
        "median_steps": float(np.median(steps)),
    }

    # Theory checks for fair coin, unit bet, SL=0
    if rules.p == 0.5 and rules.bet == 1 and rules.stop_loss == 0 and rules.take_profit < 10**10:
        start = rules.start
        T = rules.take_profit
        out["theory_tp_prob"] = start / T
        out["theory_expected_steps"] = start * (T - start)
    return out

def plot_examples(results, k=5):
    # plot a few sample paths
    plt.figure()
    for r in results[:k]:
        plt.plot(r["path"])
    plt.title(f"{k} sample bankroll paths")
    plt.xlabel("Bets taken")
    plt.ylabel("Bankroll")
    plt.show()

def plot_steps_hist(results):
    # histogram of time-to-absorption
    steps = np.array([r["bets_taken"] for r in results])
    plt.figure()
    plt.hist(steps, bins=50)
    plt.title("Distribution of bets until stop-loss/take-profit")
    plt.xlabel("Bets taken")
    plt.ylabel("Frequency")
    plt.show()

if __name__ == "__main__":
    # Example 1: your original vibe, just parameterized
    rules1 = Rules(start=100, bet=1, p=0.5, stop_loss=50, take_profit=200)
    res1 = simulate_many(rules1, n_runs=5000, seed=1)
    print("Case 1 summary:", summarize(res1, rules1))
    plot_examples(res1, k=5)
    plot_steps_hist(res1)

    # Example 2: No take-profit, see ruin dynamics
    rules2 = Rules(start=100, bet=1, p=0.5, stop_loss=0, take_profit=10**9)
    res2 = simulate_many(rules2, n_runs=2000, seed=2)
    print("Case 2 summary:", summarize(res2, rules2))
    plot_examples(res2, k=5)
    plot_steps_hist(res2)