'''
Somewhat messed up extremeley rudimenary version of blackjack
I'm honestly not sure if this is the most efficient way to 
perform this method of the game I've created. Let's give it a 
shot
'''

import random
playing = True
suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,
'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

class Card:

    def __init__(self,suit,rank):

        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of  ' + self.suit

class Deck:

    def __init__(self):

        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                # Create the card object

                self.all_cards.append(Card(suit,rank))

    def __str__(self):

        deck_translate = ''
        for card in self.all_cards:
            deck_translate += '\n'+card.__str__()   # Adds each card's printed string
        return 'The deck has: '+ deck_translate

    def shuffle(self):

        random.shuffle(self.all_cards)

    def deal(self):

        return self.all_cards.pop()

class Hand:

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        
         self.cards.append(card)
         self.value += values[card.rank]
         if card.rank == 'Ace':
             self.aces += 1 # add aces to ace count
    
    def adjust_for_ace(self):
        
        while self.value >= 21 and self.aces:
            
            self.value -= 10
            self.value -= 1

class Chips:

        def __init__(self):

            self.total = 100
            self.bet = 0

        def __str__(self):

            return f'You have: {self.total} chips'

        def win_bet(self):

            self.total += self.bet*2

        def lose_bet(self):

            self.total -= self.bet

        def push_bet(self):

            self.total += self.bet

def take_bet(chips):

    while True:
        try:
             chips.bet = int(input('How much will you bet?: '))
             chips.total -= chips.bet
        except ValueError:
            print('Sorry, must be a number!')
        else:
            if chips.bet > chips.total:
                print('Sorry, not enough chips available!')
            else:
                break

def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):

    global playing

    while True:

        choice = input('Hit or Stand? (h/s): ').lower()
        if choice[0] == 'h':
            hit(deck,hand)     # Hit defined above
        elif choice[0] == 's':
            print('Player stands. Dealer is playing.')
            playing = False
        else:
            print('Sorry, try again.')
            continue
        break

def show_some(player,dealer):

    print("\nDealer's hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])
    print("\nPlayer's hand:", *player.cards, sep='\n')
    
def show_all(player,dealer):

    print("\nDealer's hand:", *dealer.cards, sep='\n')
    print("Dealer's hand = ",dealer.value)
    print("\nPlayer's hand:", *player.cards, sep='\n')
    print("Player's hand = ",player.value)

def player_busts(chips):
    
    print('Player busts.')
    chips.lose_bet
    

def player_wins(chips):
    
    print('Player wins.')
    chips.win_bet

def dealer_busts(chips):
    
    print('Dealer busts.')
    chips.win_bet

def dealer_wins(chips):
    
    print('Dealer wins.')
    chips.lose_bet

def push():
    
    print('PUSH! Nobody wins')

'''
Game Logic:

Create deck, shuffle 2 cards to each player
Set up player's chips
Prompt player to place bet
Show cards, keep one dealer card hidden

while playing: -recall from hit_or_stand
    Prompt player to hit or stand
    Show cards
    Check for bust to break loop
    If player hasn't busted, play dealers hand until dealer reaches 17
    Show all cards
    Run different winning scenereos

Inform player of chip total
Ask to play again
'''

# Set up player's chips
player_chips = Chips()

while True:
    print('Hello! Welcome to Blackjack!')

    new_deck = Deck()
    new_deck.shuffle()
    player = Hand()
    dealer = Hand()
    

    # Display chips
    print(player_chips)

    # Initiate starting bet
    take_bet(player_chips)

    # Deals out cards
    player.add_card(new_deck.deal())
    dealer.add_card(new_deck.deal())
    player.add_card(new_deck.deal())
    dealer.add_card(new_deck.deal())

    # Shows 2 player cards and 1 dealer card
    show_some(player,dealer)

    while playing:

        # Prompt hit or stand
        if player.value < 21:
            hit_or_stand(new_deck,player)
            show_some(player,dealer)
        else:
            pass

        # Bust check
        if player.value > 21:
            player_busts(player_chips)
            print(player_chips)
            break
        else:
            break

    # Dealer hits if player has not busted
    if player.value < 21 and dealer.value < 17:
        dealer.add_card(new_deck.deal())
    elif dealer.value > 21:
        dealer_busts(player_chips)
    
    # Show all cards and values
    show_all(player,dealer)

    # Run win checks
    if player.value == dealer.value:
        push()
        player_chips.push_bet()
        pass
    elif player.value == 21:
        player_wins(player_chips)
        print(player_chips)
        pass
    elif dealer.value == 21:
        dealer_wins(player_chips)
        print(player_chips)
        pass
    elif player.value > dealer.value and player.value < 21:
        player_wins(player_chips)
        print(player_chips)
        pass
    elif dealer.value > player.value and dealer.value < 21:
        dealer_wins(player_chips)
        print(player_chips)
        pass
    else:
        pass

    # Prompt to play again
    replay = input('Would you like to play again? (y/n): ').lower

    if replay == 'y':
        playing = True
        continue
    elif replay == 'n':
        break
    else:
        break