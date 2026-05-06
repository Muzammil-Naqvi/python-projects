import random

# --- Card Setup ---
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def card_value(rank):
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def hand_total(hand):
    total = sum(card_value(rank) for rank, suit in hand)
    aces = sum(1 for rank, suit in hand if rank == 'A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def card_str(card):
    rank, suit = card
    return f"{rank} of {suit}"

def show_hand(name, hand, hide_second=False):
    print(f"\n{name}'s hand:")
    for i, card in enumerate(hand):
        if hide_second and i == 1:
            print("  [Hidden]")
        else:
            print(f"  {card_str(card)}")
    if not hide_second:
        print(f"  Total: {hand_total(hand)}")

def new_deck():
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def deal(deck, count=1):
    cards = deck[:count]
    del deck[:count]
    return cards

# --- Main Game ---
def play_blackjack():
    print("=" * 40)
    print("       Welcome to Blackjack!")
    print("=" * 40)

    balance = 1000

    while True:
        print(f"\nYour balance: ${balance}")

        # Bet
        while True:
            try:
                bet = int(input("Enter your bet: $"))
                if bet <= 0:
                    print("Bet must be positive.")
                elif bet > balance:
                    print("Not enough balance.")
                else:
                    break
            except ValueError:
                print("Enter a valid number.")

        # Deal
        deck = new_deck()
        player = deal(deck, 2)
        dealer = deal(deck, 2)

        show_hand("Dealer", dealer, hide_second=True)
        show_hand("You", player)

        # Check player blackjack
        if hand_total(player) == 21:
            print("\nBlackjack! You win 1.5x your bet!")
            balance += int(bet * 1.5)
            show_hand("Dealer", dealer)
            play_again = input("\nPlay again? (y/n): ").strip().lower()
            if play_again != 'y':
                break
            continue

        # Player turn
        bust = False
        while True:
            action = input("\nHit or Stand? (h/s): ").strip().lower()
            if action == 'h':
                player += deal(deck, 1)
                show_hand("You", player)
                if hand_total(player) > 21:
                    print("Bust! You went over 21.")
                    bust = True
                    break
                elif hand_total(player) == 21:
                    print("21! Nice hand.")
                    break
            elif action == 's':
                break
            else:
                print("Type 'h' to hit or 's' to stand.")

        # Dealer turn
        show_hand("Dealer", dealer)
        if not bust:
            while hand_total(dealer) < 17:
                print("Dealer hits...")
                dealer += deal(deck, 1)
                show_hand("Dealer", dealer)

        # Result
        player_total = hand_total(player)
        dealer_total = hand_total(dealer)

        print("\n--- Result ---")
        if bust:
            print(f"You busted. You lose ${bet}.")
            balance -= bet
        elif dealer_total > 21:
            print(f"Dealer busted! You win ${bet}!")
            balance += bet
        elif player_total > dealer_total:
            print(f"You win ${bet}!")
            balance += bet
        elif player_total < dealer_total:
            print(f"Dealer wins. You lose ${bet}.")
            balance -= bet
        else:
            print("It's a tie. Bet returned.")

        if balance <= 0:
            print("\nYou're out of money. Game over!")
            break

        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            break

    print(f"\nFinal balance: ${balance}")
    print("Thanks for playing!")

if __name__ == "__main__":
    play_blackjack()
