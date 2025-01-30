"""Estimate the expected value of a given strategy."""
from __future__ import annotations

import argparse
import inspect
import logging
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import os
import pandas as pd
import random
from typing import Iterable

from utils import get_args_info, get_cards_seen, get_hilo_running_count, DECK, readable_number
from action_strategies import BaseMover
from betting_strategies import BaseBetter
import betting_strategies
import action_strategies


class Hand:
    """Hold information about the hand of the player and the dealer."""

    def __init__(self, cards: Iterable[int]) -> None:
        """
        Save the initial cards.

        :param cards: The cards the hand started with.
        """
        self.cards = list(cards)

    def add_card(self, card: int) -> None:
        """
        Add a new card to the hand.

        :param card: The new card to add for the hand (an ace is symbolised as 11).
        """
        self.cards.append(card)

    def value_ace(self) -> tuple[int, int]:
        """
        Return the value of a hand and how many aces that count as 11 it has.

        :return: The hand's value and how many aces are counted as 11 (0 or 1).
        """
        value = sum(self.cards)
        aces = self.cards.count(11)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value, aces

    def aces(self) -> int:
        """
        Return the number of aces that count as 11.

        :return: The number of aces counted as 11.
        """
        return self.value_ace()[1]

    def value(self) -> int:
        """
        Return the value of a hand.

        :return: The hand's value.
        """
        return self.value_ace()[0]


def get_card_from_shoe(shoe: list[int]) -> int:
    """
    Get a card from the shoe. Always returns the last item from the shoe, so the shoe must be shuffled before.

    :param shoe: The shoe to get a card from.
    :return: The card we got from the shoe.
    """
    card = shoe.pop()
    return card


def get_mover_and_better(mover_name: str, better_name: str
                         ) -> tuple[action_strategies.BaseMover, betting_strategies.BaseBetter]:
    """
    Get the mover and the better from the arguments passed by the user.

    :param mover_name: The name of the mover to use. If it isn't one of the recognized names,
        then in checks if there is a class of that name.
    :param better_name: The name of the better to use. If it isn't one of the recognized names,
        then in checks if there is a class of that name.
    :return: The mover and the better to use, already set up.
    """
    mover_class: action_strategies.BaseMover
    better_class: betting_strategies.BaseBetter
    if mover_name == "card-count":
        mover_class = action_strategies.CardCountMover(
            {(-1000, -10): "data/s17/6deck_s17_das_peek_tc_minus_10.csv",
             (-10, -9): "data/s17/6deck_s17_das_peek_tc_minus_9.csv",
             (-9, -8): "data/s17/6deck_s17_das_peek_tc_minus_8.csv",
             (-8, -7): "data/s17/6deck_s17_das_peek_tc_minus_7.csv",
             (-7, -6): "data/s17/6deck_s17_das_peek_tc_minus_6.csv",
             (-6, -5): "data/s17/6deck_s17_das_peek_tc_minus_5.csv",
             (-5, -4): "data/s17/6deck_s17_das_peek_tc_minus_4.csv",
             (-4, -3): "data/s17/6deck_s17_das_peek_tc_minus_3.csv",
             (-3, -2): "data/s17/6deck_s17_das_peek_tc_minus_2.csv",
             (-2, -1): "data/s17/6deck_s17_das_peek_tc_minus_1.csv",
             (-1, 1): "data/s17/6deck_s17_das_peek_tc_0.csv",
             (1, 2): "data/s17/6deck_s17_das_peek_tc_plus_1.csv",
             (2, 3): "data/s17/6deck_s17_das_peek_tc_plus_2.csv",
             (3, 4): "data/s17/6deck_s17_das_peek_tc_plus_3.csv",
             (4, 5): "data/s17/6deck_s17_das_peek_tc_plus_4.csv",
             (5, 6): "data/s17/6deck_s17_das_peek_tc_plus_5.csv",
             (6, 7): "data/s17/6deck_s17_das_peek_tc_plus_6.csv",
             (7, 8): "data/s17/6deck_s17_das_peek_tc_plus_7.csv",
             (8, 9): "data/s17/6deck_s17_das_peek_tc_plus_8.csv",
             (9, 10): "data/s17/6deck_s17_das_peek_tc_plus_9.csv",
             (10, 1000): "data/s17/6deck_s17_das_peek_tc_plus_10.csv"})
    elif mover_name == "basic-strategy-deviations":
        mover_class = action_strategies.BasicStrategyDeviationsMover("data/s17/6deck_s17_das_peek_basic_strategy.csv")
    elif mover_name == "basic-strategy":
        mover_class = action_strategies.BasicStrategyMover("data/s17/6deck_s17_das_peek_basic_strategy.csv")
    elif mover_name == "perfect":
        mover_class = action_strategies.PerfectMover()
    elif mover_name == "simple":
        mover_class = action_strategies.SimpleMover()
    else:  # Run a user-defined class.
        mover_class = getattr(action_strategies, mover_name)()
    if better_name == "card-count":
        better_class = betting_strategies.CardCountBetter()
    elif better_name == "simple":
        better_class = betting_strategies.SimpleBetter()
    else:  # Run a user-defined class.
        better_class = getattr(betting_strategies, better_name)()
    return mover_class, better_class


