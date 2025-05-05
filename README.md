# Millionaire's Problem in Nillion

This repository demonstrates the [Millionaire's Problem](https://en.wikipedia.org/wiki/Yao%27s_Millionaire_problem) using Nillion, a platform for secure multi-party computation. The problem involves two parties (Alice and Bob) determining who is wealthier without revealing their actual wealth to each other.

## Project Structure

- `nada_programs/`: Contains the NADA program that defines the secure computation
- `client_code/`: Contains the client code to execute the computation on the Nillion network

## Setup Instructions

1. **Create and activate a virtual environment**:

   ```bash
   python -m venv ~/.virtualenvs/nillion-env
   source ~/.virtualenvs/nillion-env/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## The NADA Program

The NADA program (`millionaire_problem.py`) defines the secure computation:

```python
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
```

## Running the Program

### 1. Build the NADA program

```bash
cd millionaire-problem/nada_programs/
nada build
```

### 2. Test the NADA program

Generate a test case:

```bash
nada generate-test --test-name millionaire_problem_test millionaire_problem
```

Run the test:

```bash
nada test millionaire_problem_test
```

### 3. Start the Nillion development network

```bash
nillion-devnet
```

### 4. Run the client application

```bash
cd ../client_code/
python3 millionaire_problem.py
```

## Example Output

When you run the client application, you should see output similar to:

```
💰  Adding funds to Alice's client balance: 3000000 uNIL
💰  Adding funds to Bob's client balance: 3000000 uNIL
-----STORE PROGRAM
Stored program_id: bec552a3efed38daa4574a7b89641f17b0665893/millionaire_problem/sha256/d247c95dc8623469aea2a0b86e8b4bbcd11029ae3196a127487819a02436325e
-----STORE ALICE'S SECRET
Stored Alice's wealth with values_id: 460b849e-2e5e-4dda-9351-440bbd8ec9f0
-----COMPUTE
Invoking computation using program bec552a3efed38daa4574a7b89641f17b0665893/millionaire_problem/sha256/d247c95dc8623469aea2a0b86e8b4bbcd11029ae3196a127487819a02436325e and Alice's values id 460b849e-2e5e-4dda-9351-440bbd8ec9f0
The computation was sent to the network. compute_id: 37811fd4-2da9-47c0-8aa1-77b3db0d88da

----- RESULTS -----
Alice's wealth: $1000000
Bob's wealth: $800000

Is Alice richer than Bob? Yes
Alice's view of the result: {'comparison_result': SecretBoolean(true)}
Bob's view of the result: {'comparison_result': SecretBoolean(true)}
```

## How it Works

1. The NADA program defines the secure computation logic
2. The client application:
   - Allocates funds to Alice and Bob
   - Stores the program on the Nillion network
   - Stores Alice's and Bob's secret wealth values
   - Executes the computation
   - Retrieves and displays the results

The key feature is that neither party reveals their actual wealth - they only learn who is wealthier.
