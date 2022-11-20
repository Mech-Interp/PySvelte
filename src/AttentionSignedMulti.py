from typing import List, Union

import numpy as np
import torch

Tensor = Union[np.ndarray, torch.Tensor]


def init(tokens: List[str], pattern: Tensor, labels=None, maximum=None, minimum=None):
    """Visualize a stack of ctx by ctx 2D tensors which can be both positive and negative.

    Args:
      tokens: a list of of strings representing tokens
      pattern: A [I, P, P] array representing attention probabilities,
        where P is the number of tokens and I is the number of patterns. The function will be implicitly normalized to be in [-1, 1].

      labels: human readable labels for heads. Optional.

      maximum: maximum value for the arrays, automatically calculated

      minimum: minimum value for the arrays, automatically calculated.

    """
    assert len(tokens) == pattern.shape[1], "tokens and activations must be same length"
    assert (
        pattern.shape[1] == pattern.shape[2]
    ), "final two dimensions of pattern must be equal"
    assert pattern.ndim == 3, "attention must be 3D"
    if labels is not None:
        assert (
            len(labels) == pattern.shape[0]
        ), "labels must correspond to number of patterns"
    maximum = pattern.max()
    minimum = pattern.min()
    pattern = pattern / max(-minimum, maximum)
    return
