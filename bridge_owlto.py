import asyncio
import json
import logging
import os
import sys

import httpx
from eth_typing import HexStr
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.middleware.geth_poa import async_geth_poa_middleware
from web3.types import Nonce, TxParams, Wei

from wallet import Wallet

wallets_id_for_bridge = [1, 2, 3]
bridge_btc_amount = "0.00013"

assert os.path.isfile("./wallets.json"), "accounts must be provided"
with open("./wallets.json", "r") as f:
    wallets: list[Wallet] = json.load(f)

# TODO:
wallets = [
    {
        "wallet_id": 1,
        "address": "0x9f638213287d827ef5210999787eb04cd9e3c315",
        "private_key": "",
        "mnemonic": "",
    }
]

w3_eth = AsyncWeb3(AsyncHTTPProvider("https://ethereum.blockpi.network/v1/rpc/public"))
client = httpx.AsyncClient(base_url="https://owlto.finance/api/bridge_api/v1")
w3_bitlayer = AsyncWeb3(AsyncHTTPProvider("https://rpc.bitlayer.org"))
w3_bitlayer.middleware_onion.inject(async_geth_poa_middleware, layer=0)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(module)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs.txt"),
    ],
)


async def send_tx(
    _from: str, _to: str, value: str, data: str, nonce: Nonce, private_key: str
):
    tx_params = TxParams(
        {
            "chainId": await w3_eth.eth.chain_id,
            "from": _from,
            "to": _to,
            "value": Wei(int(value)),
            "data": HexStr(data),
            "nonce": nonce,
        }
    )
    gas = await w3_eth.eth.estimate_gas(tx_params)
    tx_params["gas"] = gas
    gas_price = await w3_eth.eth.gas_price
    tx_params["maxFeePerGas"] = Wei(gas_price * 2)
    tx_params["maxPriorityFeePerGas"] = Wei(int(gas_price / 2))
    tx = w3_eth.eth.account.sign_transaction(tx_params, private_key)
    tx_hash = await w3_eth.eth.send_raw_transaction(tx.rawTransaction)
    return await w3_eth.eth.wait_for_transaction_receipt(tx_hash)


async def bridge(wallet: Wallet):
    res = await client.post(
        "/get_build_tx",
        json={
            "from_address": wallet["address"],
            "from_chain_name": "EthereumMainnet",
            "to_address": wallet["address"],
            "to_chain_name": "BitlayerMainnet",
            "token_name": "BTC",
            "ui_value": bridge_btc_amount,
        },
    )
    if res.json()["status"]["code"] != 0:
        logging.error(f'failed to build tx: {res.json()['status']['message']}')
    else:
        logging.info(f'bridging wallet_id: {wallet["wallet_id"]}')
        nonce = await w3_eth.eth.get_transaction_count(
            w3_eth.to_checksum_address(wallet["address"])
        )
        if (approve_body := res.json()["data"]["txs"]["approve_body"]) is not None:
            tx_receipt = await send_tx(
                approve_body["from"],
                approve_body["to"],
                approve_body["value"],
                approve_body["data"],
                nonce,
                wallet["private_key"],
            )
            logging.info(f"approve successfully for wallet_id: {wallet['wallet_id']}")
            logging.info(tx_receipt)
            nonce = Nonce(nonce + 1)
        transfer_body = res.json()["data"]["txs"]["transfer_body"]
        tx_receipt = await send_tx(
            transfer_body["from"],
            transfer_body["to"],
            transfer_body["value"],
            transfer_body["data"],
            nonce,
            wallet["private_key"],
        )
        logging.info(
            f"wallet_id: {wallet['wallet_id']} send bridging successfully, waiting for receiving funds..."
        )
        logging.info(tx_receipt)
        for _ in range(300):
            await asyncio.sleep(1)
            balance = await w3_bitlayer.eth.get_balance(
                w3_bitlayer.to_checksum_address(wallet["address"])
            )
            logging.info(f'wallet_id: {wallet["wallet_id"]} balance: {balance}')
            break
        else:
            logging.error(
                f'wallet_id: {wallet['wallet_id']} failed to receive funds on bitlayer'
            )


async def main():
    w3_connected = await w3_eth.is_connected()
    assert w3_connected, "failed to connect to eth rpc"
    w3_connected = await w3_bitlayer.is_connected()
    assert w3_connected, "failed to connect to bitlayer rpc"
    await asyncio.gather(
        *(
            [
                bridge(wallet)
                for wallet in wallets
                if wallet["wallet_id"] in wallets_id_for_bridge
            ]
        )
    )


asyncio.run(main())
{
    "status": {"code": 0, "message": ""},
    "data": {
        "token_name": "BTC",
        "from_chain_name": "EthereumMainnet",
        "to_chain_name": "BitlayerMainnet",
        "input_value": {"raw_value": "13000", "ui_value": "0.00013", "decimals": 8},
        "send_value": {"raw_value": "15500", "ui_value": "0.000155", "decimals": 8},
        "receive_value": {
            "raw_value": "130000000000000",
            "ui_value": "0.00013",
            "decimals": 18,
        },
        "gas_fee": {"raw_value": "2500", "ui_value": "2.5e-05", "decimals": 8},
        "bridge_fee": {"raw_value": "0", "ui_value": "0", "decimals": 8},
        "min_value": {"raw_value": "10000", "ui_value": "0.0001", "decimals": 8},
        "max_value": {"raw_value": "1000000", "ui_value": "0.01", "decimals": 8},
        "network_type": 1,
        "txs": {
            "approve_body": {
                "data": "0x095ea7b30000000000000000000000000e83ded9f80e1c92549615d96842f5cb64a08762000000000000000000000000000000000000000000000000000000000004baf0",
                "from": "0x2C70B21536D2D003b07995dE2eab93fA078d6275",
                "to": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
                "value": "0",
            },
            "transfer_body": {
                "data": "0xfc18063800000000000000000000000000000000000000000000000000000000000000c00000000000000000000000002260fac5e5542a773aa44fbcfedf7c193bc2c5990000000000000000000000005e809a85aa182a9921edd10a4163745bb3e362840000000000000000000000000000000000000000000000000000000000003c8c000000000000000000000000000000000000000000000000000000000000002a0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002a30783243373042323135333644324430303362303739393564453265616239336641303738643632373500000000000000000000000000000000000000000000",
                "from": "0x2C70B21536D2D003b07995dE2eab93fA078d6275",
                "to": "0x0e83DEd9f80e1C92549615D96842F5cB64A08762",
                "value": "0",
            },
        },
    },
}