def play_dealer(dealer_cards: Iterable[int], shoe: list[int], dealer_stands_soft_17: bool) -> int:
    """
    Play the dealers hand to get its final value.

    :param dealer_cards: The cards the dealer already has.
    :param shoe: The shoe.
    :param dealer_stands_soft_17: Whether the dealer stands on soft 17.
    :return: The final value of the dealer's hand. If the dealer busted, the value is 0.
    """
    dealer = Hand(dealer_cards)
    while dealer.value() < 17 or not dealer_stands_soft_17 and dealer.value() == 17 and dealer.aces():
        dealer.add_card(get_card_from_shoe(shoe))
    dealer_value = dealer.value()
    logging.debug("dealer cards are: {}".format(dealer.cards))
    logging.debug("dealer_value = {}".format(dealer_value))
    return dealer_value if dealer_value <= 21 else 0


def play_hand(action_class: action_strategies.BaseMover,
              hand_cards: list[list[int]], dealer_up_card: int, dealer_down_card: int, shoe: list[int],
              splits_remaining: int, deck_number: int, dealer_peeks_for_blackjack: bool = True, das: bool = True,
              dealer_stands_soft_17: bool = True) -> list[list[int]]:
    """
    Play hands but don't play the dealer.

    :param action_class: The class that chooses the action.
    :param hand_cards: The cards in our hand.
    :param dealer_up_card: The dealer's up card.
    :param dealer_down_card: The dealer's down card.
    :param shoe: The shoe.
    :param splits_remaining: How many more splits we can do.
    :param deck_number: The number of decks in the initial shoe.
    :param dealer_peeks_for_blackjack: Whether the dealer peeks for blackjack.
    :param das: Whether we can double after splitting.
    :param dealer_stands_soft_17: Whether the dealer stands on soft 17.
    :return: The hands played out.
    """
    done_hands = []
    for hand_index, cards in enumerate(hand_cards):
        if Hand(cards).value() > 21:
            done_hands.append(cards)
            continue
        can_split = (splits_remaining > 0 and len(cards) == 2 and cards[0] == cards[1]
                     and (not cards[0] == 11 or splits_remaining == 3))
        can_double = len(cards) == 2 and (das or splits_remaining == 3)
        cards_seen = get_cards_seen(deck_number, shoe)
        cards_seen.remove(dealer_down_card)
        hand = Hand(cards)
        initial_hand_value, initial_hand_has_ace = hand.value_ace()
        action, insure = action_class.get_move(initial_hand_value, bool(initial_hand_has_ace), dealer_up_card,
                                               can_double,
                                               can_split, False, False, cards, cards_seen, deck_number,
                                               dealer_peeks_for_blackjack, das, dealer_stands_soft_17)

        if action == "s":
            logging.debug("[play_hand] player stands.")
            done_hands.append(cards)

        elif action == "d" and can_double:
            card = get_card_from_shoe(shoe)
            hand.add_card(card)
            logging.debug("[play_hand] player doubles down and gets card {}. Current hand is {}.".format(card, hand.cards))
            done_hands.append(hand.cards)
            done_hands.append(hand.cards)  # Add the same hand twice instead of doubling the bet.

        elif action == "h":
            card = get_card_from_shoe(shoe)
            hand.add_card(card)
            logging.debug("[play_hand] player hits and gets card {}. Current hand is {}.".format(card, hand.cards))
            done_hands.append(play_hand(action_class, [hand.cards], dealer_up_card, dealer_down_card, shoe,
                                        0, deck_number, dealer_peeks_for_blackjack, das,
                                        dealer_stands_soft_17)[0])

        elif action == "p" and can_split:
            hand1 = Hand([hand.cards[0]])
            hand2 = Hand([hand.cards[1]])
            card1 = get_card_from_shoe(shoe)
            hand1.add_card(card1)
            logging.debug("[play_hand] player splits and gets card {} for the 1st hand. Current hand is {}.".format(card1, hand1.cards))
            done_hands.extend(play_hand(action_class, [hand1.cards] + hand_cards[hand_index + 1:],
                                        dealer_up_card, dealer_down_card, shoe, splits_remaining - 1, deck_number,
                                        dealer_peeks_for_blackjack, das, dealer_stands_soft_17))
            card2 = get_card_from_shoe(shoe)
            hand2.add_card(card2)
            logging.debug("[play_hand] player splits and gets card {} for the 2nd hand. Current hand is {}.".format(card2, hand2.cards))
            done_hands.extend(play_hand(action_class, [hand2.cards] + hand_cards[hand_index + 1:],
                                        dealer_up_card, dealer_down_card, shoe, splits_remaining - 1, deck_number,
                                        dealer_peeks_for_blackjack, das, dealer_stands_soft_17))
            break

        else:
            raise ValueError(f"invalid action: {action}.")
    logging.debug("[play_hand] done. return with hands = {}".format(done_hands))
    return done_hands


