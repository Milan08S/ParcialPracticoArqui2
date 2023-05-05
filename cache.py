#Parcial Practico Arquitectura
#Miguel Angel Sanchez Paez
#Jose Daniel Ramirez Delgado

# Cache Memory ~ Set Associative (2 ways)
# Update Policies: Write Throught
# Replacement Policies: Random

# [Tamaño del bloque: 8 bytes] ~ [Total de Bloques: 32] ~ [Tamaño palabra: 1 byte]
# Total de direcciones: 2 ^ 11 = 2048
# Total de bits por direccion = 11 bits

# Calculo de offset: log2 (8) = 3 bits
# Calculo de index: 16 conjuntos se necesita 4 bits para representarlos en binario
# Calculo de tag: 11 - offset - index = 4 bits

# ----------------------------------
# |10  ...  7 | 6  ...  3 | 2 ... 0 |
# [   tag    ]|[  index  ]|[ offset]|
# |  4 bits   |   4 bits  |  3 bits |
# ----------------------------------




# total de bloques en la cache: 32 bloques
# numero de sets 16, dos bloques por cada set
# tamaño offset: 3 bits
# tamaño index o conjunto: 4 bits
# tamaño direccion 7 bits
# total direccion generada por procesador: 14 bits
# numero de palabras: 8 de 1 byte
# numero de direcciones de la memoria: 2048
# funcion de mapeado en asociativa por conjuntos: Set = direccion de bloque(hasta 2048) mod numero de sets en cache (16)
# tamaño del bloque: 8 bytes  


