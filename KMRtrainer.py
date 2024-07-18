from random import uniform

knight = 1
mage = 2
ranger = 3
NUM_ACTIONS = 3
strategy = []
regret_sum = []
strategy_sum = []

class CFRBot:
    def __init__(self):
        self.knight = 1
        self.mage0341
        = 2
        self.ranger = 3
        self.NUM_ACTIONS = 3
        self.regret_sum = [0] * self.NUM_ACTIONS
        self.strategy = [0] * self.NUM_ACTIONS
        self.strategy_sum = [0] * self.NUM_ACTIONS
        self.opp_strategy = [0.4, 0.3, 0.3]

    def get_strategy(self) -> list[float]:
        normalizing_sum = 0
        for i in range(self.NUM_ACTIONS):
            self.strategy[i] = self.regret_sum[i] if self.regret_sum[i] > 0 else 0
            normalizing_sum += self.strategy[i]
        for i in range(self.NUM_ACTIONS):
            if normalizing_sum > 0:
                self.strategy[i] /= normalizing_sum
            else:
                self.strategy[i] = 1.0 / self.NUM_ACTIONS
            self.strategy_sum[i] += self.strategy[i]
        return self.strategy

    def get_action(self, strat: list[float]) -> int:
        r = uniform(0, 1)
        a = 0
        cumulative_probability = 0
        while a < NUM_ACTIONS - 1:
            cumulative_probability += strat[a]
            if r < cumulative_probability:
                break
            a += 1
        return a

    def train(self, iterations: int) -> None:
        action_utility = [0] * NUM_ACTIONS
        for i in range(iterations):
            strat = self.get_strategy()
            my_action = self.get_action(strat)
            other_action = self.get_action(self.opp_strategy)

            action_index_one = 0 if other_action == NUM_ACTIONS - 1 else other_action + 1
            action_index_two = NUM_ACTIONS - 1 if other_action == 0 else other_action - 1

            action_utility[other_action] = 0
            action_utility[action_index_one] = 1
            action_utility[action_index_two] = -1

            for j in range(NUM_ACTIONS):
                self.regret_sum[j] = action_utility[j] - action_utility[my_action]

    def get_average_strategy(self) -> list[float]:
        avg_strat = [0] * self.NUM_ACTIONS 
        normalizing_sum = 0

        for i in range(self.NUM_ACTIONS):
            normalizing_sum += self.strategy_sum[i]

        for i in range(self.NUM_ACTIONS):
            if normalizing_sum > 0:
                avg_strat[i] = self.strategy_sum[i] / normalizing_sum
            else:
                avg_strat[i] = 1.0 / self.NUM_ACTIONS

        return avg_strat


if __name__ == "__main__":
    trainer = CFRBot()
    trainer.train(1000000)
    print(trainer.get_average_strategy())