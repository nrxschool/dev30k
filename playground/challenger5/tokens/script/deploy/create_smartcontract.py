from itertools import cycle
import time
from requests import RequestException, get
from stellar_sdk.xdr import TransactionMeta
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus
from stellar_sdk.exceptions import NotFoundError, PrepareTransactionException
from stellar_sdk import (
    Keypair,
    Network,
    SorobanServer,
    Server,
    TransactionBuilder,
    StrKey,
)

# Solicita o hash do WASM do usuário
wasm_id = input("👉 Insira o Hash do Wasm (ID do Wasm): ")
secret = "SDLXNGAV34DZJMUO3MZMDQLUWQPFY6J3JVVG77T2G7VA3HJYETBEBVZO"


def create_account(public_key, server: Server):
    """Create a new account using Friendbot and retrieve account balance."""
    url = "http://localhost:8000/friendbot"
    params = {"addr": public_key}
    timeout = 30
    try:
        r = get(url, params=params, timeout=timeout)
        r.raise_for_status()
    except RequestException as e:
        raise ValueError(f"Erro ao obter fundos do Friendbot: {str(e)}") from e

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
sender_keypair = Keypair.from_secret(secret)
soroban_server = SorobanServer(server_url="http://localhost:8000/soroban/rpc")
horizon_server = Server(horizon_url="http://localhost:8000")
sender_account = validate_account(sender_keypair.public_key, horizon_server)


# Build transaction to create the contract using the WASM ID
tx_create_contract = (
    TransactionBuilder(
        source_account=sender_account,
        network_passphrase=Network.STANDALONE_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .set_timeout(300)
    .append_create_contract_op(wasm_id=wasm_id, address=sender_keypair.public_key)
    .build()
)


try:
    tx_create_contract = soroban_server.prepare_transaction(tx_create_contract)
except PrepareTransactionException as e:
    print(
        f"🚨 Erro ao preparar a transação de criação do contrato: {e.simulate_transaction_response}"
    )
    raise
print("🆗 Transação para criação do contrato pronta para ser enviada!")


tx_create_contract.sign(sender_keypair)

try:
    send_transaction_data = soroban_server.send_transaction(tx_create_contract)
except Exception as e:
    raise Exception("🚨 Erro ao enviar a transação para criação do contrato") from e

if send_transaction_data.status != SendTransactionStatus.PENDING:
    raise Exception(
        "🚨 Falha ao enviar a transação para criação do contrato", send_transaction_data
    )
print("✅ Transação para criação do contrato enviada com sucesso!")


clocks = cycle(["|", "/", "-", "\\", "|", "/", "-", "\\"])
while True:
    print(f"\r⏰ Esperando transação confirmar{next(clocks)}", end="")

    get_transaction_data = soroban_server.get_transaction(send_transaction_data.hash)
    if get_transaction_data.status != GetTransactionStatus.NOT_FOUND:
        break
    time.sleep(0.1)

print("\n✅ Transação confirmada!")

# Check if contract creation transaction succeeded and retrieve the contract ID
if get_transaction_data.status != GetTransactionStatus.SUCCESS:
    raise Exception(
        f"🚨 Transação para criação do contrato falhou: {get_transaction_data}"
    )

transaction_meta = TransactionMeta.from_xdr(get_transaction_data.result_meta_xdr)
result = transaction_meta.v3.soroban_meta.return_value.address.contract_id.hash
contract_id = StrKey.encode_contract(result)
print(f"🆔 Endereço do contrato criado: {contract_id}")
