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

# Definir variables y constantes
WORD_SIZE = 1
BLOCK_SIZE = 8
NUM_BLOCKS = 32
NUM_SETS = 16
NUM_WAYS = 2
CACHE_SIZE = NUM_SETS * NUM_WAYS * BLOCK_SIZE

ram_data = []
cache_data = [[{'valid': False} for j in range(NUM_WAYS)] for i in range(NUM_SETS)]
hits = 0
misses = 0

# Leer archivo de texto de la memoria RAM
with open('ram.txt', 'r') as ram_file:
    for line in ram_file:
        ram_data.append(line.strip())

# Máquina de estados del controlador de la caché
class CacheController:
    def __init__(self):
        self.state = 'IDLE'
        self.set_index = 0
        self.tag = 0
        self.word_offset = 0
        self.op_type = 'READ'
        self.data = None
        self.way = 0
        self.hit = False

    def transition(self, input):
        state = self.state
        if state == 'IDLE':
            if input == 'READ':
                self.state = 'READ_MISS'
                self.memory_access += self.block_size
            elif input == 'WRITE':
                self.state = 'WRITE_MISS'
                self.memory_access += self.block_size
        elif state == 'READ_MISS':
            if self.check_cache_hit():
                self.state = 'IDLE'
                self.hit_count += 1
            else:
                self.state = 'READ_BLOCK'
                self.evict_block()
                self.fetch_block()
                self.memory_access += self.block_size
        elif state == 'WRITE_MISS':
            if self.check_cache_hit():
                self.state = 'IDLE'
                self.hit_count += 1
            else:
                self.state = 'WRITE_BLOCK'
                self.evict_block()
                self.fetch_block()
                self.memory_access += self.block_size
        elif state == 'READ_BLOCK':
            self.state = 'IDLE'
            self.hit_count += 1
        elif state == 'WRITE_BLOCK':
            self.state = 'IDLE'
            self.hit_count += 1
        return self.state
    # Función para generar direcciones aleatorias
    def generar_direccion():
        return random.randint(0, 2047)
    

# Clase de la memoria RAM
class MemoriaRAM:
    def __init__(self, archivo):
        self.archivo = archivo

    # Función para leer un bloque de datos de la RAM
    def leer_bloque(self, direccion):
        bloque = []
        with open(self.archivo, 'r') as f:
            for i in range(8):
                f.seek(direccion*8 + i)
                bloque.append(f.read(1))
        return bloque

    # Función para escribir un bloque de datos en la RAM
    def escribir_bloque(self, direccion, bloque):
        with open(self.archivo, 'r+') as f:
            for i in range(8):
                f.seek(direccion*8 + i)
                f.write(bloque[i])

# Clase de la memoria cache
class MemoriaCache:
    def __init__(self):
        # Configuración de la cache
        self.tam_palabra = 1 # 1 byte
        self.tam_bloque = 8 # 8 bytes
        self.num_bloques = 32
        self.num_vias = 2
        self.num_sets = self.num_bloques // self.num_vias
        self.cache = [[[0 for _ in range(self.tam_bloque)] for _ in range(self.num_vias)] for _ in range(self.num_sets)]
        self.dirty_bits = [[False for _ in range(self.num_vias)] for _ in range(self.num_sets)]
        self.tag_bits = [[0 for _ in range(self.num_vias)] for _ in range(self.num_sets)]
        self.reemplazo_aleatorio = True
        self.actualizacion_write_through = True

        # Contadores de hits y misses
        self.hits = 0
        self.misses = 0

    # Función para buscar un bloque en la cache
    def buscar_bloque(self, direccion):
        set_index = direccion % self.num_sets
        tag = direccion // self.num_sets
        for i in range(self.num_vias):
            if self.tag_bits[set_index][i] == tag:
                return set_index, i
        return set_index, None
    
 # Función para obtener un bloque de datos de la cache 

    def obtener_bloque(self, direccion):

        # Calcular el índice y la etiqueta correspondiente a la dirección
        indice = (direccion // self.tam_bloque) % self.num_sets
        etiqueta = direccion // (self.num_sets * self.tam_bloque)

        # Buscar el bloque en la cache
        for i in range(self.num_vias):
            if self.cache[indice][i]['valido'] and self.cache[indice][i]['etiqueta'] == etiqueta:
                # Hit: el bloque se encuentra en la cache
                self.hits += 1
                return self.cache[indice][i]['datos']

        # Miss: el bloque no se encuentra en la cache, se debe cargar desde la RAM
        self.misses += 1

        # Seleccionar aleatoriamente una via para el reemplazo
        via_reemplazo = random.randrange(self.num_vias)

        # Verificar si el bloque a reemplazar ha sido modificado
        if self.cache[indice][via_reemplazo]['valido'] and self.cache[indice][via_reemplazo]['modificado']:
            # Es necesario escribir el bloque de vuelta a la RAM antes de reemplazarlo
            dir_ram = self.cache[indice][via_reemplazo]['etiqueta'] * self.num_sets * self.tam_bloque + indice * self.tam_bloque
            self.ram.escribir_bloque(dir_ram, self.cache[indice][via_reemplazo]['datos'])

        # Cargar el bloque desde la RAM
        dir_ram = etiqueta * self.num_sets * self.tam_bloque + indice * self.tam_bloque
        datos = self.ram.leer_bloque(dir_ram, self.tam_bloque)

        # Actualizar la cache
        self.cache[indice][via_reemplazo]['valido'] = True
        self.cache[indice][via_reemplazo]['modificado'] = False
        self.cache[indice][via_reemplazo]['etiqueta'] = etiqueta
        self.cache[indice][via_reemplazo]['datos'] = datos

        return datos
