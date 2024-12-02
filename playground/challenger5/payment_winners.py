from stellar_sdk.exceptions import NotFoundError
from stellar_sdk import Asset
from stellar_sdk import Keypair, Network, TransactionBuilder, Server
from requests import get, RequestException


PRV_KEY = "SCDWJVAFMCNO25CKUYZQDUBNR6I6STCQ3XNYCTYBTS7S46PYUZUAKF5M"
root_keypair = Keypair.from_secret(PRV_KEY)
server = Server(horizon_url="https://horizon.stellar.org")
nearx_account = server.load_account(root_keypair.public_key)


def read_public_keys():
    with open("public_keys1.txt", "r") as file:
        public_keys = [line.strip() for line in file.readlines()]
    return public_keys


challenger5_ok = [
    # PAGAMENTO DEV30k
    # "GBPTLZBA5AO5LM7LZZBU6G2DBULROCCFBHDQWGUFJ2YBUMBZZ7EYDAJ4", https://stellar.expert/explorer/public/tx/57d0e4a77084f9ddf4014887e613c7c9a78c41703cad50c0058769d5a3c6c32f
    # "GB5UBWORACGMEHWLBN4CQMTOGPALCSOXTQLX4K7HU3SQE4DHKRV7GGD7", https://stellar.expert/explorer/public/tx/14a6d1fe3c13a7adb6d936f7f16b97da4918d29b7b9ddb27323f278b59f78026
    # "GCYQ6P5MPT6O56GQBHDCV7NCOURN6TT5M7DKYMK737ZDT5XTCR52YE5V", https://stellar.expert/explorer/public/tx/0844150432e84245f981f24b6f57d31815c1907e96e9e2bd8dc87f7fd4557e8d
    # "GD7D2Z6LQ5F7FDLDVCKPSGNXS6REDF3ABPM2ADKIZN4PIBWDKKQH4AS7", https://stellar.expert/explorer/public/tx/90ce97d41669e47f7e91ee7fcd7b18145efeb066b926e0bec274dd077912c67b
    # "GA4WYK5DJRMVFYYC7XJQJHTJSWDESEXTTATXCUF2OQZ2Z5UVJJRYQAZU", https://stellar.expert/explorer/public/tx/0844150432e84245f981f24b6f57d31815c1907e96e9e2bd8dc87f7fd4557e8d
    # "GBGIIFSLVKS2Z4XORQMOT5GV5JBTI3APQCXFNNDJ6T3U3GHQSBMOFGX7", https://stellar.expert/explorer/public/tx/33d31149f7122ea04b877b70c69fe251a15b9fdbe69818e1fdd0eaaad672586c
    # "GBB6IIYOJ3QHN246XTDF2ZZ2Q7JPSOJLKED6IZJD6XBEUNABGKEB6UIB", https://stellar.expert/explorer/public/tx/ec19d951a5a2de047eb39e21af11bc38318010247a908e1f5ff220b7d773b8a5
    # "GDEE7QQXP2UU42HLLE4Y3IXNYC6LG674UKK2IUBIFYBOJMT43VMQKSJN", https://stellar.expert/explorer/public/tx/ad24a1a08b63bafea241cae3b4a57f4e0d716cb6d366f490430f399717416f2d
    # "GBBIVZN5N7EMYMQHZL4ME64GWDM5REJDLFBDET7KLIIA6GQRQVJ2IQWE", https://stellar.expert/explorer/public/tx/665b451b4e1f9933ffbf2f5888900c36342e0221c88aadfaafeda79197bf6326
    # "GAGL327YR6JV4WUOO6TWRXB3UYWGAAOGGZAUKAJFTJDVJT6A4PASMRMS", https://stellar.expert/explorer/public/tx/7ccefb3e415957c892576a0e5d1623af25ae30173f54d2d889e28765894221a0
    # "GAFASLN5AWEKSDNXLRUH525N2FSNTBFLFG53EPUEOKRQCWUI2BLT5JES", https://stellar.expert/explorer/public/tx/1711df47e1b29c926cf6116c7088ac95eb448b855ec509163970bece8ccdf05c
    # "GBBZVRUFJONG6ECPQELXJIOKRH3CKFO24ESZL6ZZULBTHMFOB3OJH5IX", https://stellar.expert/explorer/public/tx/e89839b123256520eb213027f72ef3ef15b070010a0b88172d850943cb2a8d4b
    # "GDZOBWMQ7UT5O6TB7VVQSBKFIZ2XF7HHZJYOZYXN74ADNFWJX4RE2CMN", https://stellar.expert/explorer/public/tx/d05712baa622f3ef5a254a2aaaf00a2068518a32914d4f3f1456b111160cf29f
    # "GAAHX4TUAJPVWFDAEYKLT52ROZMYERWSKM7ZIYKT3JZQ6JJS73HRYHRU", https://stellar.expert/explorer/public/tx/abb44c0d6b5dc55c4bd26d94e675a7a95d05b654756673cc008f9124abdf6bf1
    # "GASBS5FHTGFFMYTYYIITOTX6A4ZG3J55BJGOTSQXCRDTIRRZBA6J63MG", https://stellar.expert/explorer/public/tx/adcce0305cf0962b6ab9d81f2d7286d144f6c4c5eb84643c3f88af8020439f7e
    # "GDFO7IDGWQNVHI5QHVJDXYQR3T7BZOD3ZYXA65U7TAIPKF5VKSLNQZVA", https://stellar.expert/explorer/public/tx/d79a3cef312299f33a4fe7c481d6790dde40db2ab0b8ed38785342d28aabfbdc
    # "GANSVIA3OR537VRFFB5S3Y3HA64FMNPJF4YNVLS7LHEBYCLXQ57J3QDS", https://stellar.expert/explorer/public/tx/973fcfba3176c665124088867a02169f3688ec47d3db1aa33749e21c2a49c951
    # "GCSL7N3K3HNABE63MSHWZFRHJ2UGN6C7USQ7KEL3KGNX3BPZ4ZHCPRBG", https://stellar.expert/explorer/public/tx/b323070c811513bd634448b8c2c68d2c3c712e86cbfd8bcf9cb6419cd01967d0
    # "GBT6GIJVW4Z56QTOMVVBIPGYOG4COYEFS2P5WKELER47SY2ZK2OSKTAV", https://stellar.expert/explorer/public/tx/be23fed543565d61ed928e0d276f3084ad7e565445d78f4ead6bd8e6d893cc6e
    # "GCVZ5JGBMIB6F7522DYEVY66OP6BRORJVMHDVMKCIPSJ4FYTHBYLSRX5", https://stellar.expert/explorer/public/tx/62b8f09fb5302a41d7ff971997e85628c02aae8c02c7dd003e33498fe500db38
    # "GDX4C4ACE4AKYUWW5O5AA3ZEGD5S2SF7N56MHMFYHNOUG2IXZOOH6HUE", https://stellar.expert/explorer/public/tx/f03f183fc0cd624382f7b97ea18cef570dcb0808a493815bec6382b9d16ad651
    # "GCMUASIHX2JBY2FJNRTXVEGDYNCWWZHI7CLE7DCYIYRGPK3Y4YBNHX65", https://stellar.expert/explorer/public/tx/b4c753f15b944a1c1fcdbc9092e52b9d0455edd6d10c0b41ef66aa6ba9e79de1
    # "GBF7NZHSZYYUTPYVXMAGYODM66M5BYMESE2UYVWY2OAMFHAZKA7BFRNM", https://stellar.expert/explorer/public/tx/1efa5d7b8d87dfa8709a430d86408f11ae215174125c2a2d577b35109449a6bd
    # "GBV6QI4WLBWM2CTL4Q5ZG6CDYHOULCNYNRV4DLKRCCU7HIJUIPZJXF2F", https://stellar.expert/explorer/public/tx/32dcaa2c5c02bbfab983a3e34bb9a644d708280d0d6dd67a0463b010e9b3100b
    # "GBNTK7YLWIKRVUMUEZT62R2ABN4NSKVUYBR3M5CGCPXOEL7JNW5VTDAV", https://stellar.expert/explorer/public/tx/e3a8bef6fe2d48496e7a7080e88d053fa4fd3b590335b10684f2652cbdac8e5e
    # "GBWUOQH4VD43D7QLWGRQRQ5MC7XBXRJ2E4RPUHFKAFCPVLYILWWEVYUG", https://stellar.expert/explorer/public/tx/d532055afa4f8707b9fe5a55f2d7caec5db9f646b0e91076c5b2bef542ecf64d
    # "GDXSK5FVZEQ2KMHPMQD4VNQXBS3FLSNAIRE246CBYX5XLDTQJ4B5AEFA", https://stellar.expert/explorer/public/tx/0a59f9a9b353acd73c6579063d09c476d677885b4b178ef271e26d6f30a1579b
    # "GB5DK65YH6MYYOZ5TXPJSMYTG7Y7544RMLSNS3BLXKJXPZ4S65SEYFU2", https://stellar.expert/explorer/public/tx/3c9028d9c2b4bc3196cc377a30fb49a68f73c2a40fd4ea1d535d3e9fdb0c8d5f
    # "GB227MAPSVM2PJBRLHW32ZWQYFCIEJ5RIJ3KTC2AN7GRY6IHLNUO5LCG", https://stellar.expert/explorer/public/tx/8460fbb1722a1a0626f74bde5e5fdb8034e04f79fa7eca64f078eec76aa03c6f
    # "GB2BBGHVOHUANZOB7E3B3HOQXZOJL26JKQFFNWFCWKSNPOGXEHMBVPUQ", https://stellar.expert/explorer/public/tx/148e55fcb4ee19c7c7b048b606e82b9e0df570c1fafe28c64b301706da0b32fd
]

public_keys = list(dict.fromkeys(challenger5_ok))


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
        base_fee=10000,
    )
    .add_text_memo("Pagamento FINAL DEV30K")
    .set_timeout(15)
)

for public_key in public_keys:
    transaction.append_payment_op(
        destination=public_key, asset=Asset.native(), amount=str(220)
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
