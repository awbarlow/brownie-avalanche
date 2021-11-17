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

def claim_rewards(assets,account,balance):
    incentive = interface.IAaveIncentivesController(config["networks"][network.show_active()]["aave_incetives"])
    tx = incentive.claimRewards(list(assets.values()), balance, account.address, {"from": account})
    tx.wait(1)
    return tx

def unwrap_all(account):
    wavax_address = config["networks"][network.show_active()]["wavax_address"]
    wavax = interface.IERC20(wavax_address)
    wavax_bal = wavax.balanceOf(account)
    wavax_interface = interface.WethInterface(config["networks"][network.show_active()]["wavax_address"])
    tx = wavax_interface.withdraw(wavax_bal, {"from": account})
    tx.wait(1)
    return tx

def get_avax_gateway():
    gateway = interface.IWETHGateway(config["networks"][network.show_active()]["eth_gateway"])
    return gateway

def deposit_wavax(amount,account):
    gateway = get_avax_gateway()
    lending_pool = get_lending_pool()
    tx = gateway.depositETH(lending_pool.address, account.address, 0, {"from": account,"value": amount})
    tx.wait(1)
    print(f"Deposited: {amount/(10**18)} AVAX")
    return tx

def main():
    account = get_account()

    bal = get_incentive_balance(assets, account)

    print(bal/(10**18))

    if bal > Web3.toWei(0.7, "ether"):
        # Claim - while loop allows for failures which tends to happen
        attempt1 = 0
        claim = False
        while attempt1 <= 10 and claim != True:
            try:
                # Claim the reward
                tx1 = claim_rewards(assets, account, bal)
                tx1.wait(1)
                claim = True
            except:
                attempt1 += 1
                time.sleep(5)
                pass

    wavax_address = config["networks"][network.show_active()]["wavax_address"]
    wavax = interface.IERC20(wavax_address)
    wavax_bal = wavax.balanceOf(account)

    if wavax_bal >= Web3.toWei(0.05, "ether"):
        # Claim - while loop allows for failures which tends to happen
        attempt2 = 0
        unwrap = False
        while attempt2 <= 10 and unwrap != True:
            try:
                tx2 = unwrap_all(account)
                tx2.wait(1)
                unwrap = True
            except:
                attempt2 += 1
                time.sleep(5)
                pass

    avax_balance = account.balance()
    deposit_cond = False
    if avax_balance > Web3.toWei(1, "ether"):
        amount = matic_balance - Web3.toWei(0.2, "ether")
        deposit_cond = True

    if deposit_cond == True:
        deposit = False
        attempt3 = 0
        while attempt3 <= 10 and deposit != True:
            try:
                tx3 = deposit_wmatic(amount, account)
                tx3.wait(1)
                deposit = True
            except:
                attempt3 += 1
                time.sleep(5)
                pass

            if deposit == True:
                message = f"""\  
                            Subject: AVAX Rewards Deposited  

                            Account:  {account}  

                            Rewards reinvested: {amount / (10 ** 18)} AVAX
                            """
                    send_message(message)
