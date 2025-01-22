"""Betting strategies to be used in expected value."""
import logging

from utils import get_hilo_running_count


class BaseBetter:
    """Base better. The parent class of all betters."""

    @staticmethod
    def get_bet(cards_seen: list[int], deck_number: int) -> int:
        """
        Raise `NotImplementedError`. To be overridden in the other classes.

        :param cards_seen: The cards we have already seen from the shoe. Used when card counting.
        :param deck_number: The number of decks in the starting shoe.
        :return: How much money to bet.
        """
        raise NotImplementedError("The `get_bet` method hasn't been overridden.")


class SimpleBetter(BaseBetter):
    """Simple better. Bets the same amount every time."""

    @staticmethod
    def get_bet(cards_seen: list[int], deck_number: int) -> int:
        """
        Bet 1 every time. The bet doesn't change.

        :param cards_seen: The cards we have already seen from the shoe. Used when card counting.
        :param deck_number: The number of decks in the starting shoe.
        :return: How much money to bet.
        """
        return 1


class CardCountBetter(BaseBetter):
    """Change the bet according to the true count."""

    @staticmethod
    def get_bet(cards_seen: list[int], deck_number: int) -> int:
        """
        Bet true_count ^ 2 / 2 if true_count >= +1 else 1. Cap at 15 (using a 1-15 spread).

        :param cards_seen: The cards we have already seen from the shoe. Used when card counting.
        :param deck_number: The number of decks in the starting shoe.
        :return: How much money to bet.
        """
        running_count = get_hilo_running_count(cards_seen)
        cards_left = deck_number * 52 - len(cards_seen) - 1
        true_count = running_count / (cards_left / 52)
        if true_count >= 2:
            return max(min(int(true_count ** 2), 100), 1)
        return 1

class LinearBetter(BaseBetter):
    """Change the bet according to the true count."""

    @staticmethod
    def get_bet(cards_seen: list[int], deck_number: int) -> int:
        """
        Bet (true_count - 1) / 2 if true_count >= +2 else 1. Cap at 10 (using a 1-10 spread).

        :param cards_seen: The cards we have already seen from the shoe. Used when card counting.
        :param deck_number: The number of decks in the starting shoe.
        :return: How much money to bet.
        """
        running_count = get_hilo_running_count(cards_seen)
        cards_left = deck_number * 52 - len(cards_seen) - 1
        true_count = running_count / (cards_left / 52)
        if true_count >= 2:
            return max(min(int((true_count - 1) / 2), 10), 1)
        return 1

class LinearBetterWongIn(BaseBetter):
    """Change the bet according to the true count."""

    @staticmethod
    def get_bet(cards_seen: list[int], deck_number: int) -> int:
        """
        Bet (true_count - 1) / 2 if true_count >= +2 else 1. Cap at 10 (using a 1-10 spread).

        :param cards_seen: The cards we have already seen from the shoe. Used when card counting.
        :param deck_number: The number of decks in the starting shoe.
        :return: How much money to bet.
        """
        running_count = get_hilo_running_count(cards_seen)
        cards_left = deck_number * 52 - len(cards_seen) - 1
        true_count = running_count / (cards_left / 52)
        # logging.debug("running_count = {}".format(running_count))
        # logging.debug("cards_left = {}".format(cards_left))
        # logging.debug("true_count = {}".format(true_count))
        if true_count >= 1:
            return max(min(int(true_count), 10), 1)
        return 0.001

class Wong6(BaseBetter):
    """Change the bet according to the true count."""

    @staticmethod
    def get_bet(cards_seen: list[int], deck_number: int) -> int:
        """
        Bet (true_count - 1) / 2 if true_count >= +2 else 1. Cap at 10 (using a 1-10 spread).

        :param cards_seen: The cards we have already seen from the shoe. Used when card counting.
        :param deck_number: The number of decks in the starting shoe.
        :return: How much money to bet.
        """
        running_count = get_hilo_running_count(cards_seen)
        cards_left = deck_number * 52 - len(cards_seen) - 1
        true_count = running_count / (cards_left / 52)
        # logging.debug("running_count = {}".format(running_count))
        # logging.debug("cards_left = {}".format(cards_left))
        # logging.debug("true_count = {}".format(true_count))
        if true_count >= 1:
            return max(min(int(true_count), 6), 1)
        return 0.001

class Wong20(BaseBetter):
    """Change the bet according to the true count."""

    @staticmethod
    def get_bet(cards_seen: list[int], deck_number: int) -> int:
        """
        Bet (true_count - 1) / 2 if true_count >= +2 else 1. Cap at 10 (using a 1-10 spread).

        :param cards_seen: The cards we have already seen from the shoe. Used when card counting.
        :param deck_number: The number of decks in the starting shoe.
        :return: How much money to bet.
        """
        running_count = get_hilo_running_count(cards_seen)
        cards_left = deck_number * 52 - len(cards_seen) - 1
        true_count = running_count / (cards_left / 52)
        # logging.debug("running_count = {}".format(running_count))
        # logging.debug("cards_left = {}".format(cards_left))
        # logging.debug("true_count = {}".format(true_count))
        if true_count >= 1:
            return max(min(int(true_count), 20), 1)
        return 0.001