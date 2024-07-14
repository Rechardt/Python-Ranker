"""This is my file"""
import random

# Defining constants
item_scores = {}
items = []
MAX_ROUNDS = 50
THRESHOLD = 10 # Threshold for ELO score change to consider as stable

def main():
    print("Enter the items you want to rank. To stop inputting, enter -1")
    item = input("Enter item: ")
    count = 0
    while item != "-1":
        item_scores[item] = 1400
        items.append(item)
        item = input("Enter item: ")
        count += 1

    print_items()

    # Commence the ranking
    print("We will now rank the items")

    rounds = (count * (count - 1)) / 2

    rank(min(MAX_ROUNDS, rounds))

    print()
    print("Final ranking: ")
    print_items()

def rank(max_rounds):
    rounds = 0
    last_option_a = None
    last_option_b = None

    while rounds < max_rounds:
        print()
        # Choose the competitors
        option_a = str(random.choice(items))
        option_b = str(random.choice(items))

        # Ensure no two same items are picked in a row
        while option_a == option_b or (option_a == last_option_a and option_b == last_option_b) or (option_a == last_option_b and option_b == last_option_a):
            option_a = str(random.choice(items))
            option_b = str(random.choice(items))

        print(option_a, "vs", option_b)
        choice = -1
        while (choice not in [0,1]):
            choice = int(input("Enter 1 for left, 0 for right "))
            if choice == -1:
                return

        if choice == 1:
            winner = option_a
            loser = option_b
        else:
            winner = option_b
            loser = option_a

        elo_change = updateElo(winner, loser)

        # Update last picked items
        last_option_a = option_a
        last_option_b = option_b

        # If the change was below the threshold, terminate early
        if elo_change <= THRESHOLD:
            return

        rounds += 1

def print_items():
    print("These are the items you entered: ")
    print("===========================")

    count = 1

    # Sort items by ELO score in increasing order
    sorted_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)

    for item, score in sorted_items:
        print(str(count) + ".", item, score)
        count += 1

def updateElo(winner, loser):
    # Obtain current ELOS
    winner_curr_elo = item_scores.get(winner)
    loser_curr_elo = item_scores.get(loser)

    # Calculate new ELOs
    new_winner_elo = winner_curr_elo + 100 * (1 - expectedScore(winner_curr_elo, loser_curr_elo))
    new_loser_elo = loser_curr_elo + 100 * (0 - expectedScore(loser_curr_elo, winner_curr_elo))

    # Calculate the change
    change = abs(new_winner_elo - winner_curr_elo) + abs(new_loser_elo - loser_curr_elo)

    # Update scores
    item_scores[winner] = round(new_winner_elo)
    item_scores[loser] = round(new_loser_elo)

    return change

def expectedScore(ratingA, ratingB):
    return 1 / (1 + 10**((ratingB - ratingA) / 400))

if __name__ == "__main__":
    main()