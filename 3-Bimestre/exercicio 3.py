numero = int(input("Digite um numero inteiro positivo: "))
contador = 1

if numero > 0:
    while contador <= numero:
        print(contador)
        contador += 1
else:
    print("Numero invalido. Digite um valor positivo.")