def simulate_hand(action_class: action_strategies.BaseMover,
                  cards: list[int], dealer_up_card: int,
                  dealer_down_card: int, shoe: list[int],
                  splits_remaining: int, deck_number: int, dealer_peeks_for_blackjack: bool = True, das: bool = True,
                  dealer_stands_soft_17: bool = True, surrender_allowed: bool = False) -> float:
    """
    Play one hand.

    :param action_class: The class that chooses the action.
    :param cards: The cards in our hand.
    :param dealer_up_card: The dealer's up card.
    :param dealer_down_card: The dealer's down card.
    :param shoe: The shoe.
    :param splits_remaining: How many more splits we can do.
    :param deck_number: The number of decks in the initial shoe.
    :param dealer_peeks_for_blackjack: Whether the dealer peeks for blackjack.
    :param das: Whether we can double after splitting.
    :param dealer_stands_soft_17: Whether the dealer stands on soft 17.
    :param surrender_allowed: Whether the game rules allow surrendering.
    :return: The profit/loss from the hand, and how many times we split.
    """
    can_split = (splits_remaining > 0 and len(cards) == 2 and cards[0] == cards[1]
                 and (not cards[0] == 11 or splits_remaining == 3))
    can_double = len(cards) == 2 and (das or splits_remaining == 3)
    can_surrender_now = surrender_allowed
    can_insure = dealer_up_card == 11
    insurance_profit = 0.
    dealer_has_blackjack = dealer_up_card + dealer_down_card == 21
    player_has_blackjack = cards[0] + cards[1] == 21
    player_loses_all_bets = dealer_has_blackjack and not dealer_peeks_for_blackjack and not player_has_blackjack
    cards_seen = get_cards_seen(deck_number, shoe)
    cards_seen.remove(dealer_down_card)
    hand = Hand(cards)
    initial_hand_value, initial_hand_has_ace = hand.value_ace()
    action, insure = action_class.get_move(initial_hand_value, bool(initial_hand_has_ace), dealer_up_card, can_double,
                                           can_split, can_surrender_now, can_insure, cards, cards_seen, deck_number,
                                           dealer_peeks_for_blackjack, das, dealer_stands_soft_17)

    if insure and can_insure:
        logging.debug("play takes insurance.")
        insurance_profit = 1 if dealer_down_card == 10 else -.5

    if dealer_peeks_for_blackjack:
        if dealer_has_blackjack and player_has_blackjack:  # Push
            logging.debug("dealer and player get natural blackjack. Push...")
            return 0 + insurance_profit
        elif dealer_has_blackjack:  # Dealer blackjack
            logging.debug("dealer gets natural blackjack. Player loses...")
            return -1 + insurance_profit
        elif player_has_blackjack:  # Player blackjack
            logging.debug("players gets natural blackjack. Player wins 3 to 2...")
            return 1 * 3 / 2 + insurance_profit
    else:
        if player_has_blackjack and dealer_has_blackjack:
            logging.debug("dealer and player get natural blackjack (no peeking). Push...")
            return 0 + insurance_profit
        elif player_has_blackjack:
            logging.debug("players gets natural blackjack (no peeking). Player wins 3 to 2...")
            return 1 * 3 / 2 + insurance_profit

    if action == "u" and can_surrender_now:
        logging.debug("player surrenders...")
        return -.5 + insurance_profit

    elif action == "s":
        logging.debug("player stands...")
        dealer_value = play_dealer((dealer_up_card, dealer_down_card), shoe, dealer_stands_soft_17)
        if player_loses_all_bets:
            logging.debug("player loses: {} to {}".format(initial_hand_value, dealer_value))
            return -1 + insurance_profit
        if initial_hand_value > dealer_value:
            logging.debug("player wins: {} to {}".format(initial_hand_value, dealer_value))
            return 1 + insurance_profit
        elif initial_hand_value < dealer_value:
            logging.debug("player loses: {} to {}".format(initial_hand_value, dealer_value))
            return -1 + insurance_profit
        logging.debug("push: {} to {}".format(initial_hand_value, dealer_value))
        return 0 + insurance_profit

    elif action == "d" and can_double:
        card = get_card_from_shoe(shoe)
        logging.debug("player doubling... get card {}".format(card))
        hand.add_card(card)
        if player_loses_all_bets:
            logging.debug("player loses all bets")
            return -2 + insurance_profit
        if hand.value() > 21:
            logging.debug("player busted at {}".format(hand.value()))
            return -2 + insurance_profit
        dealer_value = play_dealer((dealer_up_card, dealer_down_card), shoe, dealer_stands_soft_17)
        if hand.value() > dealer_value:
            logging.debug("player wins {} to {}".format(hand.value(), dealer_value))
            return +2 + insurance_profit
        elif hand.value() < dealer_value:
            logging.debug("player loses {} to {}".format(hand.value(), dealer_value))
            return -2 + insurance_profit
        logging.debug("push {} to {}".format(hand.value(), dealer_value))
        return 0 + insurance_profit

    elif action == "h":
        card = get_card_from_shoe(shoe)
        hand.add_card(card)
        logging.debug("player hits ... get new card {}. Hand is {}".format(card, hand.cards))
        if player_loses_all_bets:
            logging.debug("player loses all bets")
            return -1 + insurance_profit
        if hand.value() > 21:
            logging.debug("player busted at {}".format(hand.value()))
            return -1 + insurance_profit
        hand_cards = play_hand(action_class, [hand.cards], dealer_up_card, dealer_down_card, shoe,
                               splits_remaining, deck_number, dealer_peeks_for_blackjack, das, dealer_stands_soft_17)[0]
        hand = Hand(hand_cards)
        logging.debug("player keeps hitting. hand is {}".format(hand.cards))
        if hand.value() > 21:
            logging.debug("player busted: {}".format(hand.value()))
            return -1 + insurance_profit
        dealer_value = play_dealer((dealer_up_card, dealer_down_card), shoe, dealer_stands_soft_17)
        if dealer_value > hand.value():
            logging.debug("player gets beat {} to {}".format(hand.value(), dealer_value))
            return -1 + insurance_profit
        elif hand.value() > dealer_value:
            logging.debug("player wins {} to {}".format(hand.value(), dealer_value))
            return 1 + insurance_profit
        logging.debug("push: {} to {}".format(hand.value(), dealer_value))
        return 0 + insurance_profit

    elif action == "p" and can_split:
        hand1 = Hand([hand.cards[0]])
        hand2 = Hand([hand.cards[1]])
        if hand.cards[0] == 11:
            logging.debug("current 10 cards of the shoe: {}".format(shoe[-10:]))
            card = get_card_from_shoe(shoe)
            hand1.add_card(card)
            logging.debug("player splits AA: first new card = {}. Hand is {}".format(card, hand1.cards))
            card = get_card_from_shoe(shoe)
            hand2.add_card(card)
            logging.debug("player splits AA: 2nd new card = {}. Hand is {}".format(card, hand2.cards))
            if player_loses_all_bets:
                logging.debug("player loses all bets AA")
                return -2 + insurance_profit
            dealer_value = play_dealer((dealer_up_card, dealer_down_card), shoe, dealer_stands_soft_17)
            split_profit = 0
            if hand1.value() > 21 or dealer_value > hand1.value():
                logging.debug("player AA 1st hand busted or gets beat {} to {}".format(hand1.value(), dealer_value))
                split_profit -= 1
            elif hand1.value() > dealer_value:
                logging.debug("player AA 1st hand wins {} to {}".format(hand1.value(), dealer_value))
                split_profit += 1
            if hand2.value() > 21 or dealer_value > hand2.value():
                logging.debug("player AA 2nd hand busted or gets beat {} to {}".format(hand2.value(), dealer_value))
                split_profit -= 1
            elif hand2.value() > dealer_value:
                logging.debug("player AA 2nd hand wins {} to {}".format(hand2.value(), dealer_value))
                split_profit += 1
            return split_profit + insurance_profit
        logging.debug("current 10 cards of the shoe: {}".format(shoe[-10:]))
        card1 = get_card_from_shoe(shoe)
        hand1.add_card(card1)
        logging.debug("1st card is popped. Card = {}. Hands = {}. remaining shoe = {}".format(card1, hand1.cards, shoe[-10:]))
        logging.debug("player split non-AA, 1st hand gets {}".format(card1))
        hand1_all = play_hand(action_class, [hand1.cards], dealer_up_card, dealer_down_card, shoe,
                              splits_remaining - 1, deck_number, dealer_peeks_for_blackjack, das, dealer_stands_soft_17)
        card2 = get_card_from_shoe(shoe)
        hand2.add_card(card2)
        logging.debug("2nd card is popped. Card = {}. Hands = {}. remaining shoe = {}".format(card2, hand2.cards, shoe[-10:]))
        logging.debug("player split non-AA, 2nd hand gets {}".format(card2))
        hand2_all = play_hand(action_class, [hand2.cards], dealer_up_card, dealer_down_card, shoe,
                              splits_remaining - 1, deck_number, dealer_peeks_for_blackjack, das, dealer_stands_soft_17)
        all_hands = hand1_all + hand2_all
        if player_loses_all_bets:
            logging.debug("player loses all bets")
            return -len(all_hands) + insurance_profit

        split_profit = 0
        busted_counter = 0
        for hand_cards in all_hands:
            if hand.value() > 21:
                logging.debug("player busted {} to {}".format(hand.value(), dealer_value))
                split_profit -= 1
                busted_counter += 1
        if busted_counter == len(all_hands):
            return split_profit + insurance_profit

        logging.debug("player all hands are done. {} hands are: {}".format(len(all_hands), all_hands))
        dealer_value = play_dealer((dealer_up_card, dealer_down_card), shoe, dealer_stands_soft_17)        
        for hand_cards in all_hands:
            hand = Hand(hand_cards)
            if hand.value() > 21 or dealer_value > hand.value():
                logging.debug("player busted or gets beaten {} to {}".format(hand.value(), dealer_value))
                split_profit -= 1
            elif hand.value() > dealer_value:
                logging.debug("player wins {} to {}".format(hand.value(), dealer_value))
                split_profit += 1
            else:
                logging.debug("push: {} to {}".format(hand.value(), dealer_value))
                pass
        return split_profit + insurance_profit

    raise ValueError(f"invalid action: {action}.")

