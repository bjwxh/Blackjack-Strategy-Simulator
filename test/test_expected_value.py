"""Test the expected value (EV) calculator."""
import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import unittest

from expected_value import run, play_hand, simulate_hand
import action_strategies, betting_strategies
from action_strategies import SimpleMover, PerfectMover, BaseMover, BasicStrategyMover
from betting_strategies import SimpleBetter, BaseBetter


# class TestExpectedValue(unittest.TestCase):
#     def test_single_sim(self):
#         mover = action_strategies.CardCountMover({(-1000, -1): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_minus_1.csv'),
#                                                   (-1, 0): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_minus_0.csv'),
#                                                   (0, 1): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_plus_0.csv'),
#                                                   (1, 2): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_plus_1.csv'),
#                                                   (2, 3): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_plus_2.csv'),
#                                                   (3, 4): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_plus_3.csv'),
#                                                   (4, 5): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_plus_4.csv'),
#                                                   (5, 6): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_plus_5.csv'),
#                                                   (6, 100): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_plus_6.csv'),
#                                                  })
#         # mover = action_strategies.BasicStrategyMover("data/h17/6deck_h17_das_us_no_surrender_basic.csv")
#         better = betting_strategies.LinearBetterWongIn()
#         # ev = expected_value(mover, better, simulations=10, deck_number=6, shoe_penetration=.1,
#         #                     dealer_peeks_for_blackjack=True, das=True, dealer_stands_soft_17=True, 
#         #                     surrender_allowed=False, units=200, hands_played=1000, plot_profits=True, 
#         #                     print_info=True)
#         # print(ev)
#         run(mover, better, total_simulations=200, cores=2,
#             deck_number=6, shoe_penetration=.2,
#             dealer_peeks_for_blackjack=True, das=True, dealer_stands_soft_17=True, 
#             surrender_allowed=False, units=200, hands_played=1000)


