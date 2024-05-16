# array

numeros = [2, 4, 7, 9, 12, 543, 542, 11]

maior_numero = max(numeros)
menor_numero = min(numeros)
somatorio = sum(numeros)
comprimento = len(numeros)
media = somatorio / comprimento

print(
    f"O maior número presente na lista é: {maior_numero} \n"
    + f"O menor número presente na lista é: {menor_numero} \n"
    + f"O total dos dados da lista é: {somatorio} \n"
    + f"A lista tem um total de {comprimento} números. \n"
    + f"A lista tem uma média de {media}"
)