# @profile
def expected_value(action_class: action_strategies.BaseMover, betting_class: betting_strategies.BaseBetter,
                   simulations: int, deck_number: int = 6, shoe_penetration: float = .25,
                   dealer_peeks_for_blackjack: bool = True, das: bool = True,
                   dealer_stands_soft_17: bool = True, surrender_allowed: bool = True,
                   units: int = 200, hands_played: int = 1000,
                   num_of_other_players: int = 0) -> tuple[float, float, float, float]:
    """
    Estimate the expected value of a strategy.

    :param action_class: The class that chooses the action.
    :param betting_class: The class that chooses the bet.
    :param simulations: How many hands to play.
    :param deck_number: The number of decks in the initial shoe.
    :param shoe_penetration: When to reshuffle the shoe. Reshuffles when cards remaining < starting cards * deck penetration.
    :param dealer_peeks_for_blackjack: Whether the dealer peeks for blackjack.
    :param das: Whether we can double after splitting.
    :param dealer_stands_soft_17: Whether the dealer stands on soft 17.
    :param surrender_allowed: Whether the game rules allow surrendering.
    :param units: The number of units in total.
    :param hands_played: How many hands to play before checking the risk of ruin.
    :param num_of_other_players: number of players in front of us on the same table, ranging from 0 to 4.
    

    :return: The total return, the average return of a game, the average bet size, and the risk of ruin.
    """
    if num_of_other_players < 0 or num_of_other_players > 4:
        raise NotImplementedError("num_of_other_players = {}".format(num_of_other_players))

    starting_shoe = DECK * deck_number
    starting_number = len(starting_shoe)
    reshuffle_at = int(starting_number * shoe_penetration)
    shoe = starting_shoe.copy()
    random.shuffle(shoe)
    
    bets = []
    reward_record = [] # record reward at the end of every hand
    tc_record = [] # record tc at the beginning of every hand

    for i in range(simulations):
        if i % 10_000 == 0:
            print(f"Games played: {readable_number(i)}/{readable_number(simulations)}")
        cards_seen = []
        logging.debug("=" * 70)
        logging.debug("new shoe starting...")
        logging.debug("params:")
        current_frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(current_frame)
        for arg in args:
            logging.debug("{}: {}".format(arg, values[arg]))
        logging.debug("shoe: {}".format(shoe))
        logging.debug("=" * 70)
        while len(shoe) >= reshuffle_at:
            cards_seen = get_cards_seen(deck_number, shoe)
            run_count = get_hilo_running_count(cards_seen)
            true_count = run_count / (len(shoe) / 52.0)
            logging.debug("current shoe: {}".format(shoe[-10:]))
            logging.debug("running count: {}".format(run_count))
            logging.debug("true count: {}".format(true_count))
            tc_record.append(true_count)
            initial_bet = betting_class.get_bet(cards_seen, deck_number)
            logging.debug("initial bet: {}".format(initial_bet))
            for op in range(num_of_other_players):
                get_card_from_shoe(shoe)
            player_card_1 = get_card_from_shoe(shoe)
            dealer_up_card = get_card_from_shoe(shoe)
            for op in range(num_of_other_players):
                get_card_from_shoe(shoe)
            player_card_2 = get_card_from_shoe(shoe)
            dealer_down_card = get_card_from_shoe(shoe)
            player_cards = [player_card_1, player_card_2]
            cards_seen = get_cards_seen(deck_number, shoe)
            cards_seen.remove(dealer_down_card)
            # TODO: other players act based on basic strategy.
            reward = simulate_hand(action_class, player_cards, dealer_up_card,
                                   dealer_down_card, shoe, 3, deck_number,
                                   dealer_peeks_for_blackjack, das, dealer_stands_soft_17, surrender_allowed)
            reward *= initial_bet
            logging.debug("reward: {}".format(reward))
            reward_record.append(reward)
            bets.append(initial_bet)
        
        shoe = starting_shoe.copy()
        random.shuffle(shoe)
    
    return bets, reward_record, tc_record


