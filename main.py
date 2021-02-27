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

def conecta_redis():
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

def main():
    #Conecta no banco
    r = conecta_redis()
    if(r == -1):
        print("Erro ao conectar banco - aplicação encerrada!")
        return
    #Desliga o banco
    r.shutdown()

if __name__ == '__main__':
    main()