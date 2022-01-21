from __future__ import annotations
import numpy as np


def get_nearest_value(data: list[int] | list[float], target: int | float):  # type: ignore
    return data[np.abs(np.asarray(data) - target).argmin()]