def _ev_mt_wrapper(action_class: action_strategies.BaseMover = None, betting_class: betting_strategies.BaseBetter = None,
          total_simulations: int = 100, deck_number: int = 6, shoe_penetration: float = .25,
          dealer_peeks_for_blackjack: bool = True, das: bool = True,
          dealer_stands_soft_17: bool = True, surrender_allowed: bool = True,
          units: int = 200, hands_played: int = 1000, num_of_other_players: int = 0,
          mt_idx=None, result_dict = None):

    b, r, c = expected_value(action_class, betting_class, total_simulations, deck_number, shoe_penetration,
                  dealer_peeks_for_blackjack, das, dealer_stands_soft_17, surrender_allowed,
                  units, hands_played, num_of_other_players)
    result_dict[mt_idx] = [b, r, c]


def ev_mt(cores=2, action_class: action_strategies.BaseMover = None, betting_class: betting_strategies.BaseBetter = None,
          total_simulations: int = 100, deck_number: int = 6, shoe_penetration: float = .25,
          dealer_peeks_for_blackjack: bool = True, das: bool = True,
          dealer_stands_soft_17: bool = True, surrender_allowed: bool = True,
          units: int = 200, hands_played: int = 1000, num_of_other_players: int = 0):
    
    processes = []
    return_dict = multiprocessing.Manager().dict()
    for i in range(cores):
        p = multiprocessing.Process(
            target=_ev_mt_wrapper, 
            args=(action_class, betting_class, total_simulations//cores, deck_number, shoe_penetration,
                  dealer_peeks_for_blackjack, das, dealer_stands_soft_17, surrender_allowed,
                  units, hands_played, num_of_other_players, i, return_dict,),
            name="ev_mt_{}".format(i))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    
    bets = []
    rewards = []
    tcs = []
    for i in range(cores):
        cres = return_dict.get(i)
        bets += cres[0]
        rewards += cres[1]
        tcs += cres[2]
    return bets, rewards, tcs
        

