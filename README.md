# MancalaML
Personal project. An attempt to train AI to play Mancala.

Includes a full Python implementation of Mancala created by me.

This project was created to test the NEAT's effectiveness when genomes are paired against one another.

Currently a WORK IN PROGRESS, far from finished.
`python game_test.py`

Steps I chose to take while training my population:
- self_learn each genome by pitting it against a random, unevaluated genome in the same population and scoring based on tile ratio alone
- letting opponent sometimes choose a random move rather than a predicted move (based on global epsilon)
- adding fitness punishment for picking empty tile
- decrease the value of epsilon
