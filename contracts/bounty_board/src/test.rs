#![cfg(test)]

use super::*;
use soroban_sdk::{testutils::Address as _, Address, Env};

#[test]
fn test_create_bounty_fee_bps_boundary_min() {
    let env = Env::default();
    env.mock_all_auths();

    let contract_id = env.register_contract(None, BountyBoardContract);
    let client = BountyBoardContractClient::new(&env, &contract_id);

    let creator = Address::generate(&env);
    let token = Address::generate(&env);
    
    let result = client.try_create_bounty(
        &creator,
        &String::from_str(&env, "Test Bounty"),
        &String::from_str(&env, "Description"),
        &token,
        &1000,
        &0,
    );
    
    assert!(result.is_ok());
}

#[test]
fn test_create_bounty_fee_bps_boundary_max() {
    let env = Env::default();
    env.mock_all_auths();

    let contract_id = env.register_contract(None, BountyBoardContract);
    let client = BountyBoardContractClient::new(&env, &contract_id);

    let creator = Address::generate(&env);
    let token = Address::generate(&env);
    
    let result = client.try_create_bounty(
        &creator,
        &String::from_str(&env, "Test Bounty"),
        &String::from_str(&env, "Description"),
        &token,
        &1000,
        &10000,
    );
    
    assert!(result.is_ok());
}

#[test]
fn test_create_bounty_fee_bps_above_max() {
    let env = Env::default();
    env.mock_all_auths();

    let contract_id = env.register_contract(None, BountyBoardContract);
    let client = BountyBoardContractClient::new(&env, &contract_id);

    let creator = Address::generate(&env);
    let token = Address::generate(&env);
    
    let result = client.try_create_bounty(
        &creator,
        &String::from_str(&env, "Test Bounty"),
        &String::from_str(&env, "Description"),
        &token,
        &1000,
        &10001,
    );
    
    assert!(result.is_err());
}

#[test]
fn test_create_bounty_fee_bps_edge_cases() {
    let env = Env::default();
    env.mock_all_auths();

    let contract_id = env.register_contract(None, BountyBoardContract);
    let client = BountyBoardContractClient::new(&env, &contract_id);

    let creator = Address::generate(&env);
    let token = Address::generate(&env);
    
    let test_cases = vec![&env, 0, 1, 5000, 9999, 10000];
    
    for fee_bps in test_cases.iter() {
        let result = client.try_create_bounty(
            &creator,
            &String::from_str(&env, "Test Bounty"),
            &String::from_str(&env, "Description"),
            &token,
            &1000,
            fee_bps,
        );
        assert!(result.is_ok(), "fee_bps {} should be valid", fee_bps);
    }
}

#[test]
fn test_create_bounty_fee_bps_invalid_values() {
    let env = Env::default();
    env.mock_all_auths();

    let contract_id = env.register_contract(None, BountyBoardContract);
    let client = BountyBoardContractClient::new(&env, &contract_id);

    let creator = Address::generate(&env);
    let token = Address::generate(&env);
    
    let invalid_cases = vec![&env, 10001, 15000, 20000, 100000];
    
    for fee_bps in invalid_cases.iter() {
        let result = client.try_create_bounty(
            &creator,
            &String::from_str(&env, "Test Bounty"),
            &String::from_str(&env, "Description"),
            &token,
            &1000,
            fee_bps,
        );
        assert!(result.is_err(), "fee_bps {} should be invalid", fee_bps);
    }
}
