from stellar_sdk.transaction_envelope import TransactionEnvelope
from stellar_sdk import Keypair, Network, Server, ManageData
from stellar_sdk.exceptions import BadSignatureError
from stellar_sdk.exceptions import NotFoundError
import base64


def read():
    # Configurações iniciais
    SERVER_URL = "http://localhost:8000"
    server = Server(horizon_url=SERVER_URL)

    # Ler o hash da transação do arquivo
    try:
        with open("tx_hash.txt", "r") as f:
            lines = f.readlines()
            tx_hashes_and_public_keys = [line.strip().split() for line in lines]
    except FileNotFoundError as err:
        new_msg ="🚨 Arquivo 'tx_hash.txt' não encontrado. Execute o Script 1 primeiro."√
        raise FileNotFoundError(new_msg) from err

    for tx_hash, public_key in tx_hashes_and_public_keys:
        print(f"\n🔐 Conta da Transação: {public_key}")
        print(f"🔗 Hash da Transação:  {tx_hash}")

        # Recuperar a transação pelo hash
        try:
            tx = server.transactions().transaction(tx_hash).call()
        except NotFoundError:
            print("🚫 Transação não encontrada na rede.")
            continue
        except Exception as e:
            raise Exception(f"🚨 Erro ao recuperar a transação") from e

        # Recuperar o envelope XDR da transação
        try:
            envelope_xdr = tx["envelope_xdr"]
            tx_envelope = TransactionEnvelope.from_xdr(
                envelope_xdr, Network.STANDALONE_NETWORK_PASSPHRASE
            )
        except Exception as e:
            raise Exception("🚨 Erro ao decodificar o envelope XDR:") from e


        # Extrair a operação Manage Data com a chave "desafio"
        manage_data_op = None
        for op in tx_envelope.transaction.operations:
            if isinstance(op, ManageData) and op.data_name == "desafio":
                manage_data_op = op
                break

        if not manage_data_op:
            print("🚫 Operação 'manage_data' com a chave 'desafio' não encontrada na transação.")
            raise NotFoundError(f"👀 {tx_envelope.transaction.operations}")

        # Mensagem original
        mensagem = "DEV30K".encode()
        # Encode para base64
        mensagem_b64 = base64.b64encode(mensagem)
        print(f"📧 Mensagem em base64: {mensagem_b64.decode()}")

        # Obter a assinatura (bytes)
        assinatura_bytes = manage_data_op.data_value
        print(f"📝 Assinatura (hex): {assinatura_bytes.hex()}")

        # Criar um objeto Keypair a partir da chave pública
        try:
            keypair = Keypair.from_public_key(public_key)
        except Exception as e:
            raise Exception("🚨 Erro ao criar Keypair a partir da chave pública:") from e

        # Verificar a assinatura
        try:
            keypair.verify(mensagem_b64, assinatura_bytes)
            print("✅ A assinatura é válida. A mensagem foi assinada pela chave pública fornecida.")
        except BadSignatureError:
            print("❌ A assinatura é inválida. A mensagem não foi assinada pela chave pública fornecida.")
        except Exception as e:
            raise Exception("🚨 Erro ao verificar a assinatura:") from e