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
import os

DIRECCION_BINARIO = 11

cache = {}

for i in range(16):
    cache[i] = [ [None, None, [None,None,None,None,None,None,None,None]], [None, None, [None,None,None,None,None,None,None,None]] ]

cont_miss = 0
cont_hits = 0

def imprimir_cache(): #inicializamos el cache
    '''
    for i in range(16):
        print(f"{i} {cache[i]}")
    '''
    #print(cache[2][0][2])
    for clave, valor in cache.items():
        print(f"Conjunto: {clave}")
        for lista in valor:
            print(lista)

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

def copiarDato(way,tag,index,Rango_inicio):
    j = 0
    # se agrega el tag al bloque en la cache
    cache[index][way][1] = tag 
    # Abrir el archivo en modo lectura
    with open("ramc.txt", "r") as archivo:
        # Lee linea por linea del archivo
        for i, linea in enumerate(archivo):
            # Si coincide el rango inicial entonces comienza a agregar datos desde ahi
            if i >= Rango_inicio and j <= 7:
                # Eliminar salto de línea al final del dato
                linea = linea.rstrip('\n')
                # agrega palabra por palabra al bloque de la cache
                cache[index][way][2][j] = linea 
                j += 1 
                # se itera 8 veces

def cargarDatoCache(tag,index,offset,direccion_random):
    offset = int(offset,2) # pasamos offset a decimal
    Rango_inicio = direccion_random - offset # le restamos a nuestro numero el offset en binario para que nos de el principio del rango

    flag, _ = searchCache(tag,index)

    if flag == 1:
        # se guarda en la primera via
        #print("ENTRO 1 VIA")
        copiarDato(0,tag,index,Rango_inicio)
        # por ultimo se cambia el bit de validez
        cache[index][0][0] = 1 
    elif flag == 2:
        # politica random para saber en que via se hace
        #print("ENTRO VIA ALEATORIA")
        way = random.randint(0, 1)
        copiarDato(way,tag,index,Rango_inicio)
        # por ultimo se cambia el bit de validez
        cache[index][way][0] = 1 
    else:
        #print("ENTRO 2 VIA")
        # se guarda en la segunda via
        copiarDato(1,tag,index,Rango_inicio)
        # por ultimo se cambia el bit de validez
        cache[index][1][0] = 1 

def actualizarDatoRam(direccion_random,dato):
    # Abrir el archivo en modo lectura
    with open("ramc.txt", "r") as archivo_original, open("temp.txt", "w") as archivo_nuevo:
        # Iterar linea por linea del archivo
        for i, linea in enumerate(archivo_original):
            if i == direccion_random: # encontrar la direccion a actualizar el dato
                archivo_nuevo.write(dato + " <==Dato Modificado==>\n")
            else:
                archivo_nuevo.write(linea)
    # Cerrar ambos archivos y renombrar el nuevo archivo
    os.remove("ramc.txt")
    os.rename("temp.txt", "ramc.txt")


    

def actualizarDatoCache(way,index,offset,dato):
    offset = int(offset, 2)
    cache[index][way][2][offset] = dato

def searchCache(tag,index):
    way = -1
    flag = 0 # indicar en la iteracion si no se encontro el dato en las 2 vias para no generar 2 misses
    if cache[index][0][0] == None: 
        #print("NO EXISTE EN LA CACHE")
        flag = 1 # read_miss
    else:

        if cache[index][0][1] == str(tag): # si exite un bloque con un dato valido se compara su tag
            #print(" EL DATO  EN LA VIA 0")
            flag = 0 # read_hit
            way = 0
        elif cache[index][1][1] == str(tag):
            #print(" EXISTE EN LA VIA 1")
            flag = 0 # read_hit
            way = 1
        else: 
            #print("EL CONJUNTO ESTA LLENO")
            flag = 2 # ejecuta el protocolo de reemplazo
            
    return flag, way

def cacheController(direccion_random, dato): #controlador del cache
    global cont_hits, cont_miss

    dir_binario = format(direccion_random, '0' + str(DIRECCION_BINARIO) + 'b')
    direccion_random += 1 

    offset = dir_binario[0:3]
    index = int(dir_binario[3:7],2)
    tag = dir_binario[7:11]
    
    flag, _ = searchCache(tag,index)

    # Caso: read
    if dato == None: 

        if flag == 0: # Read - Hit
            cont_hits += 1 
        else: # Read - Miss
            cont_miss += 1
            cargarDatoCache(tag,index,offset, direccion_random) # se tiene que cargar el dato desde la ram 
    # Caso: write
    else: 
        if flag == 0: # Read - Hit
            print("WRITE HIT: " + str(dato))
            cont_hits += 1 # Write - Hit
            #print("ESTE ES EL DATO 1: " + str(dato))
            actualizarDatoRam(direccion_random,dato) # actualiza la memoria principal
            _,way = searchCache(tag,index)
            actualizarDatoCache(way,index,offset,dato) # actualiza el dato en la cache y memoria principal (write - throught)
        else: # Read - Miss
            print("WRITE MISS: " + str(dato))
            cont_miss += 1 # Write - Miss
            #print("ESTE ES EL DATO 2: " + str(dato))
            cargarDatoCache(tag,index,offset, direccion_random) # carga el dato que no estaba presente en la cache
            actualizarDatoRam(direccion_random,dato) # actualiza la memoria principal
            _,way = searchCache(tag,index)
            actualizarDatoCache(way,index,offset,dato) # carga el dato actualizado a la cache
        

def numero_casos():
    # proceso guarda 0 si es read y 1 si es write
    caso = random.randint(0, 1)
    return caso

def direccion_random(caso):
    direccion_random = random.randint(0, 2047)
    if caso == 0: #si es read
        cacheController(direccion_random, None)
    else: #si es write
        dato_random = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWYXZ', k=8))
        # Eliminar salto de línea al final del dato
        dato_random = dato_random.rstrip('\n')
        cacheController(direccion_random,dato_random)

def crearCachetxt():
    with open('cache.txt', 'w') as archivo:
        for clave, valor in cache.items():
            archivo.write(f"Conjunto: {clave}\n")
            for lista in valor:
                archivo.write(str(lista) + '\n')

def ejecucion_procesos(procesos):
    for i in range(procesos):
        caso = numero_casos()
        direccion_random(caso)    

def menu():
    print("1. Inicializar Memoria Ram")
    print("2. Ejecutar programa")
    print("3. Salir")




def main():
    while True:
        menu()
        opcion = int(input("Selecciona una opción: "))
    
        if opcion == 1:
            inicializar_ram()
        elif opcion == 2:
            procesos = int(input("Numero de procesos: "))
            ejecucion_procesos(procesos)
            imprimir_cache()
            print(cont_hits)
            print(cont_miss)
            crearCachetxt()
            
        elif opcion == 3:
            print("Saliendo del menú...")
            break
        else:
            print("Opción inválida. Selecciona una opción del 1 al 3.")

main()

