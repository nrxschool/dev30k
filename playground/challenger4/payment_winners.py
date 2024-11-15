from stellar_sdk.exceptions import NotFoundError
from stellar_sdk import Asset
from stellar_sdk import Keypair, Network, TransactionBuilder, Server
from requests import get, RequestException


PRV_KEY = ""
root_keypair = Keypair.from_secret(PRV_KEY)
server = Server(horizon_url="https://horizon.stellar.org")
nearx_account = server.load_account(root_keypair.public_key)


def read_public_keys():
    with open("public_keys1.txt", "r") as file:
        public_keys = [line.strip() for line in file.readlines()]
    return public_keys


challenger4_ok = [
    ("GAWOSCHY7VK6OR456AEKNSL6PUKJ7GQ4QQASFS5NRCVB3PPFDMOHSSQZ", 600),
    ("GB5UBWORACGMEHWLBN4CQMTOGPALCSOXTQLX4K7HU3SQE4DHKRV7GGD7", 600),
    ("GDXSK5FVZEQ2KMHPMQD4VNQXBS3FLSNAIRE246CBYX5XLDTQJ4B5AEFA", 600),
    ("GBB6IIYOJ3QHN246XTDF2ZZ2Q7JPSOJLKED6IZJD6XBEUNABGKEB6UIB", 600),
    ("GBF7NZHSZYYUTPYVXMAGYODM66M5BYMESE2UYVWY2OAMFHAZKA7BFRNM", 600),
    ("GASBS5FHTGFFMYTYYIITOTX6A4ZG3J55BJGOTSQXCRDTIRRZBA6J63MG", 600),
    ("GD7D2Z6LQ5F7FDLDVCKPSGNXS6REDF3ABPM2ADKIZN4PIBWDKKQH4AS7", 600),
    ("GB5DK65YH6MYYOZ5TXPJSMYTG7Y7544RMLSNS3BLXKJXPZ4S65SEYFU2", 600),
    ("GDEE7QQXP2UU42HLLE4Y3IXNYC6LG674UKK2IUBIFYBOJMT43VMQKSJN", 600),
    ("GAAHX4TUAJPVWFDAEYKLT52ROZMYERWSKM7ZIYKT3JZQ6JJS73HRYHRU", 600),
    ("GA4WYK5DJRMVFYYC7XJQJHTJSWDESEXTTATXCUF2OQZ2Z5UVJJRYQAZU", 600),
    ("GCSL7N3K3HNABE63MSHWZFRHJ2UGN6C7USQ7KEL3KGNX3BPZ4ZHCPRBG", 600),
    ("GANSVIA3OR537VRFFB5S3Y3HA64FMNPJF4YNVLS7LHEBYCLXQ57J3QDS", 600),
    ("GAGL327YR6JV4WUOO6TWRXB3UYWGAAOGGZAUKAJFTJDVJT6A4PASMRMS", 600),
    ("GAGF3B2VOP6L4PUBHTO6EQ5FO7H42YAGJXJC2J42CFH3B6UD456F563T", 600),
    ("GBPTLZBA5AO5LM7LZZBU6G2DBULROCCFBHDQWGUFJ2YBUMBZZ7EYDAJ4", 600),
    ("GBNTK7YLWIKRVUMUEZT62R2ABN4NSKVUYBR3M5CGCPXOEL7JNW5VTDAV", 600),
    ("GCR36L2ZTD2Q2BU4JHVPBKQANRNYD7LSON7ZL2DKQQZYIWLLXOLNNWON", 600),
    ("GADFNPSDVL7XSIYCUDCNI4E47NVEKY7E77BACH2I57NQTQIM2G75KUTP", 600),
    ("GB4E2QRBMJR36SBXGBKYTX3KMTJRGQ6TSUGLDAPCCU5ZHVA6FU7RUXEA", 400),
    ("GAS6QHYBYLNPRHFJG7KPRKA6PBOF54S2DCJAWETJOKBHIR2VPW5SK6CW", 400),
    ("GAFASLN5AWEKSDNXLRUH525N2FSNTBFLFG53EPUEOKRQCWUI2BLT5JES", 385),
    ("GBLZKEQ5NRQEQE5MZNL4UR3MYSVOYQ6QRJJM2HNOABKKGF3CO2LWR24G", 257),
]


def create_account(public_key, server):
    url = "http://localhost:8000/friendbot"
    params = {"addr": public_key}
    timeout = 30
    try:
        r = get(url, params=params, timeout=timeout)
        r.raise_for_status()
    except RequestException as e:
        raise ValueError(f"Error in get faucet: {str(e)}") from e
    account = server.accounts().account_id(root_keypair.public_key).call()
    balances = account["balances"]
    print(f"✅ # Balances for account {root_keypair.public_key}:", end=": ")
    for balance in balances:
        asset_type = balance["asset_type"]
        balance_amount = balance["balance"]
        print(f"Asset Type: {asset_type}, Balance: {balance_amount}")


def validate_account(public_key, server):
    try:
        server.load_account(public_key)
    except NotFoundError:
        print("The destination account does not exist!")
        print("You must be Creating Account!")
        create_account(public_key, server)


validate_account(root_keypair.public_key, server)


# Create a transaction and append payment operations for each public key
transaction = (
    TransactionBuilder(
        source_account=nearx_account,
        network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
        base_fee=100 * len(challenger4_ok),
    )
    .add_text_memo("Pagamento do DEV30K")
    .set_timeout(120)
)

for public_key, amount in challenger4_ok:
    transaction.append_payment_op(
        destination=public_key, asset=Asset.native(), amount=str(amount)
    )

# Build and sign the transaction
transaction = transaction.build()
transaction.sign(root_keypair.secret)

response = server.submit_transaction(transaction)
tx_hash = response["hash"]


tx = server.transactions().transaction(tx_hash).call()
print("✅ # Transaction details:")
print(f"  - ID: {tx['id']}")
print(f"  - Hash: {tx['hash']}")
print(f"  - Ledger: {tx['ledger']}")
print(f"  - Created At: {tx['created_at']}")
print(f"  - Source Account: {tx['source_account']}")
print(f"  - Memo: {tx['memo']}")
print(f"  - Fee Charged: {tx['fee_charged']}")
print(f"  - Operation Count: {tx['operation_count']}")
print(f"  - Successful: {tx['successful']}")
