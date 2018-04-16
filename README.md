# Introduction to AI - CSE 415 (WIN 2018)
Course Link: https://courses.cs.washington.edu/courses/cse415/18wi/

## Assignment 1 (Python Warm-up)
Link: https://courses.cs.washington.edu/courses/cse415/18wi/assign/A1.html

Homework Description:

Create a Python program run_Guess_My_Number that randomly selects a number between 0 and 1000, and then asks the user to figure out what the number is, carrying on a dialog with the user until the game is over. The user should be offered the opportunity to ask questions such as the following:
If we subtract 6 from n, is the result divisible by 13?
Thus, the questions are of this form:
If we subtract k from n, is the result divisible by m?
The rules here are that n is the secret number, k is in the range 0 to m, and m is a prime number less than 1000. 
 
In each turn, the user should be given the opportunity to either ask a question of the type above, guess the number directly, or quit. In the end the user's score is 0 if s/he quits, or ceiling(n/t) where n is the secret number, and t is the number of turns taken by the user to determine the number, including the correct "guess". 

## Assignment 2 (Problem Formulation)
Link: https://courses.cs.washington.edu/courses/cse415/18wi/assign/A2.html

Homework Description:

This assignment follows up on Assignment 1 by taking the same number-guessing game and putting it into framework of the classical theory of problem solving. When you have completed this assignment, you will be aware of the differences between a problem formulation for the classical theory and a simple game that does not take the theory into account. 

## Assignment 3 (Heuristic Search)
Link: https://courses.cs.washington.edu/courses/cse415/18wi/assign/A3.html

Homework Description:

In the current assignment, you'll implement several other search algorithms and compare how they perform.
- Breadth First Search
- Iterative-Deepening Depth-First Search
- A* Implementation
- Heuristics 

## Assignment 4 (Game-Playing Agents)
Link: https://courses.cs.washington.edu/courses/cse415/18wi/assign/A4.html

Homework Description:

In this assignment we explore two-person, zero-sum game playing using a family of games called "Toro-Tile Straight". Here we put our agents into competition, adding lookahead (with the Minimax technique) and, optionally, pruning (with the alpha-beta method) and caching (with Zobrist hashing) to the search.

## Assignment 5 (Markov Decision Processes and Q-Learning)
Link: https://courses.cs.washington.edu/courses/cse415/18wi/assign/A5.html

Homework Description:

The search theme continues here, except that now our agents operate in a world in which actions may have uncertain outcomes. The interactions are modeled probabilistically using the technique of Markov Decision Processes. Within this framework, the assignment focuses on two approaches to having the agent maximize its expected utility: 
1. by a form of planning, in which we assume that the parameters of the MDP (especially T and R) are known, which takes the form of Value Iteration, and 
2. by an important form of reinforcement learning, called Q-learning, in which we assume that the agent does not know the MDP parameters.

