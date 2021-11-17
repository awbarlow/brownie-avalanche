from scripts.helper import get_account
from brownie import interface, config, network
from web3 import Web3

assets = { 'Aave Avalanche Market USDC' : "0x46a51127c3ce23fb7ab1de06226147f446e4a857",
           'Aave Avalanche Market variable debt vUSDC' : '0x848c080d2700cbe1b894a3374ad5e887e5ccb89c',
           'Aave Avalanche Market DAI' : '0x47afa96cdc9fab46904a55a6ad4bf6660b53c38a',
           'Aave Avalanche Market variable debt vDAI' : '0x1852dc24d1a8956a0b356aa18ede954c7a0ca5ae',
           'Aave Avalanche Market variable debt vWAVAX ' : '0x66a0fe52fb629a6cb4d10b8580afdffe888f5fd4',
           'Aave Avalanche Market WAVAX' : '0xdfe521292ece2a4f44242efbcd66bc594ca9714b'}

def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def get_incentive_balance(assets,account):
    incentive = interface.IAaveIncentivesController(config["networks"][network.show_active()]["aave_incetives"])
    balance = incentive.getRewardsBalance(list(assets.values()), account.address)
    return balance

def main():
    account = get_account()

    incentives = get_incentive_balance(assets, account)

    print(incentives/(10**18))
