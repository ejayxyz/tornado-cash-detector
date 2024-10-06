# log these: transaction hash & funded address & value of sent ether
# testable blocks: 20031962, 17475649, 20877171

import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

def get_env(env_var):
    value = os.getenv(env_var)
    if value is None:
        raise KeyError(f"Environment variable '{env_var}' is not set.")
    return value

try:
    rpc_url = get_env('RPC_URL')
    tornado_cash_address = get_env('TORNADO_CASH_ADDRESS')
    print(f"RPC URL: {rpc_url}")
    print(f"Investigated Tornado Cash Address: {tornado_cash_address}")
    print('-' * 70)
except KeyError as e:
    print(f"Error: {e}")
    exit(1)

w3 = Web3(Web3.HTTPProvider(rpc_url)) 
foundSuspiciousTx = False

def get_block_number():
    while True:
        try:
            block_number = int(input("Enter the Ethereum block number: "))
            return block_number
        except ValueError:
            print("Invalid input. Please enter a valid integer for the block number.")

def process_tx(transaction, txHash: str, top_level: bool =True):
    if top_level:
        calls = transaction.get('result').get('calls')
    else:
        calls = transaction.get('calls')
    if calls and len(calls) > 0:
        for child_tx in calls:
            if child_tx.get('from').lower() == tornado_cash_address.lower():
                global foundSuspiciousTx
                foundSuspiciousTx = True
                print('Tornado Cash transaction detected:')
                print(f" - Transaction Hash: {txHash}")
                print(f" - From: {child_tx.get('from')}")
                print(f" - To: {child_tx.get('to')}")
                print(f" - Value: {w3.from_wei(int(child_tx.get('value'), 0), 'ether')} ETH")
                print('-' * 70)
            process_tx(child_tx, txHash, False)

def detect_tornado_cash_transfers_in_block(block_number):
    
    blockResponse = w3.provider.make_request('debug_traceBlockByNumber', [hex(block_number),
            {  'tracer': 'callTracer', 'onlyTopCall': 'false' }])

    blockTransactions = blockResponse.get('result')
    
    if not blockTransactions:
        print("No transaction traces found in the block.")
        return

    for transaction in blockTransactions:
        txHash = transaction.get('txHash')
        process_tx(transaction, txHash)
        
    print(f"Completed scanning for Tornado Cash transfers in {block_number} block.")
    
    if not foundSuspiciousTx:
        print("No Tornado Cash transfer detected.")

if __name__ == "__main__":
    block_number = get_block_number()

    if w3.is_connected():
        print(f"Connected to Ethereum node. Scanning block {block_number}..")
        detect_tornado_cash_transfers_in_block(block_number)
    else:
        print("Failed to connect to Ethereum node.")

