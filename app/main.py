from aiohttp import web
import database


async def create_transaction(request):
    # Extrai os dados da requisição
    data = await request.json()
    client_id = int(request.match_info["id"])
    valor = int(data["valor"])
    tipo = data["tipo"]
    descricao = data["descricao"]

    transaction_result = await database.create_transaction(client_id, valor, tipo, descricao)

    if transaction_result["possui_erro"]:
        if transaction_result['mensagem'] == "saldo insuficente":
            return web.Response(status=422)
        else:
            print(transaction_result['mensagem'])
            return web.Response(status=404)

    # Retorna uma resposta de sucesso
    return web.json_response(data=transaction_result, status=200)


async def get_statement(request):
    client_id = int(request.match_info["id"])
    statement = await database.get_statement(client_id)
    if statement is None:
        return web.Response(status=404, text="Cliente não encontrado.")
    
    # Formatação da resposta conforme especificado
    return web.json_response(statement, status=200)

async def init_app():
    # Inicializa o banco de dados
    await database.init_db()

    # Cria a aplicação web e adiciona as rotas
    app = web.Application()
    app.add_routes(
        [
            web.post("/clientes/{id}/transacoes", create_transaction),
            web.get("/clientes/{id}/extrato", get_statement),
        ]
    )
    return app


if __name__ == "__main__":
    import sys

    # Utiliza a porta do argumento da linha de comando para flexibilidade
    port = (
        int(sys.argv[1]) if len(sys.argv) > 1 else 9999
    )  # Porta padrão 9999 se não especificada
    web.run_app(init_app(), port=port)
