use soroban_sdk::contracttype;

#[derive(Copy, Clone, Debug, Eq, PartialEq, PartialOrd, Ord)]
#[repr(u32)]
#[contracttype]
pub enum Op {
    Sum,
    Sub,
    Mul,
    Div,
}

#[contracttype]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Calculation {
    pub id: u32,
    pub op: Op,
    pub x: u32,
    pub y: u32,
    pub z: u32,
}

impl Calculation {
    pub fn new(id: u32, op: Op, x: u32, y: u32, z: u32) -> Self {
        Self { id, op, x, y, z }
    }
}
impl Default for Calculation {
    fn default() -> Self {
        Self {
            id: 0,
            op: Op::Sum,
            x: 0,
            y: 0,
            z: 0,
        }
    }
}
