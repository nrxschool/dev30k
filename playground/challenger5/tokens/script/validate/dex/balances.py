from itertools import cycle
from stellar_sdk import Keypair, Network, SorobanServer, TransactionBuilder, scval, xdr, Server
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus
from stellar_sdk.exceptions import PrepareTransactionException


BOB_PRIVATE_KEY = "SCXMBN6TNHYFN724ASTOVTTQTTHVDE72766SKNXZTHADRPP6D4AR5TWC"
ALICE_PRIVATE_KEY = "SDLXNGAV34DZJMUO3MZMDQLUWQPFY6J3JVVG77T2G7VA3HJYETBEBVZO"
CONTRACT_ID = "CD56PJPZLRPCUU4XREF52DZI25TEQCBCGYEWZXCUEQHCOGXLDJ4YICNS"

# Set up sender account and servers
soroban_server = SorobanServer(server_url="http://localhost:8000/soroban/rpc")
horizon_server = Server(horizon_url="http://localhost:8000")
sender_keypair = Keypair.from_secret(ALICE_PRIVATE_KEY)

def invoke_contract_function(function_name, params):
    """
    Assíncrono: Invoca uma função do contrato e retorna o resultado.
    """
    sender_account = soroban_server.load_account(sender_keypair.public_key)

    tx = (
        TransactionBuilder(sender_account, Network.STANDALONE_NETWORK_PASSPHRASE, 100)
        .set_timeout(300)
        .append_invoke_contract_function_op(
            contract_id=CONTRACT_ID,
            function_name=function_name,
            parameters=params,
        )
        .build()
    )

    # Prepara e assina a transação
    try:
        tx = soroban_server.prepare_transaction(tx)
    except PrepareTransactionException as e:
        print(
            "🚨 Erro antes de enviar a transação",
            "👇" * 30,
            e.simulate_transaction_response.error,
            sep="\n",
        )
        return None

    tx.sign(sender_keypair)

    # Envia a transação
    try:
        response = soroban_server.send_transaction(tx)
    except Exception as e:
        print("🚨 Erro ao enviar a transação:", e)
        return None
    if response.status == SendTransactionStatus.ERROR:
        print("🚨 Erro ao enviar a transação:", response)
        return None

    # Hash da transação para confirmar o status
    tx_hash = response.hash
    # Animação de espera e verificação de status da transação
    clocks = cycle(["|", "/", "-", "\\", "|", "/", "-", "\\"])
    while True:
        print(f"\r⏰ Esperando transação confirmar {next(clocks)}", end="")
        get_transaction_data = soroban_server.get_transaction(tx_hash)
        if get_transaction_data.status != GetTransactionStatus.NOT_FOUND:
            break

    # Limpa a linha de animação após confirmação
    print("\r" + " " * 50, end="\r")

    # Verifica o status final da transação
    if get_transaction_data.status != GetTransactionStatus.SUCCESS:
        print(f"🚨 Transação falhou: {get_transaction_data.result_xdr}")
        return None

    # Extrai e retorna o resultado
    transaction_meta = xdr.TransactionMeta.from_xdr(
        get_transaction_data.result_meta_xdr
    )
    return scval.to_native(transaction_meta.v3.soroban_meta.return_value)


bob_keypair = Keypair.from_secret(BOB_PRIVATE_KEY)
print(f"✅ Conta do BOB : [{bob_keypair.public_key}]")
print("🔄 Saldo da Conta do BOB:")
account = horizon_server.accounts().account_id(bob_keypair.public_key).call()
balances = account["balances"]
for balance in balances:
    if balance["asset_type"] == "native":
        asset = balance["asset_type"]
    else:
        asset = balance["asset_code"]
    balance_amount = balance["balance"]
    print(f"   - Ativo: {asset}, Saldo: {balance_amount}")
token_balance = invoke_contract_function(
    "balance", [scval.to_address(bob_keypair.public_key)]
)
print(f"   - Ativo: NRX Token, Saldo: {token_balance/1e18}")


alice_keypair = Keypair.from_secret(ALICE_PRIVATE_KEY)
print(f"\n✅ Conta do ALICE criada com sucesso: [{alice_keypair.public_key}]")
print("🔄 Saldo da Conta do ALICE:")
account = horizon_server.accounts().account_id(alice_keypair.public_key).call()
balances = account["balances"]
for balance in balances:
    if balance["asset_type"] == "native":
        asset = balance["asset_type"]
    else:
        asset = balance["asset_code"]
    balance_amount = balance["balance"]
    print(f"   - Ativo: {asset}, Saldo: {balance_amount}")
token_balance = invoke_contract_function(
    "balance", [scval.to_address(alice_keypair.public_key)]
)
print(f"   - Ativo: NRX Token, Saldo: {token_balance/1e18}")
