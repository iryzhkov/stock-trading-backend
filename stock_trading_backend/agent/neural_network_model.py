"""Polynomial model class used by agents for building stuff.
"""
from torch import nn, optim

import torch
import torch.nn.functional as F

from stock_trading_backend.agent.model import Model


class NNModel(nn.Module):
    """Torch neural network model.
    """
    def __init__(self, num_inputs):
        """Initializer for linear model.

        Args:
            num_inputs: the dimension of input data.
        """
        super(NNModel, self).__init__()
        self.fc1 = nn.Linear(num_inputs, 120)
        self.fc2 = nn.Linear(120, 60)
        self.fc3 = nn.Linear(60, 1)

    def forward(self, input_tensor):
        """Forward pass on the neural network model.

        Args:
            input_tensor: the input tensor.

        Returns:
            Tensor with model results.
        """
        output = F.relu(self.fc1(input_tensor))
        output = F.relu(self.fc2(output))
        output = self.fc3(output)
        return output


class NeuralNetworkModel(Model):
    """Neural netowrk model class.
    """
    name = "neural_network_model"

    def __init__(self, learning_rate=1e-3):
        """Initializer for model class.

        Args:
            learning_rate: the learning rate of the model.
        """
        super(NeuralNetworkModel, self).__init__()
        self.model = None
        self.optimizer = None
        self.criterion = nn.MSELoss()
        self.learning_rate = learning_rate

    def _init_model(self, num_inputs):
        """Initializes internal linear model.

        Args:
            num_inputs: number of inputs that model will have.
        """
        self.model = NNModel(num_inputs)
        self.optimizer = optim.SGD(self.model.parameters(), lr=self.learning_rate)

    def _predict(self, state_action_tensor):
        """Use provided information to make a prediction.

        Args:
            state_action_tensor: pytorch tensor with state-action values.

        Returns:
            Predicted values for observation-action tensors.
        """
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
        if self.model is None:
            self._init_model(state_action_tensor.shape[1])

        self.optimizer.zero_grad()
        output = self.model(state_action_tensor)
        loss = self.criterion(output, expected_values_tensor)
        loss_value = loss.data.item()
        loss.backward()
        self.optimizer.step()
        return loss_value
