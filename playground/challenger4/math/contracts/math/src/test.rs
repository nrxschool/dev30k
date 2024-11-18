#![cfg(test)]

extern crate std;

use core::u32;

use crate::contract::{MathContract, MathContractClient};
use crate::types::Op;
use soroban_sdk::testutils::storage::Instance;
use soroban_sdk::testutils::Ledger;
use soroban_sdk::Env;

#[test]
fn test_sum() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 10u32;
    let b = 12u32;
    let result = MathContractClient::new(&env, &contract_id).sum(&a, &b);
    assert_eq!(result, 22);
}

#[test]
fn test_sub() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 15u32;
    let b = 5u32;
    let result = MathContractClient::new(&env, &contract_id).sub(&a, &b);
    assert_eq!(result, 10);
}

#[test]
fn test_mul() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 3u32;
    let b = 7u32;
    let result = MathContractClient::new(&env, &contract_id).mul(&a, &b);
    assert_eq!(result, 21);
}

#[test]
fn test_div() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 20u32;
    let b = 4u32;
    let result = MathContractClient::new(&env, &contract_id).div(&a, &b);
    assert_eq!(result, 5);
}

#[test]
fn test_div_by_zero() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 20u32;
    let b = 0u32;
    let result = MathContractClient::new(&env, &contract_id).div(&a, &b);
    assert_eq!(result, u32::MAX);
}

#[test]
fn test_last_op() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 10u32;
    let b = 12u32;
    MathContractClient::new(&env, &contract_id).sum(&a, &b);
    let last_op = MathContractClient::new(&env, &contract_id).last_op();
    assert_eq!(last_op.op, Op::Sum);
}

#[test]
fn test_get_op() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 10u32;
    let b = 12u32;
    let _ = MathContractClient::new(&env, &contract_id).sum(&a, &b);
    let last_op = MathContractClient::new(&env, &contract_id).last_op();
    let retrieved_op = MathContractClient::new(&env, &contract_id).get_op(&last_op.id);
    assert_eq!(retrieved_op.id, last_op.id);
}

#[test]
fn test_all_op() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 10u32;
    let b = 12u32;
    let _ = MathContractClient::new(&env, &contract_id).sum(&a, &b);
    let operations = MathContractClient::new(&env, &contract_id).all_op();
    assert!(!operations.is_empty());
}

#[test]
fn test_sum_bad_case() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = u32::MAX;
    let b = 1u32;
    let result = MathContractClient::new(&env, &contract_id).sum(&a, &b);
    assert_eq!(result, u32::MAX);
}

#[test]
fn test_sum_bad_case2() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = u32::MAX - 10;
    let b = 11;
    let result = MathContractClient::new(&env, &contract_id).sum(&a, &b);
    assert_eq!(result, u32::MAX);
}

#[test]
fn test_sub_negative_case() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 5u32;
    let b = 10u32;
    let result = MathContractClient::new(&env, &contract_id).sub(&a, &b);
    assert_eq!(result, 5);
}

#[test]
fn test_sub_bad_case() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 0;
    let b = 0;
    let result = MathContractClient::new(&env, &contract_id).sub(&a, &b);
    assert_eq!(result, 0);
}

#[test]
fn test_mul_zero_case() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 0u32;
    let b = 10u32;
    let result = MathContractClient::new(&env, &contract_id).mul(&a, &b);
    assert_eq!(result, 0);
}

#[test]
fn test_div_by_zero_case() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let a = 20u32;
    let b = 0u32;
    let result = MathContractClient::new(&env, &contract_id).div(&a, &b);
    assert_eq!(result, u32::MAX);
}

#[test]
fn test_get_op_invalid_id() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let invalid_id = 999u32;
    let result = MathContractClient::new(&env, &contract_id).get_op(&invalid_id);
    assert_eq!(result.id, 0);
}

#[test]
fn test_all_op_empty_case() {
    let env = Env::default();
    let contract_id = env.register_contract(None, MathContract);
    let operations = MathContractClient::new(&env, &contract_id).all_op();
    assert!(operations.is_empty());
}

#[test]
#[should_panic(expected = "[testing-only] Accessed contract instance key that has been archived.")]
fn test_ttl_behavior() {
    // Configura o ambiente de teste com um ledger personalizado
    let env = Env::default();
    env.ledger().with_mut(|ledger| {
        // Define o número da sequência do ledger atual.
        ledger.sequence_number = 1_000_000;
        // Define o TTL mínimo e máximo para entradas de instância.
        ledger.min_persistent_entry_ttl = 500;
        ledger.max_entry_ttl = 1000;
    });

    // Registra o contrato no ambiente.
    let contract_id = env.register_contract(None, MathContract);
    let client = MathContractClient::new(&env, &contract_id);

    // Executa uma operação para garantir que uma entrada de armazenamento seja criada
    client.sum(&10, &20);

    let mut initial_ttl: u32 = 0;
    // Verifica o TTL inicial da instância
    env.as_contract(&contract_id, || {
        initial_ttl = env.storage().instance().get_ttl();
        println!("TTL inicial do contrato: {}", initial_ttl);
        assert!(initial_ttl > 0, "O TTL inicial deve ser maior que zero.");
    });

    // Avança o número da sequência do ledger para simular o tempo passando
    env.ledger().with_mut(|ledger| {
        // Avança o ledger em uma quantidade que leva o TTL próximo de zero
        ledger.sequence_number += initial_ttl as u32 - 1;
    });

    // Verifica que o TTL agora é próximo de zero
    env.as_contract(&contract_id, || {
        let near_expiry_ttl = env.storage().instance().get_ttl();
        println!("TTL próximo da expiração: {}", near_expiry_ttl);
        assert!(near_expiry_ttl <= 1, "O TTL deve estar próximo de expirar.");
    });

    // Avança o ledger para além do TTL, forçando a expiração
    env.ledger().with_mut(|ledger| {
        ledger.sequence_number += 1;
    });

    // Tenta acessar o armazenamento após a expiração e espera um erro ou zero
    env.as_contract(&contract_id, || {
        let expired_ttl = env.storage().instance().get_ttl();
        println!("TTL após a expiração: {}", expired_ttl);
        assert_eq!(expired_ttl, 0, "O TTL deve ser zero após a expiração.");
    });

    // TTL 0
    client.last_op();

    // Avança o ledger para além do TTL, forçando a expiração
    env.ledger().with_mut(|ledger| {
        ledger.sequence_number += 1;
    });

    // TTL -1
    client.last_op();
}
