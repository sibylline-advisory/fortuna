import logging
import requests
import time

log = logging.getLogger(__name__)

# TODO get these from an index or service provider.
asset_categories = {
    "recommended": {
        "decimals": 18,
        "address": "0xAd3fe5Aeabf79B8291F877B367139466c221216e",
        "name": "Bitcoin",
        "symbol": "BTC",
    },
    "high_risk": {
        "decimals": 18,
        "address": "0xAd3fe5Aeabf79B8291F877B367139466c221216e",
        "name": "Joe Boden",
        "symbol": "JOE",
    },
    "low_risk": {
        "decimals": 18,
        "address": "0xAd3fe5Aeabf79B8291F877B367139466c221216e",
        "name": "Ethereum",
        "symbol": "ETH",
    }
}


def get_digital_asset_prices(asset: dict) -> dict:
    """Returns the price of a digital asset"""
    url = "https://api.transpose.io/prices/price"
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': '1YZ5KgCpDkVhhHG2QwvL05Neft2BFtxF',  # TODO delete lol
    }
    params = {
        "chain_id": "base",
        "token_addresses": [asset.get("address")]
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {}


def purchase_digital_asset(amount_in: float, asset_class: str) -> dict:
    """Purchases a digital asset using a DEX"""
    abi = [
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "amountIn",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "amountOutMin",
                    "type": "uint256"
                },
                {
                    "internalType": "address[]",
                    "name": "path",
                    "type": "address[]"
                },
                {
                    "internalType": "address",
                    "name": "to",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "deadline",
                    "type": "uint256"
                }
            ],
            "name": "swapExactTokensForTokens",
            "outputs": [
                {
                    "internalType": "uint256[]",
                    "name": "amounts",
                    "type": "uint256[]"
                }
            ],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    asset_details = asset_categories[asset_class]

    token_in_decimals = 6
    token_in_address = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
    token_out_address = asset_details.get("address")
    token_out_decimals = asset_details.get("decimals")

    amount_in = (amount_in * 10 ** token_in_decimals).toString()

    token_in_price = get_digital_asset_prices({
        "address":
            "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
    }).get("price")
    token_out_price = get_digital_asset_prices(asset_details).get("price")

    # 5. Calculate Minimum Amount Out:
    #    - Calculate the expected amount of tokens to receive based on the token prices and apply a slippage
    #    tolerance (e.g., 1%).
    slippage_tolerance = 0.01
    amount_out_min = int(
        round(amount_in * token_in_price / token_out_price * (1 - slippage_tolerance), token_out_decimals))

    # amountIn = '1000000000000000000'; // 1 WBNB (18 decimals)
    amount_in = (amount_in * 10 ** token_in_decimals).toString()
    # amountOutMin = '300000000000000000000'; // Minimum 300 BUSD (18 decimals)
    amount_out_min = str(amount_out_min)
    path = [token_in_address, token_out_address]
    deadline = int(time.time()) + 60 * 20  # 20 minutes from now

    args = [amount_in, amount_out_min, path, "clientWalletAddress", deadline]

    return_dict = {
        "abi": abi,
        "args": args,
        "contract": "0xAd3fe5Aeabf79B8291F877B367139466c221216e",
    }
    log.info(f"Returning {return_dict}")
    return return_dict
