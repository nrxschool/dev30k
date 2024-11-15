# install_wasm.py

from itertools import cycle
from threading import Thread

from stellar_sdk.xdr import TransactionMeta
from stellar_sdk.soroban_rpc import GetTransactionStatus
from stellar_sdk.exceptions import NotFoundError, PrepareTransactionException
from stellar_sdk import Keypair, Network, SorobanServer, Server, TransactionBuilder
from requests import get, RequestException


def create_account(public_key, server: Server):
    """Create a new account using Friendbot and retrieve account balance."""
    url = "http://localhost:8000/friendbot"
    params = {"addr": public_key}
    timeout = 30

    def loading_animation():
        clocks = cycle(["|", "/", "-", "\\", "|", "/", "-", "\\"])
        while LOADING:
            print(f"\r⏰ Criando a conta {next(clocks)}", end="")
        print()

    # Inicia a animação em uma thread separada
    LOADING = True
    loading_thread = Thread(target=loading_animation)
    loading_thread.daemon = True
    loading_thread.start()

    try:
        r = get(url, params=params, timeout=timeout)
        r.raise_for_status()
    except RequestException as e:
        raise ValueError(f"Erro ao obter fundos do Friendbot: {str(e)}") from e

    LOADING = False
    loading_thread.join()  # Wait for the thread to finish

    # Fetch account details and display balance
    account = server.accounts().account_id(public_key).call()
    balances = account["balances"]
    print(f"✅ Conta criada com sucesso: {public_key}")
    print("🔄 Saldo da Conta:")
    for balance in balances:
        asset_type = balance["asset_type"]
        balance_amount = balance["balance"]
        print(f"   - Tipo de Ativo: {asset_type}, Saldo: {balance_amount}")

    return account


def validate_account(public_key, server: Server):
    """Check if account exists; if not, create it."""
    try:
        return server.load_account(public_key)
    except NotFoundError:
        print("🚫 A conta de destino não existe!")
        print("🔧 Criando a conta...")
        create_account(public_key, server)
        return server.load_account(public_key)


# Set up sender account and servers
PRIVATE_KEY = "SDLXNGAV34DZJMUO3MZMDQLUWQPFY6J3JVVG77T2G7VA3HJYETBEBVZO"
CONTRACT_NAME = input("👉 ENTER CONTRACT NAME: ")
sender_keypair = Keypair.from_secret(PRIVATE_KEY)
soroban_server = SorobanServer(server_url="http://localhost:8000/soroban/rpc")
horizon_server = Server(horizon_url="http://localhost:8000")
sender_account = validate_account(sender_keypair.public_key, horizon_server)


# Load contract binary
with open(f"target/wasm32-unknown-unknown/release/{CONTRACT_NAME}.wasm", "rb") as f:
    contract_bin = f.read()

# Build transaction to upload the contract
tx = (
    TransactionBuilder(
        source_account=sender_account,
        network_passphrase=Network.STANDALONE_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .set_timeout(300)
    .append_upload_contract_wasm_op(
        contract=contract_bin,
    )
    .build()
)

# Prepare the transaction
try:
    tx = soroban_server.prepare_transaction(tx)
    print("🆗 Transação pronta pra ser enviada!")
except PrepareTransactionException as e:
    print(f"🚨 Erro ao preparar a transação: {e.simulate_transaction_response}")
    raise e

# Sign the transaction
tx.sign(sender_keypair)

# Send the transaction
try:
    response = soroban_server.send_transaction(tx)
    print("✅ Transação enviada com sucesso!")
    print(f"🔐 Conta da Transação: {sender_keypair.public_key}")
    print(f"🔗 Hash da Transação: {response.hash}")
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

# Retrieve WASM ID if the transaction was successful
if get_transaction_data.status == GetTransactionStatus.SUCCESS:
    transaction_meta = TransactionMeta.from_xdr(get_transaction_data.result_meta_xdr)
    wasm_id = transaction_meta.v3.soroban_meta.return_value.bytes.sc_bytes.hex()
    print(f"🆔 Wasm id: {wasm_id}")
else:
    print(f"🚨 Transação falhou: {get_transaction_data.result_xdr}")
