import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter
from stellar_sdk import Keypair, Network, SorobanServer, TransactionBuilder, scval
import pandas as pd
from stellar_sdk import Server

# Inicialize o servidor Horizon para cada rede
horizon_server = Server("https://horizon.stellar.org")
soroban_server = SorobanServer(server_url=" https://mainnet.sorobanrpc.com")

# Set up sender account and servers
PRIVATE_KEY = "SBLZT47GQECQMONNSXYETP2FX7KM4CW63WCEGQUAEYOJ5NIYCEKCJ7KU"
sender_keypair = Keypair.from_secret(PRIVATE_KEY)
sender_account = soroban_server.load_account(sender_keypair.public_key)


df = pd.read_csv("./dev30k-04.csv")

df.head()
df = df.rename(
    columns={
        "Carimbo de data/hora": "submission_datetime",
        "Qual sua Chave Pública?": "account_id",
        "ID do Contrato": "contract_id",
        "Hash do Deploy do Contrato": "deploy_tx_hash",
    }
)


########

# @title Get deploy datetime


# Função para buscar o timestamp de criação do contrato e o tipo de operação
def get_operation_details(transaction_hash, account_id):
    ops = {}
    try:
        # Obtenha todas as operações associadas à transação
        ops = (
            horizon_server.operations()
            .for_transaction(transaction_hash)
            .call()["_embedded"]["records"]
        )
    except Exception as e:
        print(f"🚨 Error fetching operation details for {transaction_hash}: {str(e)}")
        return None, None
    for op in ops:
        # Verifique se a operação é feita pela account_id
        is_correct_account = account_id == op.get("source_account", False)
        if is_correct_account:
            # Retorne o timestamp e o tipo de operação
            return op["created_at"], op.get("type", "Unknown")
    print(
        f"⚠️ No matching operation found for {transaction_hash} and account {account_id}"
    )
    return None, None


# Função para processar cada DataFrame (mainnet e testnet)
def process_deploy_details(df):
    deploy_timestamps = []
    operation_types = []

    for _, row in df.iterrows():
        timestamp, op_type = get_operation_details(
            row["deploy_tx_hash"], row["account_id"]
        )
        deploy_timestamps.append(timestamp)
        operation_types.append(op_type)

    # Adiciona as colunas ao DataFrame
    df["deploy_timestamp"] = pd.to_datetime(deploy_timestamps)
    df["op_type"] = operation_types
    return df


# Processar os DataFrames mainnet e testnet
df = process_deploy_details(df)
df = df[df["op_type"] == "invoke_host_function"]

#########


# Função para simular chamadas de contrato
def simulate_function(contract_id, function_name, args):
    tx = (
        TransactionBuilder(sender_account, Network.PUBLIC_NETWORK_PASSPHRASE)
        .set_timeout(300)
        .append_invoke_contract_function_op(
            contract_id=contract_id,
            function_name=function_name,
            parameters=args,
        )
        .build()
    )
    # Simular para obter custos
    simulation = soroban_server.simulate_transaction(tx)

    if simulation.error:
        print(f"🚨 Simulation Error:", simulation.error)

    # Acessar informações de custo
    return simulation.min_resource_fee


# Configurações do contrato
functions = [
    ("get_admin", []),
    ("initialize", [scval.to_address(sender_keypair.public_key)]),
    ("mint", [scval.to_address(sender_keypair.public_key), scval.to_int128(1000)]),
    ("set_admin", [scval.to_address(sender_keypair.public_key)]),
    (
        "allowance",
        [
            scval.to_address(sender_keypair.public_key),
            scval.to_address(sender_keypair.public_key),
        ],
    ),
    (
        "approve",
        [
            scval.to_address(sender_keypair.public_key),
            scval.to_address(sender_keypair.public_key),
            scval.to_int128(1000),
            scval.to_uint32(123456),
        ],
    ),
    ("balance", [scval.to_address(sender_keypair.public_key)]),
    (
        "transfer",
        [
            scval.to_address(sender_keypair.public_key),
            scval.to_address(sender_keypair.public_key),
            scval.to_int128(500),
        ],
    ),
    (
        "transfer_from",
        [
            scval.to_address(sender_keypair.public_key),
            scval.to_address(sender_keypair.public_key),
            scval.to_address(sender_keypair.public_key),
            scval.to_int128(500),
        ],
    ),
    ("decimals", []),
    ("name", []),
    ("symbol", []),
]

# Simulação de chamadas e coleta de custos
costs = {}
progress_counter = 0
total_operations = len(functions) * len(df.contract_id)
for func_name, args in functions:
    for contract_id in df["contract_id"]:
        progress_counter += 1
        print(f"\rProgress: {progress_counter}/{total_operations}", end="")
        try:
            cost = simulate_function(contract_id, func_name, args)
            costs[func_name] = cost
        except Exception as e:
            print(f"FUNC: {func_name}, ARGS: {args}", e)
            costs[func_name] = f"Erro: {e}"

# Visualização dos resultados
write_ops = [
    "mint",
    "set_admin",
    "approve",
    "transfer",
    "transfer_from",
]
read_ops = ["get_admin", "allowance", "balance", "decimals", "name", "symbol"]

write_costs = [costs[func] for func in write_ops if isinstance(costs[func], int)]
read_costs = [costs[func] for func in read_ops if isinstance(costs[func], int)]

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.boxplot(data=write_costs)
plt.title("WRITE OP: Boxplot")
plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))

plt.subplot(1, 2, 2)
sns.boxplot(data=read_costs)
plt.title("READ OP: Boxplot")
plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))

plt.tight_layout()
plt.show()
