'''
Funções da aplicação:
1- Cadastrar produtos e fornecedores
2- Realizar compras e dar entrada dos produtos no estoque
3- Realizar vendas e dar saída dos produtos no estoque
4- Gerar relatórios de fluxo de caixa, vendas e estoque
5- Realizar 10 consultas distintas (consulta normal, consulta com sort, consulta com orderby, etc)
'''

import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

def conectaRedis():
    try:
        #Faz a conexão
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        #Cria uma variável de teste
        r.set("msg:hello", "Hello Redis!")
        #Pega a variável de teste e imprime
        print(r.get("msg:hello"))
        #Retorna a conexão
        return r
    except Exception as e:
        print(e)
        return -1


def criaProdutos(r):
    #Adiciona itens no banco
    r.hset("prod:1", "nome", "Arroz")
    r.hset("prod:1", "desc", "Arroz branco")
    r.hset("prod:1", "preco", 30)
    r.hset("prod:1", "estoque", 10)
    #Lista de produtos (ids)
    r.zadd("lista_prod", {"prod:1": 1})
    #Lista de precos
    r.zadd("lista_preco",{"prod:1": 30})

    r.hset("prod:2", "nome", "Feijao")
    r.hset("prod:2", "desc", "Feijao vermelho")
    r.hset("prod:2", "preco", 17)
    r.hset("prod:2", "estoque", 6)
    r.zadd("lista_prod", {"prod:2": 2})
    r.zadd("lista_preco",{"prod:2": 17})

def vendeProduto(r, produto):
    r.hincrby(produto, "estoque", -1)

def compraProduto(r, produto):
    r.hincrby(produto, "estoque", 1)

def main():
    #Conecta no banco
    redis = conectaRedis()
    if(redis == -1):
        print("Erro ao conectar banco - aplicação encerrada!")
        return

    criaProdutos(redis)

    #Faz as pesquisas
    print(redis.hgetall("prod:1")) #Pesquisa um produto
    print(redis.zrangebyscore("lista_preco", 0, 30)) #Pesquisa por produtos em um range de preço
    '''
    lista = redis.zscan("lista_prod")
    for i in lista:
        print (i)
    '''

    #Desliga o banco
    #r.shutdown()

if __name__ == '__main__':
    main()