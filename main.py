# log these: transaction hash & funded address & value of sent ether
# testable blocks: 20031962, 17475649, 20877171, 19226185

import os
from typing import Optional
from dotenv import load_dotenv
from web3 import Web3
from json_types import InnerTransaction, Transaction, TraceBlockResponse


load_dotenv()

def get_env(env_var: str) -> str:
    value: Optional[str] = os.getenv(env_var)
    if value is None:
        raise KeyError(f'Environment variable {env_var} is not set.')
    return value

try:
    rpc_url: str = get_env('RPC_URL')
    tornado_cash_address: str = get_env('TORNADO_CASH_ADDRESS')
    print(f'RPC URL: {rpc_url}')
    print(f'Investigated Tornado Cash Address: {tornado_cash_address}')
    print('-' * 70)
except KeyError as e:
    print(f'Error: {e}')
    exit(1)

w3: Web3 = Web3(Web3.HTTPProvider(rpc_url))
suspiciousTxCount: int = 0
overallEthValue: float = 0.0


def get_block_number() -> int:
    while True:
        try:
            block_number: int = int(input('Enter the Ethereum block number: '))
            return block_number
        except ValueError:
            print('Invalid input. Please enter a valid integer for the block number.')

def process_tx(transaction: Transaction, txHash: str, top_level: bool = True) -> None:
    calls: list[InnerTransaction] = transaction.get('result').get('calls') if top_level else transaction.get('calls')
    if calls and len(calls) > 0:
        for child_tx in calls:
            if child_tx.get('from').lower() == tornado_cash_address.lower():
                global suspiciousTxCount
                suspiciousTxCount += 1
                currentEthValue = w3.from_wei(int(child_tx.get('value'), 0), 'ether')
                global overallEthValue
                overallEthValue += float(currentEthValue)
                print('Tornado Cash transaction detected:')
                print(f' - Transaction Hash: {txHash}')
                print(f' - From: {child_tx.get('from')}')
                print(f' - To: {child_tx.get('to')}')
                print(f' - Value: {currentEthValue} ETH')
                print('-' * 70)
            process_tx(child_tx, txHash, False)

def process_block(block_number: int) -> None:
    try:
        blockResponse: TraceBlockResponse = w3.provider.make_request('debug_traceBlockByNumber', [hex(block_number),
                {  'tracer': 'callTracer', 'onlyTopCall': 'false' }])
    except Exception as e:
        print(f'Error in make_request debug_traceBlockByNumber: {e}')
        return

    blockTransactions: list[Transaction] = blockResponse.get('result')
    
    if not blockTransactions:
        print('No transaction traces found in the block.')
        return

    for transaction in blockTransactions:
        txHash: str = transaction.get('txHash')
        process_tx(transaction, txHash)
        
    print(f'Completed scanning for Tornado Cash transfers in block #{block_number}.')
    
    if suspiciousTxCount == 0:
        print('No Tornado Cash transfer detected.')
    else:
        print(f'Detected {suspiciousTxCount} Tornado Cash transfers in block #{block_number}.')
        print(f'Total value of suspicious transactions: {overallEthValue} ETH')

if __name__ == '__main__':
    block_number: int = get_block_number()

    if w3.is_connected():
        print(f'Connected to Ethereum node. Scanning block {block_number}..')
        process_block(block_number)
    else:
        print('Failed to connect to Ethereum node.')

