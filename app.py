# app.py
import random

class Ranker:
    def __init__(self):
        self.item_scores = {}
        self.MAX_ROUNDS = 50
        self.THRESHOLD = 10

    def add_item(self, item):
        if item not in self.item_scores:
            self.item_scores[item] = 1400

    def get_items(self):
        return list(self.item_scores.keys())

    def reset_items(self):
        self.item_scores = {}

    def get_next_pair(self, last_option_a=None, last_option_b=None):
        items = self.get_items()
        if len(items) < 2:
            return None, None

        option_a = random.choice(items)
        option_b = random.choice(items)

        while option_a == option_b or (option_a == last_option_a and option_b == last_option_b) or (option_a == last_option_b and option_b == last_option_a):
            option_a = random.choice(items)
            option_b = random.choice(items)

        return option_a, option_b

    def update_elo(self, winner, loser):
        winner_curr_elo = self.item_scores.get(winner)
        loser_curr_elo = self.item_scores.get(loser)

        new_winner_elo = winner_curr_elo + 100 * (1 - self.expected_score(winner_curr_elo, loser_curr_elo))
        new_loser_elo = loser_curr_elo + 100 * (0 - self.expected_score(loser_curr_elo, winner_curr_elo))

        change = abs(new_winner_elo - winner_curr_elo) + abs(new_loser_elo - loser_curr_elo)

        self.item_scores[winner] = round(new_winner_elo)
        self.item_scores[loser] = round(new_loser_elo)

        return change

    def expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10**((rating_b - rating_a) / 400))

    def get_sorted_items(self):
        return sorted(self.item_scores.items(), key=lambda x: x[1], reverse=True)
    
    def reset(self):
        self.item_scores = {}
