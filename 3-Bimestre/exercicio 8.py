numero = int(input("Digite um numero inteiro positivo: "))

divisor = 1
quantidade_divisores = 0

if numero > 0:
    while divisor <= numero:
        if numero % divisor == 0:
            quantidade_divisores += 1

        divisor += 1

    if quantidade_divisores == 2:
        print("O numero e primo.")
    else:
        print("O numero nao e primo.")
else:
    print("Numero invalido.")