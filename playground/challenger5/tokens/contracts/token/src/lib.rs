#![no_std]

mod admin;
mod allowance;
mod balance;
mod contract;
mod error;
mod metadata;
mod storage_types;

mod test;

pub use crate::contract::TokenClient;
