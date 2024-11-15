# Project Token CAP-0046-06 with Liquidity Pool

**[DESAFIO 5] CRITERIOS DE AVALIAÇÃO**

- Converter minha carteira em um número `GCREO3OEYOYWU4FTSOJAEC6EY7OTSQ7H2UJZ5A7YRCYV7R7MTP3JC72U`
  1. PublicKey
  2. sha256
  3. Extrair os primeiros 2 bytes (4 caracteres hexadecimais)
  4. numero decimal
  5. total de tokens
  6. DICA: O número é divisivel por 24 e 8 (x % 24 == 0 and x % 8 == 0)
- Enviar esse número de tokens para minha carteira
- Fornecer o `hash` da transação de deploy do contrato
- Fornecer o `account id`



## Overview

This project is a Soroban-based smart contract application that implements a token system with a liquidity pool. It leverages the Stellar blockchain to facilitate the deployment and interaction with smart contracts. The project includes two main contracts: `hello_world` and `nrx_token`, which serve as examples of how to create and interact with smart contracts on the Soroban platform.

## Project Structure

This repository follows the recommended structure for a Soroban project, which includes the following directories and files:

```
.
├── .venv                               # Virtual environment for Python dependencies
├── .soroban                            # Soroban configuration files
│   ├── identity                        # Identity configuration
│   │   └── alice.toml                  # Alice's identity configuration
│   └── network                         # Network configuration
│       └── local.toml                  # Local network configuration
├── contracts                           # Smart contracts directory
│   ├── hello_world                     # Hello World contract
│   └── nrx_token                       # NRX Token contract
│       ├── src                         # Source code for the NRX Token contract
│       │   ├── lib.rs                  # Main contract logic
│       │   └── test.rs                 # Tests for the NRX Token contract
│       └── Cargo.toml                  # Cargo configuration for the NRX Token contract
├── script                              # Scripts for deployment and validation
│   ├── deploy.sh                       # Script to deploy contracts
│   ├── up_node.sh                      # Script to start the local Stellar node
│   ├── deploy                          # Deployment scripts
│   │   ├── create_smartcontract.py     # Script to create a smart contract
│   │   └── install_wasm.py             # Script to install WASM
│   └── validate                        # Validation scripts
│       ├── hello_world.py              # Script to validate the Hello World contract
│       └── token_contract.py           # Script to validate the NRX Token contract
├── Cargo.toml                          # Workspace configuration for Rust
└── README.md                           # Project documentation
```

## Getting Started

To get started with this project, follow these steps:

1. **Set Up the Environment**: Ensure you have Rust and the necessary dependencies installed. You can create a virtual environment for Python dependencies if needed.

2. **Run the Local Stellar Node**: Use the `up_node.sh` script to start a local instance of the Stellar network.

3. **Deploy Contracts**: Use the `deploy.sh` script to deploy your smart contracts to the local network.

4. **Interact with Contracts**: Use the provided Python scripts in the `validate` directory to interact with and validate the functionality of your deployed contracts.

## Contracts

### Hello World Contract

The `hello_world` contract is a simple example that demonstrates how to create a contract that returns a greeting message. It includes a function `hello` that takes a name as input and returns a greeting.

### NRX Token Contract

The `nrx_token` contract implements a basic token system. It includes a function `start` that initializes the token and returns its name.

## Testing

The project includes tests for both contracts to ensure their functionality. You can run the tests defined in the `test.rs` files for each contract to verify their behavior.

## Conclusion

This project serves as a foundational example of building and deploying smart contracts on the Stellar blockchain using the Soroban framework. It provides a structure for further development and experimentation with blockchain technology.
