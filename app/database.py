import asyncpg
import os

DB_ENV = os.getenv("DB_HOSTNAME", "localhost")
DATABASE_URL = f"postgres://admin:123@{DB_ENV}:5432/rinha"


async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)


async def create_transaction(client_id, valor, tipo, descricao):
    async with pool.acquire() as connection:
        # Escolha a função com base no tipo de transação
        func_name = "creditar" if tipo == "c" else "debitar"
        # Prepare a instrução CALL para executar a stored procedure
        query = f"SELECT valor, tipo, descricao, TO_CHAR(realizada_em, 'YYYY-MM-DD HH24:MI:SS') AS realizada_em FROM {func_name}($1, $2, $3);"
        # Execute a stored procedure com os parâmetros
        # Execute the stored procedure with parameters
        result = await connection.fetch(query, client_id, valor, descricao)
        return result[0] if result else None


async def get_statement(client_id):
    async with pool.acquire() as connection:
        # Busque o saldo mais recente e as últimas transações
        balance_query = "SELECT valor FROM saldos WHERE cliente_id = $1;"
        transactions_query = """
            SELECT valor, tipo, descricao, TO_CHAR(realizada_em, 'YYYY-MM-DD HH24:MI:SS') AS realizada_em
            FROM transacoes
            WHERE cliente_id = $1
            ORDER BY realizada_em DESC
            LIMIT 10;
        """
        balance = await connection.fetchval(balance_query, client_id)
        transactions = await connection.fetch(transactions_query, client_id)
        # Se nenhum saldo ou transações forem encontrados, o cliente pode não existir
        if balance is None:
            return None
        # Converta as transações em uma lista de dicionários
        transactions_list = [dict(tx) for tx in transactions]
        # Construa o dicionário do extrato
        statement = {"saldo": balance, "ultimas_transacoes": transactions_list}
        return statement