class TestPlayHand(unittest.TestCase):
    
    def test_s17(self):
        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_basic_strategy.csv')
        action_class = BasicStrategyMover(cfile)

        # hold cards are 22 to AA: 
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=6, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 10], [2, 10]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=7, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 10, 10], [2, 10, 10]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=8, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 2, 10, 10]])
        res = play_hand(action_class, hand_cards=[[5,5]], dealer_up_card=8, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[5, 5, 10], [5, 5, 10]])
        res = play_hand(action_class, hand_cards=[[5,5]], dealer_up_card=10, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[5, 5, 10]])
        res = play_hand(action_class, hand_cards=[[11, 11]], dealer_up_card=10, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11,10], [11,10]])
        res = play_hand(action_class, hand_cards=[[11, 11]], dealer_up_card=11, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11,10], [11,10]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=8, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10,11],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 2, 11, 10, 9]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=6, dealer_down_card=10, shoe=[3, 3, 3, 3, 4, 4, 4, 4, 4],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 4, 4, 4], [2, 4, 4, 3]])


        # hold cards are AX: 
        res = play_hand(action_class, hand_cards=[[11,2]], dealer_up_card=6, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 2, 10], [11, 2, 10]])
        res = play_hand(action_class, hand_cards=[[11,6]], dealer_up_card=2, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 6, 10]])
        res = play_hand(action_class, hand_cards=[[11,6]], dealer_up_card=3, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 6, 10], [11, 6, 10]])
        res = play_hand(action_class, hand_cards=[[11,6]], dealer_up_card=7, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 6, 10]])
        res = play_hand(action_class, hand_cards=[[11,7]], dealer_up_card=2, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 7]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=2, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=6, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8]])

        # hold cards are otherwise: 
        res = play_hand(action_class, hand_cards=[[10,2]], dealer_up_card=6, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[10, 2]])
        res = play_hand(action_class, hand_cards=[[10,2]], dealer_up_card=2, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[10, 2, 7]])
        res = play_hand(action_class, hand_cards=[[10,2]], dealer_up_card=7, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[10, 2, 7]])
        res = play_hand(action_class, hand_cards=[[8,2]], dealer_up_card=7, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[8, 2, 7], [8, 2, 7]])
        res = play_hand(action_class, hand_cards=[[8,2]], dealer_up_card=10, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[8, 2, 7]])
        res = play_hand(action_class, hand_cards=[[8,3]], dealer_up_card=11, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[8, 3, 7]])
        res = play_hand(action_class, hand_cards=[[2,9]], dealer_up_card=11, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 9, 10]])

        # TODO: handle empty shoe
        # res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=7, dealer_down_card=10, shoe=[10, 10, 10],
        #                 splits_remaining=3, deck_number=6)
        # self.assertEqual(res, [[2, 10, 10], [2, 10]])

    def test_h17(self):
        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'h17', '6deck_h17_das_peek_basic.csv')
        action_class = BasicStrategyMover(cfile)

        # hold cards are 22 to AA: 
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=6, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 10], [2, 10]])
        res = play_hand(action_class, hand_cards=[[5,5]], dealer_up_card=11, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[5, 5, 7]])
        res = play_hand(action_class, hand_cards=[[5,5]], dealer_up_card=9, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[5, 5, 7], [5,5,7]])
        res = play_hand(action_class, hand_cards=[[4,4]], dealer_up_card=5, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[4, 7, 6], [4, 7, 6], [4, 5, 4], [4, 5, 4]])
        res = play_hand(action_class, hand_cards=[[4,4]], dealer_up_card=5, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=0, deck_number=6)
        self.assertEqual(res, [[4, 4, 7]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[10,5,2,8,4,8,2],
                        splits_remaining=4, deck_number=6)
        self.assertEqual(res, [[2,8,4], [2,8,4],[2,8,2],[2,8,2],[2,5,10]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[10,10,11,10,9,8,7,6,5,4,3,2,2],
                        splits_remaining=4, deck_number=6)
        self.assertEqual(res, [[2,3,4,5], [2,6,7],[2,8,9],[2,8,9],[2,10]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[10,10,11,10,9,8,7,6,5,4,3,2,2],
                        splits_remaining=0, deck_number=6)
        self.assertEqual(res, [[2,2,2,2,3,4]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[10,10,11,10,9,8,7,6,5,4,3,2,2],
                        splits_remaining=0, deck_number=6)
        self.assertEqual(res, [[2,2,2,2,3,4]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[10,10,11,10,9,8,7,6,5,4,3,2,2],
                        splits_remaining=1, deck_number=6)
        self.assertEqual(res, [[2,2,2,3,4], [2,5,6]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[10,10,11,10,9,8,7,6,5,4,3,2,2],
                        splits_remaining=2, deck_number=6)
        self.assertEqual(res, [[2,2,3,4,5], [2,6,7], [2,8,9], [2, 8, 9]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[10,10,11,10,9,8,7,6,5,4,3,2,2],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2,3,4,5], [2,6,7], [2,8,9], [2, 8, 9], [2, 10]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[8,9,10,11],
                        splits_remaining=2, deck_number=6)
        self.assertEqual(res, [[2,11,10], [2,11,10], [2,9,8], [2,9,8]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[8,9,10,11],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2,11,10], [2,11,10], [2,9,8], [2,9,8]])
        res = play_hand(action_class, hand_cards=[[2,2]], dealer_up_card=5, dealer_down_card=10, shoe=[10,10,11,10,9,8,7,6,5,4,3,2,2,2],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2,2,3,4,5], [2,6,7],[2,8,9],[2,8,9],[2,10]])

        # hold cards are AX: 
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=5, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=6, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8, 7], [11, 8, 7]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=7, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8]])
        res = play_hand(action_class, hand_cards=[[11,7]], dealer_up_card=6, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 7, 7], [11, 7, 7]])
        res = play_hand(action_class, hand_cards=[[11,7]], dealer_up_card=2, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 7, 7], [11, 7, 7]])
        res = play_hand(action_class, hand_cards=[[11,7]], dealer_up_card=7, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 7]])
        res = play_hand(action_class, hand_cards=[[11,7]], dealer_up_card=9, dealer_down_card=10, shoe=[2,3,4,5,6,7],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 7, 7, 6]])