def calculate_sum_in_chunks(values, chunk_size=100):
    # Split the list into chunks of size 'chunk_size'
    chunks = [values[i:i + chunk_size] for i in range(0, len(values), chunk_size)]
    res = []
    for chunk in chunks:
        # Convert to numpy array for calculation
        np_chunk = np.array(chunk)
        res.append(np.sum(np_chunk))
    return res

def calc_ror(ev, sd, bankroll):
    if sd == 0 or (1 + ev/sd) == 0:
        return np.nan
    return ((1 - ev/sd) / (1 + ev/sd)) ** (bankroll / sd)

def calculate_max_drawdown_and_duration(pnl_series):
    # Convert PnL to cumulative returns
    cumulative_returns = np.cumsum(pnl_series)
    
    # Calculate the running maximum
    running_max = np.maximum.accumulate(cumulative_returns)
    
    # Drawdown is the difference between running max and current value
    drawdowns = running_max - cumulative_returns
    
    # Maximum Drawdown
    max_drawdown = np.max(drawdowns)
    
    # Find the index where max drawdown occurs
    max_drawdown_index = np.argmax(drawdowns)
    
    # Find the index where the peak before max drawdown occurred
    peak_index = np.argmax(cumulative_returns[:max_drawdown_index + 1])
    
    # Duration of max drawdown is from peak to trough
    drawdown_duration = max_drawdown_index - peak_index + 1  # +1 for inclusive count
    
    return max_drawdown, drawdown_duration

