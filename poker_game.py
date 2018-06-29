#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 20:16:54 2018

@author: brianwon

Poker Game
"""

import sys
import numpy as np

def parse_arguments():
    arguments = sys.argv[1:]
    return arguments

class Player:
    def __init__(self, name, hand, type_of_hand=1, high_card=0):
        self.name = name
        self.hand = hand
        self.type_of_hand = type_of_hand
        self.high_card = high_card
        self.type_high_card = 0
        
    def set_highcard(self, hand):
        other_cards = []
        card_in_order = np.sort(hand)
        card_num = np.sort(hand // 4)
        num_occur = np.arange(5)
        index = 0
        for num in card_num:
            num_occur[index] = sum(card_num == num)
            index += 1
        if self.type_of_hand == 1 or self.type_of_hand == 5 or self.type_of_hand == 6:
            self.high_card = np.amax(hand)
            self.type_high_card = self.high_card
        elif self.type_of_hand == 2 or self.type_of_hand == 3:
            for index in np.arange(5):
                if num_occur[index] == 1:
                    other_cards.append(card_num[index])
                elif num_occur[index] == 2 and card_in_order[index] > self.type_high_card:
                    self.type_high_card = card_in_order[index]
            self.high_card = max(other_cards)
        elif self.type_of_hand == 4 or self.type_of_hand == 7:
            for index in np.arange(5):
                if num_occur[index] == 3 and card_in_order[index] > self.type_high_card:
                    self.type_high_card = card_in_order[index]
        elif self.type_of_hand == 8:
            if num_occur[0] == 1:
                self.high_card = card_in_order[0]
                self.type_high_card = card_in_order[4]
            elif num_occur[4] == 1:
                self.high_card = card_in_order[4]
                self.type_high_card = card_in_order[0]
                
            
        
    def set_handtype(self, hand):
        self.type_of_hand = type_hand(hand)
        
    def __gt__(self, other):
        if self.type_of_hand == other.type_of_hand and self.type_high_card == other.type_high_card:
            return(self.high_card > other.high_card)
        elif self.type_of_hand == other.type_of_hand:
            return(self.type_high_card > other.type_high_card)
        else:
            return(self.type_of_hand > other.type_of_hand)
        
        
def gen_hands():
    return(np.random.choice(52, 52, replace=False))
    
def type_hand(hand):
    card_num = np.sort(hand // 4)
    card_suits = hand % 4
    num_occur = np.arange(5)
    index = 0
    for num in card_num:
        num_occur[index] = sum(card_num == num)
        index += 1
    suit_occur = np.arange(5)
    index = 0
    for suit in card_suits:
        suit_occur[index] = sum(card_suits == suit)
        index += 1
    check_str8 = card_num - card_num[0]
    check_kind = np.sort(num_occur)
    if suit_occur[0] == 5:
        return(6) # 6 = flush
    elif check_str8[0]==0 and check_str8[1]==1 and check_str8[2]==2 and check_str8[3]==3 and check_str8[4]==4:
        return(5) # 5 = straight
    elif check_kind[1] == 4:
        return(8) # 8 = four of kind
    elif check_kind[0] == 2 and check_kind[2] == 3:
        return(7) # 7 = house
    elif check_kind[2] == 3:
        return(4) # 4 = three of a kind
    elif sum(check_kind == 2) == 4:
        return(3) # 3 = two pair
    elif sum(check_kind == 2) == 2:
        return(2) # 2 = one pair
    else:
        return(1) # 1 = high card
        
cardnum = {
        0: 2,
        1: 3,
        2: 4,
        3: 5,
        4: 6,
        5: 7,
        6: 8,
        7: 9,
        8: 10,
        9: 'J',
        10: 'Q',
        11: 'K',
        12: 'A'
        }

suits = {
        0: 'diamond',
        1: 'club',
        2: 'heart',
        3: 'spade'
        }
    

def poker(num_players):
    players = [None] * num_players
    names = [None] * num_players
    player_num = 1
    player = 0
    card_shuff = gen_hands()
    while player < num_players:
        name = input('Player ' + str(player_num) + ', what is your name? ')
        names[player] = name
        players[player] = Player(name, card_shuff[(5*player):(5*player_num)])
        players[player].set_highcard(players[player].hand)
        players[player].set_handtype(players[player].hand)
        player += 1
        player_num += 1
    for guy in players:
        card_num = guy.hand // 4
        card_suits = guy.hand % 4
        hand_str = ''
        card_index = 0
        while card_index < 5:
            hand_str += str(cardnum[card_num[card_index]]) + str(suits[card_suits[card_index]]) + ' '
            card_index += 1
        print(str(guy.name) + ', your hand is: ' + hand_str)
    besthand = players[0]
    for guy in players:
        if guy > besthand:
            besthand = guy
    print(besthand.name + ' wins!')

if __name__ == "__main__":
    # This code will only be executed if this file is called from the terminal directly
    num = int(parse_arguments()[0])
    poker(num)