Tan Network puzzle solution
===========================

## Overview

This project is a solution to the Tan Network programming puzzle provided by the CodinGame website, that can be found [here](https://www.codingame.com/ide/puzzle/tan-network).

The solution was implemented outside the website's IDE first, in order to properly use the TDD method, and to also ease
the debugging process.
The tests created as part of the TDD are also provided here.


## Algorithm

The puzzle is a path finding problem, applied on a directed graph, and to be resolved without any strict
performance constraint.

Since there are no strict performance constraints, relying on the Dijkstra algorithm or even a BFS would be a valid choice,
but this project uses the A* algorithm instead, just for the fun of it :) .


## Project structure

The project is split into several folders:
* src : contains the solution's source code
* test : contains the related tests
* tools : contains some utility scripts

Each src/\<filename\> source file has an associated test/test_\<filename\> file testing its code.
Below is a short description of each source file:
* src/graph.py : implements the graph theory logic; namely a directed graph and the A* algorithm
* src/main.py : implements the main functions of the solution
* src/tan_network.py : implements the logic related to the puzzle's context, namely the representation of the transportation network and its stops.


## Testing the solution on CodinGame

CodinGame's online IDE does not support multiple files; they have to be merged into a single one.
The tools/codingame_formatter script was written to handle this formatting process, which then allows to test the solution by performing the following steps:

1. Checkout this project
2. Go to the puzzle's address mentionned above
3. Select Python 3 as the solution's programming language, by using the drop down list on top of the text editor
4. Remove the template code provided inside the online IDE
5. Run the tools/codingame_formatter script, and copy its output, and paste it inside the online IDE's text editor
6. Press 'Play all testcases'

