import asyncio
import random

from client import Client
from config import SIGN_ABI, Chain_id, chain_name, rpc_url, explorer_url, sign_contract

# СКРИПТ ПОДДЕРЖИВАЕТ "Arbitrum", "Base", "Polygon", "Ethereum"

chein = "Base" # Сеть в которой будет отправка сообщения, поддерживается  "Arbitrum", "Optimism", "Base"

random_scain = False #  Если True, то будет выбирать рандомную сеть для сигна, на всю пачку счетов.  False если сами хотите указать сеть(пункт выше)

chein_list = ["Arbitrum", "Base", "Polygon", "Ethereum"] # Сюда нужно указать сети, которые будут рандомно выбираться, при  random_scain = True  "Arbitrum", "Base", "Polygon", "Ethereum"


from_time = 30 # Задержка перед началом страта следующего кошелька, в секундах. from_time это минимальное время. Если хотите проще, то 15*60 это 15 минут задержки.
to_time = 60 #  to_time это максимальное время задержки


class Sign:
    def __init__(self, client: Client):
        self.client = client
        self.contract = self.client.get_contract(
            contract_address=sign_contract[self.client.chain_name],
            abi=SIGN_ABI
        )

    async def randimazer(self):

        i = random.randint(1, 6)

        with open('word.txt', 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file if line.strip()]


        if i == 1:
            info = random.choice(words)
            return info
        if i == 2:
            info = str(random.randint(1,999999999))
            return info
        if i == 3:
            hislo = str(random.randint(1,999999999))
            slovo = random.choice(words)
            info = hislo+slovo
            return info
        if i == 4:
            hislo = str(random.randint(1,999999999))
            slovo = random.choice(words)
            info = slovo+hislo
            return info
        if i == 5:
            info = random.choice(words)+random.choice(words)
            return info
        if i == 6:
            info = random.choice(words)+random.choice(words)+random.choice(words)
            return info

    async def signature(self):

        balance = await self.client.eth_balance()
        gas = int((await self.client.w3.eth.gas_price) * 6)
        if balance - gas <= 0:
            print(f"Недостаточно ЕТН для сигна на кошельке {self.client.address}")
            print()

        else:
            try:
                name = await self.randimazer()
                tx = await self.contract.functions.register([
                    self.client.address,  # address
                    False,  # bool
                    0,  # uint8 (should be 0-255)
                    0,  # uint64
                    "0x0000000000000000000000000000000000000000",  # address
                    0,  # uint64
                    f"{{\"name\":\"{name}\",\"description\":\"{await self.randimazer()}\",\"data\":[{{\"name\":\"{await self.randimazer()}\",\"type\":\"string\"}}]}}"
                    ],
                    b''
                    # string
                ).build_transaction(await self.client.prepare_tx())
                # Отправляем транзакцию
                print(f"Начинаю работу с кошельком в {self.client.address} в сети {self.client.chain_name} , название сигна = {name}")
                print()
                tx_hash = await self.client.send_transaction(tx, need_hash=True)
                print(f"Транзакция успешно отправлена: {tx_hash}")
                print()
            except Exception as e:
                print(f"Ошибка при отправке транзакции: {e}")
                try:
                    print("Делаю еще одну попытку сигна")
                    print()
                    await asyncio.sleep(2)
                    await self.signature()
                except Exception as e:
                    print(f"Ошибка при отправке транзакции: {e}")
                    print(f"Кошелек {self.client.address} дефектный, скипаю его")

    async def main(self):

        await self.signature()

        time = random.randint(from_time, to_time)
        print(f"Ожидаю {time} секунд перед запуском следующего кошелька")
        print()
        await asyncio.sleep(time)





async def main():
    with open("private_keys.txt", 'r') as f:
        kohi = [line.strip() for line in f.readlines()]

    for private_key in kohi:
        if random_scain:
            chain_name = random.choice(chein_list)
        else:
            chain_name = chein


        proxy = ''
        rpc_url_selected = rpc_url[chain_name]
        chain_id = Chain_id[chain_name]
        explorer_url_selected = explorer_url[chain_name]


        w3_client = Client(
            private_key=private_key,
            proxy=proxy,
            chain_name=chain_name,
            chain_id=chain_id,
            explorer_url=explorer_url_selected,
            rpc_url=rpc_url_selected,
        )

        swap_client = Sign(client=w3_client)
        await swap_client.main()

asyncio.run(main())
