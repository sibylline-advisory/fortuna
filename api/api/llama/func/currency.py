import logging

log = logging.getLogger(__name__)


def send_currency(amount: float, currency: str, recipient: str) -> dict:
    """Send an amount of a chosen currency to a someone or something."""

    if currency == "USD":
        abi = [{
            "inputs": [{"internalType": "address", "name": "to", "type": "address"},
                       {"internalType": "uint256", "name": "value", "type": "uint256"}], "name": "transfer",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "nonpayable", "type": "function"
        }, {
            "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
            "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view", "type": "function"
        }, {
            "inputs": [], "name": "decimals",
            "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view",
            "type": "function"
        }]


        # TODO: resolve ens for to value
        args = [recipient, amount]

        return_dict = {
            "abi": abi,
            "args": args,
            "contract": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
        }
        log.info(f"Returning {return_dict}")

        return return_dict
    else:
        pass

    return {}
