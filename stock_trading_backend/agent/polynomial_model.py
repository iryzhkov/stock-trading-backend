"""Polynomial model class used by agents for building stuff.
"""
from torch import nn, optim

import torch

from stock_trading_backend.agent.model import Model


class LinearModel(nn.Module):
    """Torch linear model.
    """
    def __init__(self, num_inputs):
        """Initializer for linear model.

        Args:
            num_inputs: the dimension of input data.
        """
        super(LinearModel, self).__init__()
        self.linear = nn.Linear(num_inputs, 1)

    def forward(self, input_tensor):
        """Forward pass on the linear model.

        Args:
            input_tensor: the input tensor.

        Returns:
            Tensor with model results.
        """
        output = self.linear(input_tensor)
        return output


class PolynomialModel(Model):
    """Polynomial model class.
    """
    name = "polynomial_model"

    def __init__(self, degree=1, learning_rate=1e-3):
        """Initializer for model class.

        Args:
            degree: the maximum degree of polynomial. (1 is linear, 2 is quadratic, etc.,).
        """
        super(PolynomialModel, self).__init__()

        if degree < 1:
            raise ValueError("polynomial model does not work with degree of {}".format(degree))

        self.degree = degree
        self.id_str = "{}_{}_{}".format(self.name, degree, learning_rate)
        self.model = None
        self.optimizer = None
        self.criterion = nn.MSELoss()
        self.learning_rate = learning_rate

    def _init_model(self, num_inputs):
        """Initializes internal linear model.

        Args:
            num_inputs: number of inputs that model will have.
        """
        self.model = LinearModel(num_inputs)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def _convert_tensor_to_polynomial(self, tensor):
        """Converts tensor to polynomial tensor.

        Args:
            tensor: torch.tensor to convert.

        Returns:
            Converted tensor.
        """
        # pylint: disable=no-member
        rows = [torch.cat([row ** i for i in range(1, self.degree + 1)], 0) for row in tensor]
        # pylint: disable=no-member
        return torch.stack(rows)

    def _predict(self, state_action_tensor):
        """Use provided information to make a prediction.

        Args:
            state_action_tensor: pytorch tensor with state-action values.

        Returns:
            Predicted values for observation-action tensors.
        """
        state_action_tensor = self._convert_tensor_to_polynomial(state_action_tensor)
        if self.model is None:
            self._init_model(state_action_tensor.shape[1])
        return self.model(state_action_tensor).detach().reshape(-1)

    def _train(self, state_action_tensor, expected_values_tensor):
        """Train the model for 1 epoch.

        Args:
            state_action_tensor: pytorch tensor with state-action expected_values.
            expected_values: pytorch tensor with expected values for each state-action.

        Returns:
            The loss before trainig.
        """
        state_action_tensor = self._convert_tensor_to_polynomial(state_action_tensor)
        if self.model is None:
            self._init_model(state_action_tensor.shape[1])

        self.optimizer.zero_grad()
        output = self.model(state_action_tensor)
        loss = self.criterion(output, expected_values_tensor)
        loss_value = loss.data.item()
        loss.backward()
        self.optimizer.step()
        return loss_value
