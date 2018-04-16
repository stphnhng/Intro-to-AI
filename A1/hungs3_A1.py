'''
Stephen Hung
CSE 415 A1
This python program runs the "Guess My Number" game which consists of the
user trying to guess a randomly generated number.
The user does so through three actions, "Guess", "Ask", or "Quit"
"Guess" allows the user to directly guess the number.
"Ask" allows the user to ask if the number - k is divisible by m 
where k and m are provided by the user.
"Quit" allows the user to quit with a score of 0.
Each action by the user will decrease the score by a certain factor.
'''

import random
import math

'''
This function checks if 'm' is a prime under 1000.
Parameters:
  m: the number to be checked
Returns:
  True/False: If the number is a prime under 1000
'''
def isPrimeUnder1000(m):
    if(m <= 1 or m >= 1000):
        return False
    for i in range(2,m):
        if(m % i == 0):
            return False    
    return True

'''
This function checks if 0 <= k < m and if m is prime
Furthermore, it checks if (n-k) is divisible by m.
Parameters:
  n: The randomly generated integer to be guessed
  k: The integer to be subtracted from n.
  m: The integer to check (n-k)'s divisibility.
Returns:
  True/False: If (n-k) is divisible by m and if 0 <= k < m 
              and m is a prime under 1000.
'''
def is_n_minus_k_divisible_by_m(n,k,m):
    if(k < 0 or m <= k):
        print('Error: k < 0 or m <= k')
        return False

    if(not isPrimeUnder1000(m)):
        print('Error: m is not a prime under 1000')
        return False

    if( (n-k) % m != 0):
        return False

    return True
'''
    This function runs the game, "Guess My Number" where the user
guesses a randomly generated integer 'n' by choosing one of three options,
"Ask", "Guess", and "Quit".

"Ask" calls the function is_n_minus_k_divisible_by_m and returns
a string answering whether (n-k) % m along with several other conditions.

"Guess" allows the user to guess a number

"Quit" lets the user quit the game

At the end of the game, the score of the user is printed.
Parameters: none
Returns: none
'''
def run_Guess_My_Number():
    turnNumber = 0

    print("Welcome to \"Guess My Number!\"")
    randomInt = random.randint(0,1000)
    quitGame = False
    while(not quitGame):
        # While the user doesn't want to quit, keep running the while loop
        print('\n---------------------\n')
        userInput = input("Would you like to Ask, Guess, or Quit: ").lower()
        if(userInput == 'quit'):
            # If the user wants to quit, break the while loop
            break
        elif(userInput == 'ask'):
            # If the user wants to ask the question.

            turnNumber+=1
            askIntException = False

            print('\nIf we subtract \"k\" from n, is the result divisible by \"m\"?')
            print('Conditions: 0 <= k < m and m is a prime under 1000\n')

            try:
                # Exception Handler to ensure that the input is an integer
                inputK = int(input('Input your \"k\" (Integers only please) :  '))
                inputM = int(input('Input your \"m\" (Integers only please) :  '))
            except:
                turnNumber-=1
                askIntException = True
                print('Please input integers for your \"k\" and \"m\"')

            if not askIntException:
                # If no exception was thrown.
                if( is_n_minus_k_divisible_by_m(randomInt, inputK, inputM) ):
                    # Check if (n-k) % m and other conditions.
                    print('YES, If we subtract ',inputK, ' from n, the result IS divisible by ',inputM)
                else:
                    print('NO, If we subtract ',inputK, ' from n, the result IS NOT divisible by ',inputM)

        elif(userInput == 'guess'):
            # If the user wants to guess the number

            turnNumber+=1
            guessIntException = False

            try:
                # Exception Handler to ensure that the input is an integer
                inputGuess = int(input('Input your guess (Integers only please) :  '))
            except:
                turnNumber-=1
                guessIntException = True
                print('Please input an integer for your guess')

            if not guessIntException:
                # If no exception was thrown.
                if(inputGuess == randomInt):
                    print('You guessed it!')
                    quitGame = True
                else:
                    print('Sorry, try again!')


    score = 0
    if(quitGame):
        # Calculates the score of the user if they won.
        score = math.ceil(randomInt*1.0/turnNumber)
        print('\n\nCongratulations!!!')

    print('Your score is: ',score, '\n')


if __name__ == '__main__':
    # When this is run as a script, run the game.
	run_Guess_My_Number()
