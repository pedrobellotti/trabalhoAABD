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
    print("--Criando produtos--")
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

    #Limpa o banco
    #redis.flushall()
    #Cria os produtos
    criaProdutos(redis)

    #Faz as consultas
    print("--Fazendo as consultas--")

    #Pesquisa um produto
    print("\n--Consulta 1: um produto especifico--")
    print(redis.hgetall("prod:1")) 

    #Faz o "select * from Produto"
    print("\n--Consulta 2: todos os produtos--")
    lista = redis.scan(match="prod:*")[1]
    for item in lista:
        print(redis.hgetall(item))

    #Pesquisa por produtos em um range de preço
    print("\n--Consulta 3: produtos dentro de um range de preço--")
    lista = redis.zrangebyscore("lista_preco", 0, 20)
    for item in lista:
        print(redis.hgetall(item))

    #Busca por todos os produtos ordenados pelo preço
    print("\n--Consulta 4: todos os produtos ordenados pelo preço (menor para o maior)--")
    lista = redis.zrangebyscore("lista_preco", 0, float('inf'))
    for item in lista:
        print(redis.hgetall(item))
    
    #Busca por quantos produtos existem registrados
    print("\n--Consulta 5: quantidade de produtos registrados--")
    print(len(redis.keys("prod:*")))

    #Desliga o banco
    #r.shutdown()

if __name__ == '__main__':
    main()