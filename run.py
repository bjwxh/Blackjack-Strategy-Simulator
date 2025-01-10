import os
import logging

import action_strategies, betting_strategies, expected_value


def run_ev_us_s17():
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
    better = betting_strategies.LinearBetterWongIn()
    expected_value.run(mover, better, total_simulations=1000, cores=4,
                        deck_number=6, shoe_penetration=.333,
                        dealer_peeks_for_blackjack=True, das=True, dealer_stands_soft_17=True, 
                        surrender_allowed=False, units=200, hands_played=1000)


def run_ev_us_h17():
    mover = action_strategies.CardCountMover({(-1000, -1): os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_tc_minus_1.csv'),
                                              (-1, 0): os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_tc_minus_0.csv'),
                                              (0, 1): os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_tc_plus_0.csv'),
                                              (1, 2): os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_tc_plus_1.csv'),
                                              (2, 3): os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_tc_plus_2.csv'),
                                              (3, 4): os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_tc_plus_3.csv'),
                                              (4, 5): os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_tc_plus_4.csv'),
                                              (5, 6): os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_tc_plus_5.csv'),
                                              (6, 100): os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_tc_plus_6.csv'),
                                             })
    # better = betting_strategies.LinearBetterWongIn()
    better = betting_strategies.Wong6()
    expected_value.run(mover, better, total_simulations=100000, cores=4,
                        deck_number=6, shoe_penetration=.1667,
                        dealer_peeks_for_blackjack=True, das=True, dealer_stands_soft_17=True, 
                        surrender_allowed=False, units=200, hands_played=1000)


if __name__ == "__main__":
    logging.basicConfig(filename='run.log', level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    
    # run_ev_us_s17()
    run_ev_us_h17()