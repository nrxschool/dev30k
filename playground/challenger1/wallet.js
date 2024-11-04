import { Keypair } from '@stellar/stellar-sdk';

const generateRandomKeypair = () => {
  const pair = Keypair.random()
  console.log(`Public Key: ${pair.publicKey()}`);
  console.log(`Public Key: ${pair.secret()}`);
};

generateRandomKeypair()