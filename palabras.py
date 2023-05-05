import random

# Genera una lista de 2048 combinaciones aleatorias de tres letras en mayúscula
combinations = [''.join(random.choices('0123456789', k=8)) for _ in range(2048)]

# Crea un archivo de texto y escribe cada combinación en una línea separada
with open('combinations.txt', 'w') as file:
    for combination in combinations:
        file.write(combination + '\n')