def run(mover: action_strategies.BaseMover, better: betting_strategies.BaseBetter,
        total_simulations: int, cores: int = 2, deck_number: int = 6, shoe_penetration: float = .25,
        dealer_peeks_for_blackjack: bool = True, das: bool = True,
        dealer_stands_soft_17: bool = True, surrender_allowed: bool = True,
        units: int = 200, hands_played: int = 1000, num_of_other_players: int = 0,
        plot=True):
    logging.info("expected_value.run() is called with the following configurations:")
    logging.info(get_args_info())
    if cores > 1:
        bets, rewards, tcs = ev_mt(
            cores, mover, better, total_simulations, deck_number, shoe_penetration,
            dealer_peeks_for_blackjack, das, dealer_stands_soft_17, surrender_allowed, units, hands_played, num_of_other_players
            )
    else:
        bets, rewards, tcs = expected_value(
            mover, better, simulations=total_simulations, deck_number=deck_number, shoe_penetration=shoe_penetration,
            dealer_peeks_for_blackjack=dealer_peeks_for_blackjack, das=das, dealer_stands_soft_17=dealer_stands_soft_17, 
            surrender_allowed=surrender_allowed, units=units, hands_played=hands_played, num_of_other_players=num_of_other_players
            )

    summary = {"shoes": total_simulations,
               "hands_per_shoe": len(bets) / total_simulations,
               "avg_bet": np.nan, "win_2_lose": np.nan,
               "ev_per_shoe": np.nan, "ev_per_100": np.nan, "std_per_shoe": np.nan,
               "std_per_100": np.nan, "max_dd": np.nan, "dd_duration_in_hands": np.nan,
               "risk_of_ruin": np.nan}
    if len(bets) > 0:
        summary['avg_bet'] = sum(bets) / len(bets)
        total_win = sum([x for x in rewards if x > 0])
        total_loss = sum([-x for x in rewards if x < 0])
        summary['win_2_lose'] =  total_win / total_loss
        summary['ev_per_shoe'] = sum(rewards) / total_simulations
        summary['std_per_shoe'] = np.std(rewards) * np.sqrt(len(bets) / total_simulations)
        sum_per_100 = calculate_sum_in_chunks(rewards, 100)
        summary['ev_per_100'] = np.mean(sum_per_100)
        summary['std_per_100'] = np.std(sum_per_100)
        num_of_win = sum([1 for x in rewards if x > 0])
        num_of_loss = sum([1 for x in rewards if x < 0])
        win_prob = num_of_win / len(bets)
        loss_prob = num_of_loss / len(bets)
        dd, ddd = calculate_max_drawdown_and_duration(rewards)
        summary['max_dd'] = dd
        summary['dd_duration_in_hands'] = ddd
        summary['risk_of_ruin'] = calc_ror(np.mean(rewards), np.std(rewards), units)

    print_unit_size = 20
    print_1st = "|".join([x.center(print_unit_size) for x in summary.keys()])
    print_1st = "|" + print_1st + '|'
    print_2nd = "|".join([("{:.3f}".format(x)).center(print_unit_size) for x in summary.values()])
    print_2nd = "|" + print_2nd + '|'
    print('=' * ((print_unit_size + 1) * len(summary) + 1))
    print(print_1st)
    print('-' * ((print_unit_size + 1) * len(summary) + 1))
    print(print_2nd)
    print('=' * ((print_unit_size + 1) * len(summary) + 1))
    logging.info("=" * 50)
    logging.info("results:")
    logging.info('\n' + ','.join(summary.keys()) + '\n' + ','.join(str(x) for x in summary.values()))
    logging.info("=" * 50)

    # # stats for reward-true count:
    # df = pd.DataFrame({
    #     'true_count': tcs,
    #     'rewards': rewards
    #     })
    # bins = [-21, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 21]
    # labels = ['-20 to -1', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11 to 20']
    # df['tc'] = pd.cut(df['true_count'], bins=bins, labels=labels, right=False)
    # pivot_table = df.pivot_table(values='rewards', index='tc', aggfunc={'rewards': ['mean', 'std']}, observed=False)
    # print("----------- ev per tc --------------")
    # print(pivot_table)
    # logging.info(pivot_table)
    # logging.info("=" * 50)

    if plot:
        pnl = np.cumsum(rewards)
        plt.plot(pnl, label="Accumulated Profit")
        plt.xlabel("Hands played")
        plt.ylabel("Total profit")
        plt.title("PnL Curve")
        plt.legend()
        plt.show()    

