from stellar_sdk import Keypair

random_pair = Keypair.random()

print("Random Private Key: ", random_pair.secret)
print("Random Public Key:", random_pair.public_key)
