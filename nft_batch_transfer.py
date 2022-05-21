# %%
from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware
import pandas as pd
import numpy as np
import json

# put the the private keys above here
private_keys = [
    '0x91113e12b8df6be7bbe4a4e5b7d536a382b5e75009b2c471dee916c7bd0f29d5',
    '0x526c33242f6662c2cbb23e0af5df5f252872670ec656ed03d6b57217932c9e34'
]

accounts = [Account.from_key(key).address for key in private_keys]

with open('Farm.json', 'r') as f:
    abi = json.loads(f.read())

farm_addr = '0x2B4A66557A79263275826AD31a4cDDc2789334bD'

# http provider here
provider = 'https://rpc.ankr.com/polygon'

w3 = Web3(Web3.HTTPProvider(provider))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

farm_contract = w3.eth.contract(address=farm_addr, abi=abi)

farm_amounts = [farm_contract.functions.balanceOf(a).call() for a in accounts]

total_farm_amount = sum(farm_amounts)

print('total farm amount is ', total_farm_amount)


# %%
def create_accounts(amount):
    accounts = []
    for _ in range(amount):
        acct = Account.create()
        accounts.append({'address': acct.address, 'key': acct.key.hex()})
    return accounts


pd.DataFrame(create_accounts(total_farm_amount)).to_csv('new_accounts.csv',
                                                        index=False)

# %%
new_accounts = pd.read_csv('new_accounts.csv').reset_index()
# %%
accounts_farm_amount_cumsum = [0]
accounts_farm_amount_cumsum.extend(np.cumsum(farm_amounts).tolist())
# %%
for i, acct in enumerate(accounts):
    print('current account is ', acct)

    base_nonce = w3.eth.get_transaction_count(acct)

    tokenIds = [
        farm_contract.functions.tokenOfOwnerByIndex(acct, j).call()
        for j in range(farm_amounts[i])
    ]

    print('current account has ', len(tokenIds), ' farms')

    for j, token_id in enumerate(tokenIds):
        print('current transfering tokenId is ', token_id)

        transfer_tx = farm_contract.functions.transferFrom(
            acct, new_accounts.loc[accounts_farm_amount_cumsum[i] + j,
                                   'address'], token_id).buildTransaction({
                                       'from':
                                       acct,
                                       'nonce':
                                       base_nonce + j
                                   })

        signed_transfer_tx = w3.eth.account.sign_transaction(
            transfer_tx, private_keys[i])

        hash = w3.eth.send_raw_transaction(signed_transfer_tx.rawTransaction)

        print('transfer transaction sended with hash: ', hash.hex())
