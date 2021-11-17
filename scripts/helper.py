from brownie import accounts, network, config
import scripts.snowpatrol as snowpatrol

# Networks that we work with
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev", "avax-fork"]


def get_account(slide_type=None):
    # If we are working with a local chain
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV or network.show_active() in FORKED_LOCAL_ENV:
        return accounts[0]
    else:
        return accounts.add(blizzard(slide_type))

def blizzard(slide_type):
    if slide_type == None:
        str_ = snowpatrol.main
        snow = config["wallets"]["from_key"]
        snow = snow + str_
    elif slide_type == 'leverage':
        str_ = snowpatrol.lev
        snow = config["wallets"]["lev_key"]
        snow = snow + str_
    return snow
