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

    r.hset("prod:3", "nome", "Macarrao")
    r.hset("prod:3", "desc", "Macarrao instantaneo")
    r.hset("prod:3", "preco", 2.5)
    r.hset("prod:3", "estoque", 9)
    r.zadd("lista_prod", {"prod:3": 3})
    r.zadd("lista_preco",{"prod:3": 2.5})
    r.zadd("lista_ofertas", {"prod:3": 10}) #Produto em oferta com 10% de desconto

    r.hset("prod:4", "nome", "Garrafa de agua")
    r.hset("prod:4", "desc", "Agua com gas")
    r.hset("prod:4", "preco", 1.75)
    r.hset("prod:4", "estoque", 0)
    r.zadd("lista_prod", {"prod:4": 4})
    r.zadd("lista_preco",{"prod:4": 1.75})

def vendeProduto(r, produto):
    r.hincrby(produto, "estoque", -1)

def compraProduto(r, produto):
    r.hincrby(produto, "estoque", 1)

def criaFornecedores(r):
    print("--Criando fornecedores--")
    #Fornecedor 1
    r.hset("forn:1", "nome", "Fornecedor 1")
    r.hset("forn:1", "cidade", "Juiz de Fora")
    r.hset("forn:1", "ddd", 32)
    r.hset("forn:1", "telefone", "3232-3232")
    r.zadd("lista_forn", {"forn:1": 1})
    r.zadd("lista_regiao", {"forn:1": 32})
    #Fornecedor 2
    r.hset("forn:2", "nome", "Fornecedor 2")
    r.hset("forn:2", "cidade", "Rio de Janeiro")
    r.hset("forn:2", "ddd", 21)
    r.hset("forn:2", "telefone", "9898-9898")
    r.zadd("lista_forn", {"forn:2": 2})
    r.zadd("lista_regiao", {"forn:2": 21})

    #Adiciona fornecedores nos produtos
    r.lpush("produtos_forn:1", "prod:1")
    r.lpush("produtos_forn:1", "prod:3")
    r.lpush("produtos_forn:2", "prod:2")
    r.lpush("produtos_forn:2", "prod:4")

def printMenu():
    print("-----Menu-----")
    print("1: consultar um produto especifico")
    print("2: consultar todos os produtos")
    print("3: consultar produtos dentro de um range de preço")
    print("4: consultar todos os produtos ordenados pelo preço (menor para o maior)")
    print("5: consultar a quantidade de produtos registrados")
    print("6: consultar produtos sem estoque")
    print("7: consultar fornecedor de um produto")
    print("8: consultar produtos de um fornecedor")
    print("9: consultar o telefone de fornecedores de produtos sem estoque")
    print("10: consultar se um produto existe ou não no banco")
    print("0: sair da aplicação")
    op = input("Digite uma opção: ")
    return op

def main():
    #Conecta no banco
    redis = conectaRedis()
    if(redis == -1):
        print("Erro ao conectar banco - aplicação encerrada!")
        return

    #Limpa o banco
    #redis.flushall()

    #Cria os produtos e fornecedores
    criaProdutos(redis)
    criaFornecedores(redis)

    op = printMenu()
    while(True):
        if(op == '0'):
            return
        elif (op == '1'):
            #Pesquisa um produto
            print("Informações do produto 1 (prod:1):")
            print(redis.hgetall("prod:1"))
        elif (op == '2'):
            #Faz o "select * from Produto"
            print("Lista de todos os produtos:")
            lista = redis.scan(match="prod:*", count=100)[1]
            for item in lista:
                print(redis.hgetall(item))
        elif (op == '3'):
            #Pesquisa por produtos em um range de preço
            print("Produtos com o preço entre 0 e 20 reais")
            lista = redis.zrangebyscore("lista_preco", 0, 20)
            for item in lista:
                print(redis.hgetall(item))
        elif (op == '4'):
            #Busca por todos os produtos ordenados pelo preço
            print("Lista de todos os produtos ordenados pelo preço")
            lista = redis.zrangebyscore("lista_preco", 0, float('inf'))
            for item in lista:
                print(redis.hgetall(item))
        elif (op == '5'):
            #Busca por quantos produtos existem registrados
            print("Quantidade de produtos registrados:")
            print(len(redis.keys("prod:*")))
        elif (op == '6'):
            #Consulta produtos com estoque 0
            print("Lista de produtos sem estoque:")
            produtos = redis.scan(match="prod:*", count=100)[1]
            lista = []
            for item in produtos:
                produto = redis.hgetall(item)
                if(produto['estoque'] == '0'):
                    lista.append(produto)
            for produto in lista:
                print (produto)
        elif (op == '7'):
            #Consulta fornecedor de um produto
            for i in range(1, len(redis.keys("forn:*"))+1):
                f = redis.lrange("produtos_forn:"+str(i), 0, -1)
                for produto in f:
                    if (produto == 'prod:1'):
                        print("O fornecedor do produto 1 (prod:1) é:")
                        print(redis.hgetall("forn:"+str(i)))
        elif (op == '8'):
            #Consultar produtos de um fornecedor
            produtos = redis.lrange("produtos_forn:2", 0, -1)
            print("Os produtos fornecidos pelo fornecedor 2 (forn:2) são:")
            for produto in produtos:
                print(redis.hgetall(produto))
        elif (op == '9'):
            #Consulta telefones dos fornecedores dos produtos sem estoque
            print("Telefones dos fornecedores de produtos sem estoque:")
            produtos = redis.scan(match="prod:*", count=100)[1]
            lista = []
            for item in produtos:
                produto = redis.hgetall(item)
                if(produto['estoque'] == '0'):
                    lista.append(produto)
            for produto in lista:
                print ("O produto %s está fora de estoque." % produto['nome'])
                for i in range(1, len(redis.keys("forn:*"))+1):
                    f = redis.lrange("produtos_forn:"+str(i), 0, -1)
                    for produto_f in f:
                        if (redis.hget(produto_f, "nome") == produto["nome"]):
                            print("O telefone de seu fornecedor é:")
                            print(redis.hget("forn:"+str(i),'telefone'))
        elif (op == '10'):
            #Consulta se um produto existe no banco
            ids = ['prod:1', 'prod:999']
            for prod in ids:
                if (redis.exists(prod)):
                    print("O produto %s existe no banco." % prod)
                else:
                    print("O produto %s não existe no banco." % prod)
        else:
            print ("Opção inválida!")
        op = printMenu()

    #Desliga o banco
    #r.shutdown()

if __name__ == '__main__':
    main()