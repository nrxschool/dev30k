# Aula 2: Criação de Wallets e Transações no Stellar

## Abertura

- Boas vindas, interação
- Se aprensentar, apresentar a NearX e o DEV30K

### Programa da aula:

0. Stellar e Blockchain
1. Como funcionam as Wallets
2. Resolução do desafio 1: Criar um par de chaves
3. Pagamento dos classificados
4. Introdução às Transações no Stellar

---

## 0. O que é a Stellar

- Ecosistema e [Comunidade](https://stellar.org/community)
- [Documentação](https://developers.stellar.org)
- [SDK](https://developers.stellar.org/docs/tools/sdks/library)

## 1. Como funcionam as Wallets

- Intodução a criptografia: Hash
- Intodução a criptografia: Chaves Públicas
- Intodução a criptografia: Segurança

---

## 2. Configurando ambiente

1. Instalar Python, Node e Docker
2. Criar ambiente python (stellar_sdk)
3. Criar ambiente javascript (stellar-sdk)

---

## 3. Criar um par de chaves

- Criar par de chaves em Python
- Criar par de chaves em JavaScript

---

## 3. Pagamento dos Classificados

- Explicar o conceito de contas na rede Stellar [doc](https://developers.stellar.org/docs/build/guides/basics/create-account)
- Pegar a chave pública das pessoas do forms
- Escrever o script de `create_account_op`

---

## 4. Introdução às Transações no Stellar

- Explicar o conceito de transações: from, to, fee, memo, hash, explorer e redes
- Explicar sobre os tipos de transações que são possiveis em Stellar
- Ensinar criar transações de `create_account_op` e `payments_op`
- Criar uma transação simples em Python

## 5. Desafio Inicial (Criar uma transação com "DEV30K" assinado no MEMO)

- Explicar o desafio número 2:
  - Utilizar o Stellar SDK em **Python** ou **JavaScript**.
  - Assinar o texto "DEV30K" usando a chave privada
  - Criar uma transação `menage_data_op` com a chave="desafio" e o valor="Assinatura do texto `DEV30K`".
  - Enviar para a rede Mainnet da Stellar.
- Explicar os critérios de aceite: hash da transação no forms

---

## Recapitulação

- [x] Aprendemos como funcionam as wallets
- [x] Aprendemos o que é uma transação em blockchain
- [x] Aprendemos quais tipos de transações a rede Stellar suporta
