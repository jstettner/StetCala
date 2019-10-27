# StetCala
Personal project by Jack Stettner. An attempt to train AI to play Mancala.

Includes a full Python implementation of Mancala created by me.

This project was created to test the NEAT's effectiveness when genomes are paired against one another.

Steps I chose to take while training my population:
- Make each genome play against a full random player.
- Pit each genome against random other genomes in the same population and score based on tile ratio alone
- letting opponent sometimes choose a random move rather than a predicted move (based on global epsilon)
- adding fitness punishment for picking empty tile
- decrease the value of epsilon
