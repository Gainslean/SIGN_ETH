import json


chain_name = {
    'Arbitrum': "Arbitrum",
    'Optimism': "Optimism",
    'Base': "Base",
    'Polygon': "Polygon",
    'Ethereum': "Ethereum",
    'Avalance': "Avalance",
    'Zora': "Zora",
    'Abstract': "Abstract"
}

rpc_url = {
    'Arbitrum': "https://rpc.ankr.com/arbitrum",
    'Optimism': "https://rpc.ankr.com/optimism",
    'Base': "https://rpc.ankr.com/base",
    'Polygon': "https://rpc.ankr.com/polygon",
    'Ethereum': "https://rpc.ankr.com/eth",
    'Avalance': "https://rpc.ankr.com/avalanche",
    'Abstract': "https://api.mainnet.abs.xyz",
    'Zora': "wss://zora.drpc.org"
}

explorer_url = {
    'Arbitrum': "https://arbiscan.io/",
    'Optimism': "https://optimistic.etherscan.io/",
    'Base': "https://basescan.org/",
    'Polygon': "https://polygonscan.com/",
    'Ethereum': "https://etherscan.io/",
    'Avalance': "https://www.oklink.com/ru/avax/",
    'Abstract': "https://abscan.org/",
    'Zora': "https://zora.drpc.org"
}

Chain_id = {
    'Ethereum': 1,
    'Optimism': 10,
    'Arbitrum': 42161,
    'Base': 8453,
    'Polygon': 137,
    'Linea': 59144,
    'Blast': 81457,
    'Avalance': 43114,
    'Abstract': 2741,
    'Zora': 7777777
    }

sign_contract = {
    'Ethereum': "0x3D8E699Db14d7781557fE94ad99d93Be180A6594",
    'Arbitrum': "0x4e4af2a21ebf62850fD99Eb6253E1eFBb56098cD",
    'Base': "0x2b3224D080452276a76690341e5Cfa81A945a985",
    'Polygon': "0xe2C15B97F628B7Ad279D6b002cEDd414390b6D63"
    }
with open("sign.json") as file:
    SIGN_ABI = json.load(file)


