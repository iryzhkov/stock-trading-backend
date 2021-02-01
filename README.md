# Stock Trading Back-end

[![Build Status](https://travis-ci.com/iryzhkov/stock-trading-backend.svg?branch=main)](https://travis-ci.com/iryzhkov/stock-trading-backend)
[![Inline docs](http://inch-ci.org/github/iryzhkov/stock-trading-backend.svg?branch=master)](http://inch-ci.org/github/iryzhkov/stock-trading-backend)

A back-end for AI-based (simulated) stock trading.

Current status: in progress

## Overview

A back-end system for training and testing of AI agents that buy and sell stocks.

Contains custom OpenAI Gym environment for simulation stock market.

Supports multiple sources of stock data:
- Real historical stock data (quandl)
- Generated stock data

Supports multiple types of AI agents:
- Q-Learning agent
- SARSA-Learning agent

Supports saving/loading of AI agents in the following environments:
- local

## Usage

To install required dependencies:
```
make install
```

To run the unit-tests:
```
make test
```

To train a model:
```
make train
```

To back-test a model:
```
make back-test
```

## Performance
