from collections import deque
import random
from typing import Deque
import json
import itertools

from error import MarkovException


def make_model(
    item_list: list[str], order: int = 2, end: str = "[EOF]", start: str = "[BOS]"
) -> dict[tuple[str, ...], list[str]]:
    """Make markov model from item list

    Args:
        itemList (list): Item list.
        order (int, optional): Number of layers of Markov model. Defaults to 2.
        end (str, optional): End statement. Defaults to "[EOF]".
        start (str, optional): Start statement. Defaults to "[BOS]".

    Returns:
        dict[tuple, list[str]]: Markov model.
    """
    model: dict[tuple[str, ...], list[str]] = {}
    queue: deque[str] = deque([], order)
    queue.append(start)
    for markov_value in item_list:
        if len(queue) < order:
            queue.append(markov_value)
            continue

        if queue[-1] == end:
            markov_key = tuple(queue)
            if markov_key not in model:
                model[markov_key] = []
            model.setdefault(markov_key, []).append(start)
            queue.append(start)
        markov_key = tuple(queue)
        model.setdefault(markov_key, []).append(markov_value)
        queue.append(markov_value)
    return model


def make_result(
    model: dict[tuple[str, ...], list[str]],
    num: int = 5,
    seed: str = "[BOS]",
    max_items: int = 10,
    end: str = "[EOF]",
) -> list[list[str]]:
    """Make result from model.

    Args:
        model (dict[tuple, list]): Markov model.
        num (int, optional): Number to generate. Defaults to 5.
        seed (str, optional): Seed. Defaults to "[BOS]".
        max_items (int, optional): Maximum number of items in the generated content. Defaults to 10.
        end (str, optional): End statement. Defaults to "[EOF]".

    Raises:
        MarkovException: Markov exception.

    Returns:
        list[list]: Generated contents.
    """
    result_list: list[list[str]] = []
    for _ in range(num):
        key_condidates = [key for key in model if key[0] == seed]
        if not key_condidates:
            raise MarkovException("Not find keyword")

        markov_key = random.choice(key_condidates)
        queue: Deque[str] = deque(list(markov_key), len(list(model.keys())[0]))

        result = list(markov_key)
        for _ in range(max_items - 2):
            markov_key = tuple(queue)
            if markov_key not in model:
                continue
            next_item = random.choice(model[markov_key])
            result.append(next_item)
            queue.append(next_item)

            if next_item == end:
                result_list.append(result)
                return result_list
        result_list.append(result)
    return result_list


if __name__ == "__main__":
    with open("dist/chords_data.json", "r") as f:
        data: list[list[str]] = json.load(f)
        molding_data = list(itertools.chain.from_iterable(data))
        model = make_model(molding_data, order=4)
        for res in make_result(model, max_items=10, seed="G"):
            print(res)
