import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração
API_BASE_URL = "http://localhost:9999"
CLIENT_IDS = [1, 2, 3, 4, 5]  # IDs dos clientes para os testes
TRANSACTIONS_PER_CLIENT = 50  # Quantidade de transações por cliente
TIMEOUT_SECONDS = 10  # Timeout para as requisições

def make_transaction(client_id):
    """
    Cria uma transação aleatória (crédito ou débito) para um cliente específico.
    """
    try:
        transaction_type = random.choice(['c', 'd'])
        amount = random.randint(1, 1000) * 100  # Valores em centavos
        description = ''.join(random.choices(string.ascii_letters, k=10))

        transaction_data = {
            "valor": amount,
            "tipo": transaction_type,
            "descricao": description
        }
        

        response = requests.post(f"{API_BASE_URL}/clientes/{client_id}/transacoes", json=transaction_data, timeout=TIMEOUT_SECONDS)
        # response.raise_for_status()  # Isso vai lançar um erro para respostas 4xx/5xx
        return response.json()
    except Exception as e:
        print(f"Erro ao realizar transação para o cliente {client_id}: {e}")
        return None

def get_client_balance(client_id):
    """
    Obtém o extrato do cliente.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/clientes/{client_id}/extrato", timeout=TIMEOUT_SECONDS)
        # response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao obter o extrato para o cliente {client_id}: {e}")
        return None

def test_client_transactions(client_id):
    """
    Testa as transações de um cliente.
    """
    try:
        for _ in range(TRANSACTIONS_PER_CLIENT):
            transaction_result = make_transaction(client_id)
            if transaction_result:
                print(f"Cliente {client_id} - Transação: {transaction_result}")

        balance = get_client_balance(client_id)
        if balance:
            print(f"Cliente {client_id} - Saldo: {balance['saldo']}")
    except Exception as e:
        print(f"Erro durante os testes para o cliente {client_id}: {e}")

def main():
    """
    Executa os testes em paralelo para todos os clientes.
    """
    with ThreadPoolExecutor(max_workers=len(CLIENT_IDS)) as executor:
        futures = [executor.submit(test_client_transactions, client_id) for client_id in CLIENT_IDS]
        for future in as_completed(futures):
            future.result()  # Isso vai esperar cada thread terminar

if __name__ == "__main__":
    main()
