use crate::storage_types::{DataKey, INSTANCE_BUMP_AMOUNT, INSTANCE_LIFETIME_THRESHOLD};
use crate::types::{Calculation, Op};
use soroban_sdk::{vec, Env, Vec};

pub fn write(env: &Env, x: u32, y: u32, z: u32, op: Op) {
    // Get existing calculations or create new vector
    let mut calcs = read_all(env);

    // Get and increment calculation count
    let new_id = read_count(env) + 1;
    write_count(env, new_id);

    // Create and store new calculation
    let new_calc = Calculation::new(new_id, op, x, y, z);
    calcs.push_back(new_calc.clone());

    // Update storage
    env.storage().instance().set(&DataKey::Calculations, &calcs);
    env.storage()
        .instance()
        .set(&DataKey::LastCalculation, &new_calc);

    // Extend TTL
    extend_storage_ttl(env);
}

pub fn read_all(env: &Env) -> Vec<Calculation> {
    env.storage()
        .instance()
        .get(&DataKey::Calculations)
        .unwrap_or(vec![env])
}

pub fn read_last(env: &Env) -> Calculation {
    env.storage()
        .instance()
        .get(&DataKey::LastCalculation)
        .unwrap_or_default()
}

pub fn read_by_id(env: &Env, id: u32) -> Calculation {
    read_all(env)
        .iter()
        .find(|calc| calc.id == id)
        .unwrap_or_default()
}

fn write_count(env: &Env, count: u32) {
    env.storage()
        .instance()
        .set(&DataKey::CalculationCount, &count);
}

fn read_count(env: &Env) -> u32 {
    env.storage()
        .instance()
        .get(&DataKey::CalculationCount)
        .unwrap_or_default()
}

fn extend_storage_ttl(env: &Env) {
    env.storage()
        .instance()
        .extend_ttl(INSTANCE_LIFETIME_THRESHOLD, INSTANCE_BUMP_AMOUNT);
}
