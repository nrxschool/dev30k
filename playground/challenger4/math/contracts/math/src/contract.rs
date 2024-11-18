use crate::interface::Math;
use crate::storage;
use crate::types::{Calculation, Op};
use soroban_sdk::{contract, contractimpl, Env, Vec};

#[contract]
pub struct MathContract;

#[contractimpl]
impl Math for MathContract {

    fn sum(e: Env, x: u32, y: u32) -> u32 {
        let z;

        if x >= u32::MAX - y {
            z = u32::MAX;
            storage::write(&e, x, y, z, Op::Sum);
            return z;
        }

        let z = x + y;
    
        storage::write(&e, x, y, z, Op::Sum);
        z
    }

    fn sub(e: Env, x: u32, y: u32) -> u32 {
        let z = if x < y { y - x } else { x - y };
        storage::write(&e, x, y, z, Op::Sub);
        z
    }

    fn mul(e: Env, x: u32, y: u32) -> u32 {
        let z = x * y;
        storage::write(&e, x, y, z, Op::Mul);
        z
    }

    fn div(e: Env, x: u32, y: u32) -> u32 {
        let z = if y == 0 { u32::MAX } else { x / y };
        storage::write(&e, x, y, z, Op::Div);
        z
    }

    fn last_op(e: Env) -> Calculation {
        storage::read_last(&e)
    }

    fn get_op(e: Env, id: u32) -> Calculation {
        storage::read_by_id(&e, id)
    }

    fn all_op(e: Env) -> Vec<Calculation> {
        storage::read_all(&e)
    }
}
