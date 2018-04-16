'''a1_basic_tests.py

This program makes a few tests of the two special functions in
your program for Assignment 1.

Although passing the tests does not guarantee your functions are
completely correct, it does give you some evidence for correctness.

S. Tanimoto, Jan. 4, 2018.
'''

from hungs3_A1 import isPrimeUnder1000, is_n_minus_k_divisible_by_m


SOME_PRIMES = [2, 3, 5, 101, 997]

SOME_NON_PRIMES = [0, 1, 4, 9, 100, 999]

def prime_tests():
  passing = True
  for n in SOME_PRIMES:
    if not isPrimeUnder1000(n):
      print("Error : "+str(n)+" is actually prime.")
      passing = False
  return passing

def non_prime_tests():
  passing = True
  for n in SOME_NON_PRIMES:
    if isPrimeUnder1000(n):
      print("Error : "+str(n)+" is actually NOT prime.")
      passing = False
  return passing

OK_TRIPLES = [(10, 0, 2), (35, 2, 11), (35, 9, 13),(998, 1, 997)]
NON_OK_TRIPLES = [(10, 1, 2), (35, 5, 11), (35, 0, 9),(998, 2, 997)]

def divisibility_tests():
  passing = True
  for triple in OK_TRIPLES:
    n, k, m = triple
    if not is_n_minus_k_divisible_by_m(n, k, m):
      print("Error : "+str(triple)+" is actually OK.")
      passing = False
  return passing

def non_divisibility_tests():
  passing = True
  for triple in NON_OK_TRIPLES:
    n, k, m = triple
    if is_n_minus_k_divisible_by_m(n, k, m):
      print("Error : "+str(triple)+" is actually NOT OK.")
      passing = False
  return passing

def do_all_tests():
  if prime_tests():
    print("Passed the prime tests.")
  else:
    print("Did not pass all the prime tests.")
  if non_prime_tests():
    print("Passed the non-prime tests.")
  else:
    print("Did not pass all the non-prime tests.")
  if divisibility_tests():
    print("Passed the divisibility tests.")
  else:
    print("Did not pass all the divisibility tests.")
  if non_divisibility_tests():
    print("Passed the non-divisibility tests.")
  else:
    print("Did not pass all the non-divisibility tests.")

do_all_tests()