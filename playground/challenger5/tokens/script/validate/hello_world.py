# install_wasm.py

from stellar_sdk import Keypair, Network, SorobanServer, TransactionBuilder, scval
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban_rpc import GetTransactionStatus
from itertools import cycle


# Set up sender account and servers
PRIVATE_KEY = "SDLXNGAV34DZJMUO3MZMDQLUWQPFY6J3JVVG77T2G7VA3HJYETBEBVZO"
CONTRACT_ID = input("👉 ENTER CONTRACT ID: ")
sender_keypair = Keypair.from_secret(PRIVATE_KEY)
soroban_server = SorobanServer(server_url="http://localhost:8000/soroban/rpc")
sender_account = soroban_server.load_account(sender_keypair.public_key)
tx = (
    TransactionBuilder(sender_account, Network.STANDALONE_NETWORK_PASSPHRASE, 100)
    .set_timeout(300)
    .append_invoke_contract_function_op(
        contract_id=CONTRACT_ID,
        function_name="hello",
        parameters=[scval.to_symbol("Lucas")],
    )
    .build()
)

tx = soroban_server.prepare_transaction(tx)
tx.sign(sender_keypair)
try:
    response = soroban_server.send_transaction(tx)
    print("✅ Transação enviada com sucesso!")
except Exception as e:
    raise Exception("🚨 Erro ao enviar a transação:") from e

# Wait for transaction confirmation
tx_hash = response.hash

clocks = cycle(["|", "/", "-", "\\", "|", "/", "-", "\\"])
while True:
    print(f"\r⏰ Esperando transação confirmar {next(clocks)}", end="")

    get_transaction_data = soroban_server.get_transaction(tx_hash)
    if get_transaction_data.status != GetTransactionStatus.NOT_FOUND:
        break

print("\n✅ Transação confirmada!")
if get_transaction_data.status != GetTransactionStatus.SUCCESS:
    # The transaction failed, so we can extract the `result_xdr`
    print(f"Transaction failed: {get_transaction_data.result_xdr}")
    raise Exception("Transaction failed")

# The transaction was successful, so we can extract the `result_meta_xdr`
transaction_meta = stellar_xdr.TransactionMeta.from_xdr(
    get_transaction_data.result_meta_xdr
)
result = transaction_meta.v3.soroban_meta.return_value

print(f"🎁 Resultado: {scval.to_native(result)}")