class TestSimulateHand(unittest.TestCase):

    def test_surrender(self):
        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'h17', '6deck_h17_das_peek_basic.csv')
        action_class = BasicStrategyMover(cfile)

        res = simulate_hand(action_class, cards=[8,8], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[8,7], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[9,7], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[9,7], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[9,7], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,7], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)

        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'h17', '6deck_h17_das_peek_tc_minus_1.csv')
        action_class = BasicStrategyMover(cfile)
        res = simulate_hand(action_class, cards=[10,7], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=8, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)

        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'h17', '6deck_h17_das_peek_tc_minus_0.csv')
        action_class = BasicStrategyMover(cfile)
        res = simulate_hand(action_class, cards=[10,7], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=8, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)

        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'h17', '6deck_h17_das_peek_tc_plus_0.csv')
        action_class = BasicStrategyMover(cfile)
        res = simulate_hand(action_class, cards=[10,7], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=8, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)

        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'h17', '6deck_h17_das_peek_tc_plus_1.csv')
        action_class = BasicStrategyMover(cfile)
        res = simulate_hand(action_class, cards=[10,7], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=8, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)

        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'h17', '6deck_h17_das_peek_tc_plus_2.csv')
        action_class = BasicStrategyMover(cfile)
        res = simulate_hand(action_class, cards=[10,7], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=8, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)

        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'h17', '6deck_h17_das_peek_tc_plus_3.csv')
        action_class = BasicStrategyMover(cfile)
        res = simulate_hand(action_class, cards=[10,7], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=8, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)

        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'h17', '6deck_h17_das_peek_tc_plus_4.csv')
        action_class = BasicStrategyMover(cfile)
        res = simulate_hand(action_class, cards=[10,7], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,6], dealer_up_card=8, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=11, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=10, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)
        res = simulate_hand(action_class, cards=[10,5], dealer_up_card=9, dealer_down_card=2, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6, surrender_allowed=True)
        self.assertEqual(res, -0.5)



    def test_s17(self):
        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_basic_strategy.csv')
        action_class = BasicStrategyMover(cfile)

        # hold cards are mixed:
        res = simulate_hand(action_class, cards=[10,4], dealer_up_card=4, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 1)
        res = simulate_hand(action_class, cards=[10,11], dealer_up_card=4, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 1.5)
        res = simulate_hand(action_class, cards=[2,8], dealer_up_card=4, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 2)
        res = simulate_hand(action_class, cards=[2,9], dealer_up_card=4, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 2)
        res = simulate_hand(action_class, cards=[2,8], dealer_up_card=9, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 2)
        res = simulate_hand(action_class, cards=[2,3], dealer_up_card=9, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[2,3], dealer_up_card=9, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[8,3], dealer_up_card=11, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[11,10], dealer_up_card=11, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 0)

        # hold cards are Ax:
        res = simulate_hand(action_class, cards=[11,2], dealer_up_card=4, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 1)
        res = simulate_hand(action_class, cards=[11,2], dealer_up_card=5, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 2)
        res = simulate_hand(action_class, cards=[11,2], dealer_up_card=6, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 2)
        res = simulate_hand(action_class, cards=[11,2], dealer_up_card=7, dealer_down_card=10, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[11,2], dealer_up_card=4, dealer_down_card=7, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, -1)
        res = simulate_hand(action_class, cards=[11,2], dealer_up_card=5, dealer_down_card=6, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, -2)
        res = simulate_hand(action_class, cards=[11,2], dealer_up_card=6, dealer_down_card=5, shoe=[2,3,4,5,6,7,8,9,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, -2)
        
        # hold cards are 22 - AA:
        res = simulate_hand(action_class, cards=[2,2], dealer_up_card=7, dealer_down_card=10, shoe=[8,10,8,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 2)
        res = simulate_hand(action_class, cards=[2,2], dealer_up_card=7, dealer_down_card=10, shoe=[8,10,8,10,8], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 4)
        res = simulate_hand(action_class, cards=[2,2], dealer_up_card=7, dealer_down_card=10, shoe=[10,8,10,8,10,8,10,8,2,2], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 8)
        res = simulate_hand(action_class, cards=[2,2], dealer_up_card=7, dealer_down_card=10, shoe=[8,3,8,3,8,3,8,3,8], splits_remaining=4, deck_number=6)
        self.assertEqual(res, -4)
        res = simulate_hand(action_class, cards=[2,2], dealer_up_card=7, dealer_down_card=10, shoe=[11,10,9,8,7,6,5,4,3], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 1)
        res = simulate_hand(action_class, cards=[8,8], dealer_up_card=10, dealer_down_card=8, shoe=[10,10,11,6,11,11,9,9,3,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 2)
        res = simulate_hand(action_class, cards=[8,8], dealer_up_card=10, dealer_down_card=7, shoe=[10,10,11,6,11,11,9,9,3,10], splits_remaining=4, deck_number=6)
        self.assertEqual(res, 3)

class TestDeviations(unittest.TestCase):
    def test_s17(self):
        # 1+
        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_plus_1.csv')
        action_class = BasicStrategyMover(cfile)
        res = play_hand(action_class, hand_cards=[[2,9]], dealer_up_card=11, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 9, 10], [2, 9, 10]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=5, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8, 10], [11, 8, 10]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=4, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=6, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8, 10], [11, 8, 10]])
        res = play_hand(action_class, hand_cards=[[2,7]], dealer_up_card=2, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 7, 10], [2, 7, 10]])
        res = play_hand(action_class, hand_cards=[[3,9]], dealer_up_card=3, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[3, 9, 10]])
        res = play_hand(action_class, hand_cards=[[3,5]], dealer_up_card=6, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[3, 5, 10]])

        # 2+
        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_plus_2.csv')
        action_class = BasicStrategyMover(cfile)
        res = play_hand(action_class, hand_cards=[[10,10]], dealer_up_card=6, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[10, 10]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=6, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8, 10],[11, 8, 10]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=5, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8, 10],[11, 8, 10]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=4, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8]])
        res = play_hand(action_class, hand_cards=[[11,8]], dealer_up_card=7, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[11, 8]])
        res = play_hand(action_class, hand_cards=[[4,8]], dealer_up_card=2, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[4, 8, 10]])
        res = play_hand(action_class, hand_cards=[[4,8]], dealer_up_card=3, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[4, 8]])
        res = play_hand(action_class, hand_cards=[[4,8]], dealer_up_card=4, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[4, 8]])
        res = play_hand(action_class, hand_cards=[[2,8]], dealer_up_card=10, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[2, 8, 10]])
        res = play_hand(action_class, hand_cards=[[3,5]], dealer_up_card=6, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[3, 5, 10],[3, 5, 10]])
        res = play_hand(action_class, hand_cards=[[3,6]], dealer_up_card=7, dealer_down_card=10, shoe=[10, 10, 10, 10],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[3, 6, 10]])

        # 0-
        cfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_minus_0.csv')
        action_class = BasicStrategyMover(cfile)
        res = play_hand(action_class, hand_cards=[[7,7]], dealer_up_card=10, dealer_down_card=9, shoe=[4,3,2],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[7,7,2,3]])
        action_class = action_strategies.CardCountMover({(-1000, 1000): os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 's17', '6deck_s17_das_peek_tc_minus_0.csv')})
        res = play_hand(action_class, hand_cards=[[7,7]], dealer_up_card=10, dealer_down_card=9, shoe=[4,3,2],
                        splits_remaining=3, deck_number=6)
        self.assertEqual(res, [[7,7,2,3]])



if __name__ == '__main__':
    logging.basicConfig(filename='test_expected_value.log', level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    # logging.getLogger('urllib3').setLevel(logging.WARNING)
    unittest.main()