use soroban_sdk::{Env, String};

pub fn read_decimal() -> u32 {
    18
}

pub fn read_name(e: &Env) -> String {
    String::from_str(e, "NRX Token")
}

pub fn read_symbol(e: &Env) -> String {
    String::from_str(e, "NRX")
}
