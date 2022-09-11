from typing import List, Union

import numpy as np
import torch

Tensor = Union[np.ndarray, torch.Tensor]


def init(
    pos_logit_tokens: List[str], pos_logit_values: Tensor, neg_logit_tokens: List[str], neg_logit_values: Tensor, default_display=10, max_display=10, name="", 
):
    """Visualize the activation patterns over the tokens in a text.

    Args:
      tokens: a list of of strings representing tokens
      attention: A 1D tensor of activations over the tokens.
      neuron_name: A string representing the neuron name.

    """
    return
