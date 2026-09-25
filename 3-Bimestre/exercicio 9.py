numero = int(input("Digite um numero inteiro positivo: "))

if numero >= 0:
    contador = 1
    fatorial = 1

    while contador <= numero:
        fatorial = fatorial * contador
        contador += 1

    print("Fatorial:", fatorial)
else:
    print("Numero invalido.")