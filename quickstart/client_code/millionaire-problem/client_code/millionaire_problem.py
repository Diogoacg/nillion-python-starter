"""
Millionaire Problem Example

Alice and Bob want to know who is richer without revealing their actual wealth.
This program:
1. Imports necessary packages
2. Connects to the local nillion-devnet
3. Stores the millionaire program
4. Stores a secret (Alice's wealth)
5. Computes the program with Bob's wealth as a computation-time secret
6. Returns the computation result (1 if Alice is richer, 0 if Bob is richer)
"""

import asyncio
import os

from nillion_client import (
    InputPartyBinding,
    Network,
    NilChainPayer,
    NilChainPrivateKey,
    OutputPartyBinding,
    Permissions,
    SecretInteger,
    VmClient,
    PrivateKey,
)
from dotenv import load_dotenv

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


async def main():
    # Initial setup/config, then initialize the NillionClient against nillion-devnet
    network = Network.from_config("devnet")

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    nilchain_key: str = os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0")  # type: ignore
    payer = NilChainPayer(
        network,
        wallet_private_key=NilChainPrivateKey(bytes.fromhex(nilchain_key)),
        gas_limit=10000000,
    )

    # Create two keys to identify Alice and Bob
    alice_key = PrivateKey()
    bob_key = PrivateKey()
    
    # Create clients for Alice and Bob
    alice_client = await VmClient.create(alice_key, network, payer)
    bob_client = await VmClient.create(bob_key, network, payer)
    
    program_name = "millionaire_problem"
    program_mir_path = "../nada_programs/target/millionaire_problem.nada.bin"

    # Adding funds to clients' balances
    funds_amount = 3000000
    print(f"💰  Adding funds to Alice's client balance: {funds_amount} uNIL")
    await alice_client.add_funds(funds_amount)
    
    print(f"💰  Adding funds to Bob's client balance: {funds_amount} uNIL")
    await bob_client.add_funds(funds_amount)

    # Store the program
    print("-----STORE PROGRAM")
    try:
        program_mir = open(program_mir_path, "rb").read()
    except FileNotFoundError:
        print(f"ERROR: Could not find compiled program at {program_mir_path}")
        print("Make sure to compile the program first with: nillion nada build")
        return
        
    program_id = await alice_client.store_program(program_name, program_mir).invoke()
    print(f"Stored program_id: {program_id}")

    # Store Alice's wealth as a secret
    print("-----STORE ALICE'S SECRET")
    alice_wealth = 1000000  # Alice has $1,000,000
    
    alice_values = {
        "alice_wealth": SecretInteger(alice_wealth),
    }

    # Create permissions for computation
    alice_permissions = Permissions.defaults_for_user(alice_client.user_id).allow_compute(
        alice_client.user_id, program_id
    ).allow_compute(bob_client.user_id, program_id)

    # Store Alice's secret
    alice_values_id = await alice_client.store_values(
        alice_values, ttl_days=5, permissions=alice_permissions
    ).invoke()
    
    print(f"Stored Alice's wealth with values_id: {alice_values_id}")

    # Set up for computation
    print("-----COMPUTE")

    # Bind the parties in the computation
    input_bindings = [
        InputPartyBinding("Alice", alice_client.user_id),
        InputPartyBinding("Bob", bob_client.user_id)
    ]
    
    output_bindings = [
        OutputPartyBinding("Alice", [alice_client.user_id]),
        OutputPartyBinding("Bob", [bob_client.user_id])
    ]

    # Bob's wealth as a computation-time secret
    bob_wealth = 800000  # Bob has $800,000
    compute_time_values = {"bob_wealth": SecretInteger(bob_wealth)}

    # Compute using Bob's client, with Bob's wealth and Alice's stored wealth
    print(f"Invoking computation using program {program_id} and Alice's values id {alice_values_id}")
    compute_id = await bob_client.compute(
        program_id,
        input_bindings,
        output_bindings,
        values=compute_time_values,
        value_ids=[alice_values_id],
    ).invoke()

    # Return the computation result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    
    # Both parties can retrieve the result
    alice_result = await alice_client.retrieve_compute_results(compute_id).invoke()
    bob_result = await bob_client.retrieve_compute_results(compute_id).invoke()
    
    print("\n----- RESULTS -----")
    print(f"Alice's wealth: ${alice_wealth}")
    print(f"Bob's wealth: ${bob_wealth}")
    
    is_alice_richer = bool(alice_result["comparison_result"])
    print(f"\nIs Alice richer than Bob? {'Yes' if is_alice_richer else 'No'}")
    print(f"Alice's view of the result: {alice_result}")
    print(f"Bob's view of the result: {bob_result}")
    
    alice_client.close()
    bob_client.close()
    
    return alice_result


if __name__ == "__main__":
    asyncio.run(main())