import logging

log = logging.getLogger(__name__)


#  TODO implement proper ENS and name book lookup
def convert_name_to_address(name: str) -> str:
    if name == "3266miles.eth":
        return "0x9BF4E958BE655297df383f67A4ff8435b032F1B8"  # μίλια.eth safe
    elif name == "harper":
        return "0x8f56A5cF7c56a01118d2C5992146473D32b5f612"  # harper safe
    else:
        return "0xA87122E39391B7A1C6a5d1D7166b1c3bd5eB6843"  # μίλια.eth


def send_currency(amount: float, currency: str, recipient: str) -> dict:
    """Send an amount of a chosen currency to a someone or something."""
    if currency == "USD":
        amount_in_wei = int(amount * 10 ** 6)  # TODO fix this properly
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

        args = [convert_name_to_address(recipient), amount_in_wei]

        return_dict = {
            "abi": abi,
            "args": args,
            "contract": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
        }
        log.info(f"Returning {return_dict}")
        return return_dict
    else:
        # TODO impl.
        pass
    return {}


def get_account_balances(account: str) -> dict:
    """Get the balances of an account."""
    import requests
    url = "https://api.transpose.io/token/tokens-by-contract-address"
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': '1YZ5KgCpDkVhhHG2QwvL05Neft2BFtxF',  # TODO delete lol
    }
    params = {
        "chain_id": "base",
        "contract_addresses": account,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.ok:
        return response.json()
    else:
        return {}
