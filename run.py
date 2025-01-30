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
    better = betting_strategies.Wong6()
    expected_value.run(mover, better, total_simulations=100000, cores=6,
                        deck_number=6, shoe_penetration=0.1667,
                        dealer_peeks_for_blackjack=True, das=True, dealer_stands_soft_17=True, 
                        surrender_allowed=False, units=280, hands_played=1000, num_of_other_players=0,
                        plot=False)


def run_ev_us_h17():
    # mover = action_strategies.BasicStrategyMover(os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_basic.csv'))
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
    # better = betting_strategies.WongBJA7()
    expected_value.run(mover, better, total_simulations=100000, cores=6,
                        deck_number=6, shoe_penetration=0.15,
                        dealer_peeks_for_blackjack=True, das=True, dealer_stands_soft_17=False, 
                        surrender_allowed=False, units=300, hands_played=1000, num_of_other_players=0,
                        plot=False)

def run_ev_us_h17_ls():
    # mover = action_strategies.BasicStrategyMover(os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_basic.csv'))
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
    expected_value.run(mover, better, total_simulations=100000, cores=6,
                        deck_number=6, shoe_penetration=.25,
                        dealer_peeks_for_blackjack=True, das=True, dealer_stands_soft_17=False, 
                        surrender_allowed=True, units=300, hands_played=1000, num_of_other_players=0,
                        plot=False)

def run_ev_us_d2s17():
    mover = action_strategies.CardCountMover({(-100, -1): os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_tc_minus_1.csv'),
                                              (-1, 0): os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_tc_minus_0.csv'),
                                              (0, 1): os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_tc_plus_0.csv'),
                                              (1, 2): os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_tc_plus_1.csv'),
                                              (2, 3): os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_tc_plus_2.csv'),
                                              (3, 4): os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_tc_plus_3.csv'),
                                              (4, 5): os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_tc_plus_4.csv'),
                                              (5, 6): os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_tc_plus_5.csv'),
                                              (6, 100): os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_tc_plus_6.csv'),
                                             })
    # mover = action_strategies.BasicStrategyMover(os.path.join(os.path.dirname(__file__), 'data', '2ds17', 'das_us_basic.csv'))
    better = betting_strategies.Linear2D()
    # better = betting_strategies.Linear4Passive()
    expected_value.run(mover, better, total_simulations=100000, cores=6,
                        deck_number=2, shoe_penetration=.25,
                        dealer_peeks_for_blackjack=True, das=True, dealer_stands_soft_17=True, 
                        surrender_allowed=False, units=250, hands_played=1000, num_of_other_players=0,
                        plot=False)


def run_ev_benchmark_h17():
    mover = action_strategies.BasicStrategyMover(os.path.join(os.path.dirname(__file__), 'data', 'h17', '6deck_h17_das_peek_basic.csv'))
    better = betting_strategies.SimpleBetter()
    expected_value.run(mover, better, total_simulations=100000, cores=6,
                        deck_number=6, shoe_penetration=.333,
                        dealer_peeks_for_blackjack=True, das=True, dealer_stands_soft_17=False, 
                        surrender_allowed=False, units=200, hands_played=1000, num_of_other_players=4)



if __name__ == "__main__":
    logging.basicConfig(filename='run.log', level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    
    run_ev_us_s17()
    # run_ev_us_h17()
    # run_ev_us_h17_ls()
    # run_ev_us_d2s17()
    # run_ev_benchmark_h17()
    