if __name__ == "__main__":
    logging.basicConfig(filename='expected_value.log', level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')
    parser = argparse.ArgumentParser(prog='Expected Value (EV) Calculation',
                                     description='Evaluate the profitability of different blackjack strategies by calculating'
                                                 ' their expected value (EV).')
    parser.add_argument("-c", "--custom", action='store_true',
                        help='Run custom user-defined movers and betters that require special initialization.')
    parser.add_argument("--cores", default=1, type=int,
                        help='How many cores to use in the calculation. (default: 1, use -1 for all cores)')
    parser.add_argument("-m", "--mover", default="card-count",
                        help='Use a predefined mover. Can also be the name of the class of a user-defined mover. '
                             '(possible values: card-count, basic-strategy-deviations, basic-strategy, perfect, simple; '
                             'default: card-count)')
    parser.add_argument("-b", "--better", default="card-count",
                        help='Use a predefined better. Can also be the name of the class of a user-defined better. '
                             '(possible values: card-count, simple; default: card-count)')
    parser.add_argument("-s", "--simulations", default=100_000, type=int,
                        help='How many simulations to run. Running more simulations gives more accurate '
                             'results but they are slower to calculate. (default: 100,000)')
    parser.add_argument("--decks", default=6, type=int, help='How many decks the shoe starts with. (default: 6)')
    parser.add_argument("--deck-penetration", default=.25, type=float,
                        help='When to reshuffle the shoe. Reshuffles when cards remaining < starting cards'
                             ' * deck penetration. (default: 0.25)')
    parser.add_argument("--stand17", action='store_true', help='Dealer should stand on soft 17. (default: true)')
    parser.add_argument("--hit17", action='store_true', help='Dealer should hit on soft 17. (default: false)')
    parser.add_argument("--das", action='store_true', help='Allow double after split. (default: true)')
    parser.add_argument("--no-das", action='store_true', help='Don\'t allow double after split. (default: false)')
    parser.add_argument("--peek", action='store_true', help='Dealer peeks for blackjack. (default: true)')
    parser.add_argument("--no-peek", action='store_true', help="Dealer doesn't peek for blackjack. (default: false)")
    parser.add_argument("--surrender", action='store_true', help='Allow surrendering. (default: true)')
    parser.add_argument("--no-surrender", action='store_true', help='Don\'t allow surrendering. (default: false)')
    parser.add_argument("--units", default=200, type=int, help='The number of units in total. (default: 200)')
    parser.add_argument("--hands-played", default=1000, type=int,
                        help='How many hands to play before checking the risk of ruin. (default: 1000)')
    args = parser.parse_args()

    decks_number = args.decks
    stand_soft_17 = args.stand17 or (not args.hit17)
    das_allowed = args.das or (not args.no_das)
    peek_for_bj = args.peek or (not args.no_peek)
    can_surrender = args.surrender or (not args.no_surrender)

    cores_used = args.cores if args.cores != -1 else multiprocessing.cpu_count()

    if args.custom:
        # ADD CUSTOM CODE HERE IF YOU HAVE BUILT YOUR OWN MOVER OR BETTER.
        mover = action_strategies.CardCountMover({(-1000, -1): os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_tc_minus_1.csv'),
                                              (-1, 0): os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_tc_minus_0.csv'),
                                              (0, 1): os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_tc_plus_0.csv'),
                                              (1, 2): os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_tc_plus_1.csv'),
                                              (2, 3): os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_tc_plus_2.csv'),
                                              (3, 4): os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_tc_plus_3.csv'),
                                              (4, 5): os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_tc_plus_4.csv'),
                                              (5, 6): os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_tc_plus_5.csv'),
                                              (6, 100): os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_tc_plus_6.csv'),
                                             })
        # mover = action_strategies.BasicStrategyDeviationsMover(os.path.join(os.path.dirname(__file__), 'data', 's17', '6deck_s17_das_peek_basic_strategy.csv'))
        better = betting_strategies.LinearBetterWongIn()
    else:
        mover, better = get_mover_and_better(args.mover, args.better)
    run(mover, better, args.simulations, cores_used, args.decks, args.deck_penetration,
        peek_for_bj, das_allowed, stand_soft_17, can_surrender, args.units, args.hands_played)
