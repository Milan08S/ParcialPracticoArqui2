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

import random
import shutil

DIRECCION_BINARIO = 11

cache = {}
for i in range(16):
    cache[i] = [ [None, None, [None,None,None,None,None,None,None,None]], [None, None, [None,None,None,None,None,None,None,None]] ]

cont_miss = 0
cont_hits = 0

def inicializacion_cache(): #inicializamos el cache

    for i in range(16):
        print(f"{i} {cache[i]}")
    return cache
    
    '''for clave, valor in cache.items():
        print(f"Clave: {clave}")
        for lista in valor:
            print(lista)'''

def inicializar_ram():
    # Genera una lista de 2048 combinaciones aleatorias de 8 numeros
    combinations = [''.join(random.choices('0123456789', k=8)) for _ in range(2048)]

        # Crea un archivo de texto y escribe cada combinación en una línea separada
    with open('ram.txt', 'w') as file:
        for combination in combinations:
            file.write(combination + '\n')

        # Especifica el nombre del archivo original y el nombre de la copia
    original_file = 'ram.txt'
    copy_file = 'ramc.txt'

    # Crea una copia del archivo original en la misma carpeta
    shutil.copyfile(original_file, copy_file)

def cacheController(dir_binario, dato): #

    dir_mod = dir_binario[3:11]
    setCache = dir_mod % 16
    
    offset = dir_binario[0:3]
    index = int(dir_binario[3:7],2)
    tag = dir_binario[7:11]
    if dato == None: #en caso de ser read
        if cache[index][0][0] == None:
            cont_miss += 1
            
            pass
        else:
            
            pass
            
        
    else:
        #implementa dato 
        pass
        

def numero_casos():
    # proceso guarda 0 si es read y 1 si es write
    caso = random.randrange(0,1)
    return caso

def direccion_random(caso):
    direccion_random = random.randrange(0,2047)
    dir_binario = format(direccion_random, '0' + str(DIRECCION_BINARIO) + 'b')
    if caso == 0: #si es read
        cacheController(dir_binario, None)
    elif caso == 1: #si es write
        dato_random = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWYXZ', k=8))
        cacheController(dir_binario,dato_random)


def ejecucion_procesos(procesos):
    for i in range(procesos):
        caso = numero_casos()
        direccion_random(caso)    

def menu():
    print("1. Inicializar Memoria Ram")
    print("2. Ejecutar programa")
    print("3. Salir")

while True:
    menu()
    opcion = int(input("\n\nSelecciona una opción: "))
    
    if opcion == 1:
        inicializar_ram()
    elif opcion == 2:
        inicializacion_cache()
        ejecucion_procesos(procesos)
    elif opcion == 3:
        print("Saliendo del menú...")
        break
    else:
        print("Opción inválida. Selecciona una opción del 1 al 3.")


def main():
    menu()

main()

