senha_correta = 1234
tentativas = 1
limite_tentativas = 3

senha = int(input("Digite a senha: "))

while senha != senha_correta and tentativas < limite_tentativas:
    senha = int(input("Senha incorreta. Tente novamente: "))
    tentativas += 1

if senha == senha_correta:
    print("Acesso liberado.")
else:
    print("Acesso bloqueado.")