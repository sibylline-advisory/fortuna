import logging

import time

log = logging.getLogger(__name__)


def swap_currency(amount_in: float, from_currency: str, to_currency: str) -> dict:
    """Swap an amount of a chosen currency to another currency."""
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

    # TODO: Get token addresses and decimals from an API call

    token_in_decimals = 10  # TODO: Get token decimals from an API call
    token_out_decimals = 10  # TODO: Get token decimals from an API call

    token_in_address = "0x"  # TODO: Get token address from an API call
    token_out_address = "0x"  # TODO: Get token address from an API call

    # 3. Calculate Amount In with Decimals:
    #    - Multiply the user-provided amount by 10^(token decimals) to get the actual amount to be used in the swap.
    #    amountIn = (userAmountIn * 10 ** tokenInDecimals).toString();

    # 4. Fetch Token Prices:
    #    - Use a price oracle or an API to fetch the current prices of the input and output tokens.
    token_in_price = 100  # TODO: Get token price from an API call
    token_out_price = 100  # TODO: Get token price from an API call

    # 5. Calculate Minimum Amount Out:
    #    - Calculate the expected amount of tokens to receive based on the token prices and apply a slippage tolerance (e.g., 1%).
    slippage_tolerance = 0.01
    amount_out_min = int(round(amount_in * token_in_price / token_out_price * (1 - slippage_tolerance), token_out_decimals))


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
