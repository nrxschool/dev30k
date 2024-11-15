"""
Cria uma ordem de venda TOKENS
"""

from stellar_sdk import Keypair, Network, Server, TransactionBuilder, Asset

# Configurações iniciais
ALICE_PRIVATE_KEY = "SDLXNGAV34DZJMUO3MZMDQLUWQPFY6J3JVVG77T2G7VA3HJYETBEBVZO"
# CONTRACT_ID = input("👉 Enter contract id: ")
alice_keypair = Keypair.from_secret(ALICE_PRIVATE_KEY)
horizon_server = Server("http://localhost:8000")
alice_account = horizon_server.load_account(alice_keypair.public_key)

# Configura o token e XLM como os ativos de venda e compra
token_asset = Asset("NRX", alice_keypair.public_key)
native_asset = Asset.native()

order = {
    "selling": token_asset,
    "buying": native_asset,
    "amount": 1000,
    "price": 1,
    "source": alice_keypair.public_key,
}

transaction_args = {
    "source_account": alice_account,
    "network_passphrase": Network.STANDALONE_NETWORK_PASSPHRASE,
    "base_fee": 100,
}

sell_order_transaction = (
    TransactionBuilder(**transaction_args)
    .append_manage_sell_offer_op(**order)
    .set_timeout(30)
    .build()
)

sell_order_transaction.sign(alice_keypair)
response = horizon_server.submit_transaction(sell_order_transaction)
print("✅ Ordem de venda criada com sucesso!", response["hash"])

import balances
