# !/usr/bin/python
'''
Created on 04/21/1024

@author: Kaili Zhang
'''

'''
 Rules:
 1) One player vs. One dealer
 2) Deck: 52 cards
 3) Dealer should hit until >= 17
 4) Player start with 100 chips and must bet at least 1 clip each hand
 5) Initialization: Two cards for dealer, one face-down and one face-up;
                    Two cards for player, one face-down and one face-up
 6) Win: Blackjack 
         Bigger Value;
    Push: Double black jack
          Equal value;
    Bust: More than 21
 7) Hit
    Stand
    Split
8) Assistant : A function that providing advises to help you make decisions.
'''


import random, copy


class Card():
    ''' Basic Card Class '''
    def __init__(self, value=1, rank="Ace", color="Spades"):
        
        self.value = value
        self.rank = rank
        self.color = color
        # value is 1 to 10
        # rank a, 1, ... 10, j, q, k
        # color: spade, heart, club, diamond

    def __str__(self):
        return self.color + "-" + self.rank


class Deck():
    ''' Basic deck, 52 cards '''
    def __init__(self):
        self.cards = []
        # Generate 52 Cards
        colors = ['Spade','Heart','Club','Diamond']
        ranks = [('A', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
             ('J', 10), ('Q', 10), ('K', 10)]
        for r in ranks:
            for s in colors:
                c = Card()
                c.rank = r[0]
                c.value = r[1]
                c.color = s
                self.cards.append(c)

class Hand():
    ''' A blackjack hand. Hands keep track of player bets '''

    def __init__(self, bet=1):
        self.cards = []
        self.values = 0
        self.valid_moves = []
        self.bet = bet

    def add_card(self, card):
        ''' A blackjack hand. Hands keep track of player bets '''
        self.cards.append(card)
        self.update_values()
        self.update_valid_moves()

    def update_valid_moves(self):
        ''' Update valid moves '''
        moves = ['Stand']
        # case for 21
        for value in self.values:
            if value > 21:
                self.valid_moves = 'Bust'
                return
            if value == 21:
                if len(self.cards) == 2:
                    self.valid_moves = 'Blackjack'
                    return
                self.valid_moves = '21'
                return
        moves.append('Hit')

        if len(self.cards) <= 2:
            moves.append('Double')

        if len(self.cards) == 2:
            if self.cards[0].rank == self.cards[1].rank:
                moves.append('Split')

        self.valid_moves = moves

    def update_values(self):
        ''' Calculate the total value of hand '''
        v = [0]
        has_ace = 0
        # two values for hands with aces
        for card in self.cards:
            v[0] += card.value
            if card.rank == 'A':
                has_ace = True

        # hand is soft if below 12
        if has_ace:
            if v[0] < 12:
                v.append(v[0] + 10)

        self.values = v

    def __str__(self):
        handshow = ''
        for card in self.cards:
            handshow += '\n        --' + str(card)
        return handshow
    
    def dealer_show(self):
        handshow = ''
        for i in xrange(len(self.cards) - 1):
            handshow += '\n        --' + str(self.cards[i])
        handshow += '\n        --One Hidden Card'
        return handshow


class CardStack():
    ''' Here you can set the number of decks '''

    def __init__(self, num_decks=1):
        '''Build a stack and shuffle'''
        self.stack = []
        for i in range(num_decks):
            deck = Deck()
            for card in deck.cards:
                self.stack.append(card)
        # randomly shuffle the stack
        random.shuffle(self.stack)

    def draw(self):
        ''' draw a card '''
        return self.stack.pop()

    def __len__(self):
        return len(self.stack)


class Player():
    def __init__(self, chips=1000):
        self.chips = chips
        self.name = raw_input('May I have your name : ')

    def __str__(self):
        return 'Player ' + self.name

    def place_bet(self):
        print 'Player ' + self.name + '\'s Chips: ' + str(self.chips) + ' chips'
        bet = raw_input("Place your bet ('q' to quit): ")
        if bet == 'q':
            return bet

        while True:
            try:
                bet = int(bet)
                if bet < 1:
                    bet = int(raw_input('Bet must be at leats 1. Please place your bet again: '))
                elif self.chips - bet < 0:
                    bet = int(raw_input('Your funds isn\'t enough. Please place your bet again: '))
                else:
                    break
            except ValueError:
                bet = raw_input('Not a valid bet. Please place your bet again: ')

        self.chips -= bet
        print 'Chips: ' + str(self.chips)
        return bet

    # given a poker hand, returns a move
    def make_move(self, hand):
        print str(self) + ','
        moves_list = hand.valid_moves
        print 'Your Valid moves - ' + str([str(i) + ':' + move for i, move in enumerate(moves_list)])
        move = raw_input("Choose a move (e.g. '0'): ")
        while True:
            try:
                move = int(move)
                if move < 0 or move >= len(moves_list):
                    move = int(raw_input('Invalid move number. Please choose a move again: '))

                # case of double down without enough chips
                elif moves_list[move] == 'Double':
                    if self.chips < hand.bet:
                        move = int(raw_input('Chips are not enough to Double. Please choose a move again: '))
                    else:
                        self.chips -= hand.bet
                        break

                # case of split without enough chips
                elif moves_list[move] == 'Split':
                    if self.chips < hand.bet:
                        move = int(raw_input('Chips are not enough to Split. Please choose a move again: '))
                    else:
                        self.chips -= hand.bet
                        break

                else:
                    break
            except ValueError:
                move = raw_input('Invalid move number. Please choose a move again: ')
        return moves_list[move]


class Game():
    ''' Here's the main game logic '''

    def __init__(self, num_players, num_decks):
        # positions is list of players and their hands
        self.positions = []
        self.num_players = num_players
        self.num_decks = num_decks
        for i in xrange(num_players):
            self.positions.append([Player(), []])
        self.dealer = Hand()
        self.cardstack = CardStack(num_decks)
        self.chips = 0
        self.round = 0

    def play(self):
        ''' Begain to play the game '''

        print "Welcome to BlackJack Game !"
        print "Let's Start ! "

        # ------------------------------------game loop begain -------------------------
        while True:
            print "Starting a new round!\n"
            self.round += 1
            print "-------------------------Round " + str(self.round) + "-------------------------"

            # new shoe if less than one deck remaining
            if len(self.cardstack) < 52:
                self.cardstack = CardStack(self.num_decks)

            # collect bets and reset lists of players and hands
            self.dealer = Hand()
            new_positions = []
            for player, hands in self.positions:
                bet = player.place_bet()
                if bet == 'q':
                    print player, 'Quits!'
                    self.num_players -= 1
                    if self.num_players == 0:
                        print 'No more players. Game over!'
                        return
                    continue
                new_positions.append([player, [Hand(bet)]])
            self.positions = new_positions

            self.deal_cards()
            self.print_status()

            # handle dealer blackjack case
            if self.dealer.valid_moves == 'Blackjack':
                print 'Dealer BlackJack ! Bad Luck :('
                for player, hands in self.positions:
                    # push on player blackjack
                    if hands[0].valid_moves == 'Blackjack':
                        player.chips += hands[0].bet
                        print str(player) + ' pushes on dealer blackjack.'
                continue

            # go through players' hands and take moves
            standing_hands = []
            for player, hands in self.positions:
                for hand in hands:

                    # loop until 21, bust, or stand
                    while True:
                        # check for 21 or blackjack
                        if hand.valid_moves == 'Blackjack':
                            print "\n\n!!! Congratulations !!!"
                            print str(player) + ' has blackjack and wins ' + str(2 * hand.bet) + ' chips! Congratulations!'
                            player.chips += 2 * hand.bet
                            break
                        if hand.valid_moves == '21':
                            print str(player) + ' has 21'
                            standing_hands.append([player, hand])
                            break

                        # if not 21, then get player move
                        selected_move = player.make_move(copy.deepcopy(hand))
                        if selected_move == 'Stand':
                            if len(hand.values) == 2:
                                print '\n ' + str(player) + ' stands on soft ' + str(hand.values[1])
                            else:
                                print '\n ' + str(player) + ' stands on ' + str(hand.values[0])
                            standing_hands.append([player, hand])
                            break
                        if selected_move == 'Hit':
                            new_card = self.cardstack.draw()
                            print player, 'hits and draws a', new_card
                            hand.add_card(new_card)
                            self.print_status()
                            if hand.valid_moves == 'Bust':
                                print '!!! Bust !!!'
                                break
                        if selected_move == 'Double':
                            new_card = self.cardstack.draw()
                            print player, 'doubles down and draws a', new_card
                            hand.add_card(new_card)
                            hand.bet *= 2
                            if hand.valid_moves == 'Bust':
                                print '!!! Bust !!!'
                                break
                            print str(player) + ' ends on ' + str(max(hand.values))
                            standing_hands.append([player, hand])
                            break

                        # for splits, make two new Hands and insert them after the current hand
                        if selected_move == 'Split':
                            print player, ' splits on two ', str(hand.cards[0].rank)
                            index = hands.index(hand) + 1
                            hand1 = Hand(hand.bet)
                            hand1.add_card(hand.cards[0])
                            hand2 = Hand(hand.bet)
                            hand2.add_card(hand.cards[1])
                            hands.insert(index, hand2)
                            hands.insert(index, hand1)
                            break
            self.print_status()
            # if no more players, start new round
            if not standing_hands:
                continue

            # dealer's turn
            while True:
                is_dealer_soft = False
                if len(self.dealer.values) == 2:
                    is_dealer_soft = True
                    dealer_value = self.dealer.values[1]
                else:
                    dealer_value = self.dealer.values[0]

                # stand if more than 17 or hard 17
                if dealer_value > 17 or (dealer_value == 17 and is_dealer_soft is False):
                    break

                # hits on soft 17
                else:
                    card = self.cardstack.draw()
                    self.dealer.add_card(card)
                    print 'Dealer hits and draws a ' + str(card)

            # if dealer busts, then all standing hands win
            is_dealer_busted = False
            if self.dealer.valid_moves == 'Bust':
                print 'Dealer busts!'
                print str(self.dealer)
                is_dealer_busted = True
            else:
                print 'Dealer has hand: ' + self.dealer.dealer_show()
                #print 'Dealer stands on ' + str(dealer_value)
            for player, hand in standing_hands:
                # win
                if is_dealer_busted or max(hand.values) > max(self.dealer.values):
                    player.chips += 2 * hand.bet
                    print "\n\n!!! Congratulations !!!"
                    print str(player) + ' wins ' + str(2 * hand.bet) + ' chips with hand: ' + str(hand)
                # push
                elif max(hand.values) == max(self.dealer.values):
                    player.chips += hand.bet
                    print "\n\n!!! Congratulations !!!"
                    print str(player) + ' pushes with hand: ' + str(hand) + ' \n Wins ' + str(hand.bet) + ' back'
                # loss
                else:
                    print str(player) + ' loses with hand: ' + str(hand)
            print '\nEnd of round.\n\n'

    def deal_cards(self):
        ''' Deal initial cards following casino order '''
        for i in xrange(2):
            for player, hands in self.positions:
                hands[0].add_card(self.cardstack.draw())
            self.dealer.add_card(self.cardstack.draw())

    def print_status(self):
        ''' Print player hands, then print dealer hand '''

        for player, hands in self.positions:
            print '>>>> Player ' + player.name
            for i, hand in enumerate(hands):
                print '        Hand ' + str(i) + ': ' + str(hand)
            print '\n'
        print '#### Dealer: ' + self.dealer.dealer_show()
        print '\n'
        
        
def mainGame():
    num_players = raw_input("Please input the number of Players: ")
    while True:
        try:
            num_players = int(num_players)
            if num_players < 0:
                num_players = raw_input("Invalid number. Please input the number of Players: ")
            else:
                break
        except ValueError:
            num_players = raw_input("Invalid number. Please input the number of Players: ")
    num_decks = raw_input("Please input the number of Decks used: ")
    while True:
        try:
            num_decks = int(num_decks)
            if num_decks < 0:
                num_decks = raw_input("Invalid number. Please input the number of Decks used: ")
            else:
                break
        except ValueError:
            num_decks = raw_input("Invalid number. Please input the number of Decks used: ")
    game = Game(num_players, num_decks)
    game.play()
    

if __name__ == "__main__":
    mainGame()
    
    