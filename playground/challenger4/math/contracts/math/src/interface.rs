use crate::types::Calculation;
use soroban_sdk::{Env, Vec};

pub trait Math {
    fn sum(env: Env, x: u32, y: u32) -> u32;
    fn sub(env: Env, x: u32, y: u32) -> u32;
    fn mul(env: Env, x: u32, y: u32) -> u32;
    fn div(env: Env, x: u32, y: u32) -> u32;

    fn last_op(env: Env) -> Calculation;
    fn get_op(env: Env, id: u32) -> Calculation;
    fn all_op(env: Env) -> Vec<Calculation>;
}
