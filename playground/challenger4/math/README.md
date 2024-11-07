# Soroban Project

## Project Structure

This repository uses the recommended structure for a Soroban project:

```text
.
├── contracts
│   └── hello_world
│       ├── src
│       │   ├── lib.rs
│       │   └── test.rs
│       └── Cargo.toml
├── Cargo.toml
└── README.md
```

## How to config

- Wallet

```
stellar keys generate alice --network local
stellar keys fund alice --network local
```

- Network

```
stellar network add local \
    --rpc-url "http://localhost:8000/soroban/rpc" \
    --network-passphrase "Standalone Network ; February 2017"
```

## How to Compile

```
stellar contract build
```

## How to Test

```
cargo test
```

## How to Deploy

- install .wasm

```
stellar contract install \
  --wasm target/wasm32-unknown-unknown/release/math.wasm \
  --source alice \
  --network local
```

- create contract from .wasm

```
stellar contract deploy \
  --wasm-hash WASM_ID \
  --source alice \
  --network local
```

## How to Interact

```
stellar contract invoke \
  --id CONTRACT_ID \
  --source alice \
  --network local \
  -- \
  hello \
  --to Lucas
```