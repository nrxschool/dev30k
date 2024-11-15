from itertools import cycle
from stellar_sdk import Keypair, Network, SorobanServer, TransactionBuilder, scval, xdr
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus
from stellar_sdk.exceptions import PrepareTransactionException


# Set up sender account and servers
PRIVATE_KEY = "SDLXNGAV34DZJMUO3MZMDQLUWQPFY6J3JVVG77T2G7VA3HJYETBEBVZO"
CONTRACT_ID = input("👉 Enter contract id: ")
sender_keypair = Keypair.from_secret(PRIVATE_KEY)
soroban_server = SorobanServer(server_url="http://localhost:8000/soroban/rpc")


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


def test_name(name):
    try:
        result = invoke_contract_function("name", [])
        assert result == name, f"❌ Erro: name() retornou {result}, esperado {name}"
    except AssertionError as e:
        print(f"🚨 Erro: {e}")
    else:
        print(f"✅ Sucesso: name() retornou {result}")


def test_symbol(symbol):
    try:
        result = invoke_contract_function("symbol", [])
        assert (
            result == symbol
        ), f"❌ Erro: symbol() retornou {result}, esperado {symbol}"
    except AssertionError as e:
        print(f"🚨 Erro: {e}")
    else:
        print(f"✅ Sucesso: symbol() retornou {result}")


def test_decimals(decimals):
    try:
        result = invoke_contract_function("decimals", [])
        assert (
            result == decimals
        ), f"❌ Erro: decimals() retornou {result}, esperado {decimals}"
    except AssertionError as e:
        print(f"🚨 Erro: {e}")
    else:
        print(f"✅ Sucesso: decimals() retornou {result}")


def test_initialize(admin_key):
    try:
        result = invoke_contract_function("initialize", [scval.to_address(admin_key)])
        assert result, "❌ Erro: initialize() retornou None, esperado True"
    except AssertionError as e:
        print(f"🚨 Erro: {e}")
    else:
        print("✅ Sucesso: initialize() foi chamado com sucesso")


def test_get_admin(admin_key):
    try:
        result = invoke_contract_function("get_admin", [])
        assert (
            result is not None
        ), f"❌ Erro: get_admin() retornou None, esperado {sender_keypair.public_key}"
        assert (
            result.address == admin_key
        ), f"❌ Erro: get_admin() retornou {result.address}, esperado {sender_keypair.public_key}"
    except AssertionError as e:
        print(f"🚨 Erro: {e}")
    else:
        print("✅ Sucesso: get_admin() retornou", result.address)


def test_balance_admin(admin_key, amount):
    try:
        result = invoke_contract_function("balance", [scval.to_address(admin_key)])
        assert (
            result == amount
        ), f"❌ Erro: balance() retornou {result}, esperado {amount}"
    except AssertionError as e:
        print(f"🚨 Erro: {e}")
    else:
        print("✅ Sucesso: balance() retornou", result / 1e18)


test_initialize(sender_keypair.public_key)
test_get_admin(sender_keypair.public_key)
test_balance_admin(sender_keypair.public_key, 1000 * 1e18)
test_name("NRX Token")
test_symbol("NRX")
test_decimals(18)
