import asyncio

from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.contract import AsyncContract
from web3.exceptions import TransactionNotFound
from termcolor import cprint



class Client:
    def __init__(self, private_key, proxy, chain_name, chain_id, explorer_url,rpc_url):
        self.private_key = private_key

        request_kwargs = {'proxy': f'http://{proxy}'}
        rpc_url = rpc_url

        self.chain_name = chain_name
        self.chain_token = 'ETH'
        self.chain_id = chain_id
        self.proxy = proxy
        self.eip_1559 = True
        self.explorer_url = explorer_url
        self.w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url, request_kwargs=request_kwargs))
        self.address = self.w3.to_checksum_address(self.w3.eth.account.from_key(self.private_key).address)



    def get_contract(self, contract_address: str, abi: dict) -> AsyncContract:
        return self.w3.eth.contract(
            address=AsyncWeb3.to_checksum_address(contract_address),
            abi=abi
        )

    def eth_balance(self):

        return self.w3.eth.get_balance(self.address)


    async def get_priotiry_fee(self) -> int:
        fee_history = await self.w3.eth.fee_history(5, 'latest', [80.0])
        non_empty_block_priority_fees = [fee[0] for fee in fee_history["reward"] if fee[0] != 0]

        divisor_priority = max(len(non_empty_block_priority_fees), 1)
        priority_fee = int(round(sum(non_empty_block_priority_fees) / divisor_priority))

        return priority_fee

    async def to_checksum_address(self, data):
        a = self.w3.to_checksum_address(data)
        return a



    async def prepare_tx(self, value: int | float = 0):
        transaction = {
            'chainId': await self.w3.eth.chain_id,
            'nonce': await self.w3.eth.get_transaction_count(self.address),
            'from': self.address,
            'value': value,
            'gasPrice': int((await self.w3.eth.gas_price) * 1.8),
        }

        if self.eip_1559:
            del transaction['gasPrice']

            base_fee = int(await self.w3.eth.gas_price * 1.8)
            max_priority_fee_per_gas = await self.get_priotiry_fee()

            if max_priority_fee_per_gas == 0:
                max_priority_fee_per_gas = base_fee

            max_fee_per_gas = int(base_fee * 1.2 + max_priority_fee_per_gas)

            transaction['maxPriorityFeePerGas'] = max_priority_fee_per_gas
            transaction['maxFeePerGas'] = max_fee_per_gas
            transaction['type'] = '0x2'

        return transaction

    async def send_transaction(
            self, transaction=None, without_gas: bool = False, need_hash: bool = False, ready_tx: bytes = None
    ):
        if ready_tx:
            tx_hash_bytes = await self.w3.eth.send_raw_transaction(ready_tx)

            cprint('Successfully sent transaction!', 'light_green')

            tx_hash_hex = self.w3.to_hex(tx_hash_bytes)
        else:

            if not without_gas:
                transaction['gas'] = int((await self.w3.eth.estimate_gas(transaction)) * 1.5)

            signed_raw_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key).rawTransaction

            cprint('Successfully signed transaction!', 'light_green')

            tx_hash_bytes = await self.w3.eth.send_raw_transaction(signed_raw_tx)

            cprint('Successfully sent transaction!', 'light_green')

            tx_hash_hex = self.w3.to_hex(tx_hash_bytes)

        if need_hash:
            await self.wait_tx(tx_hash_hex)
            return tx_hash_hex

        return await self.wait_tx(tx_hash_hex)

    async def wait_tx(self, tx_hash):
        total_time = 0
        timeout = 120
        poll_latency = 10
        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(tx_hash)
                status = receipts.get("status")
                if status == 1:
                    cprint(f'Transaction was successful: {self.explorer_url}tx/{tx_hash}', 'light_green')
                    return True
                elif status is None:
                    await asyncio.sleep(poll_latency)
                else:
                    cprint(f'Transaction failed: {self.explorer_url}tx/{tx_hash}', 'light_red')
                    return False
            except TransactionNotFound:
                if total_time > timeout:
                    cprint(f"Transaction is not in the chain after {timeout} seconds", 'light_yellow')
                    return False
                total_time += poll_latency
                await asyncio.sleep(poll_latency)
