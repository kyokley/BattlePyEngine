# BattlePy [![Build Status](https://travis-ci.org/kyokley/BattlePy.svg?branch=master)](https://travis-ci.org/kyokley/BattlePy)
Python Battleship Engine

## What is it?
BattlePy is a game engine that can be used to pit 2 battleship AIs against each other.

## The Rules
Each individual game consists of two phases. The first phase involves each player placing 5 ships on the board without the other player's knowledge. The second phase is where each player takes turns firing shots at their opponents ships. The player that successfully sinks all of their opponents ships wins. In addition, if a player raises an unhandled exception, they automatically lose the game.

A single game is of very little use in terms of training an AI. Therefore, the Tournament class has been provided to allow a series of games to be played. Each AI player's "knowledge" can be preserved from game to game.

## Why Battleship?
BattlePy was created to be a fun way to encourage python development and friendly competition between developers.

Battleship is an excellent choice for building a rudimentary AI. The game is easily separated into offensive and defensive phases. The simplest solution can be implemented in just 30 lines of code. Of course, your AI may experience more success by analyzing your opponent's patterns and adapting to them.
