from nada_dsl import *

def nada_main():
    # Define two parties
    alice = Party(name="Alice")
    bob = Party(name="Bob")

    # Define their secret wealth values
    alice_wealth = SecretInteger(Input(name="alice_wealth", party=alice))
    bob_wealth = SecretInteger(Input(name="bob_wealth", party=bob))

    # Compare wealth (returns 1 if alice_wealth > bob_wealth, 0 otherwise)
    result = alice_wealth > bob_wealth

    # Return result to both parties
    return [
        Output(result, "comparison_result", alice),
        Output(result, "comparison_result", bob)
    ]