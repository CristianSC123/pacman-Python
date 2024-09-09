import pygame
import random
import math

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
ancho_pantalla = 800
alto_pantalla = 600

# Creación de la pantalla
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Pac-Man")

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

# Tamaño de las celdas del laberinto
tamaño_celda = 40

# Carga de imágenes para la animación de Pac-Man
pacman_imgs = [
    pygame.transform.scale(pygame.image.load('assets/player_images/1.png'), (tamaño_celda, tamaño_celda)),
    pygame.transform.scale(pygame.image.load('assets/player_images/2.png'), (tamaño_celda, tamaño_celda)),
    pygame.transform.scale(pygame.image.load('assets/player_images/3.png'), (tamaño_celda, tamaño_celda)),
    pygame.transform.scale(pygame.image.load('assets/player_images/4.png'), (tamaño_celda, tamaño_celda))
]
# Carga de imágenes de los fantasmas y cereza
fantasma_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/blue.png'), (tamaño_celda, tamaño_celda))
fantasma_muerto_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/dead.png'), (tamaño_celda, tamaño_celda))
fantasma_powerup_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/powerup.png'), (tamaño_celda, tamaño_celda))
cereza_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/cherry.png'), (tamaño_celda, tamaño_celda))  # Placeholder para la imagen de la cereza

# Definición del laberinto (ahora una lista de listas para poder modificar)
laberinto = [
    list("*********************"),
    list("*.......*....C......*"),
    list("*.*.***.*.***.***.*.*"),
    list("*.*.............*.*.*"),
    list("*.*.***.*******.*.*.*"),
    list("*.....*.....*.....*.*"),
    list("*****.*.***.*.*******"),
    list("*.....*...*.*.....*.*"),
    list("*.*.*******.*.***.*.*"),
    list("*.*.*.........*.*...*"),
    list("*.*.***.*******.*.***"),
    list("*.*.....*.....*.*...*"),
    list("*.*******.*.*****.***"),
    list("*.........*....C....*"),
    list("*********************")
]

# Variables de posición y velocidad de Pac-Man
pacman_x = 1 * tamaño_celda
pacman_y = 1 * tamaño_celda
velocidad_pacman = 1
direccion_pacman = None
direccion_proxima = None

# Variables de animación de Pac-Man
indice_pacman = 0
reloj_pacman = 0

# Puntos
puntos = 0
vidas = 3

# Variables de los fantasmas
fantasmas = [
    {"x": 10 * tamaño_celda, "y": 10 * tamaño_celda, "velocidad": 1, "estado": "normal", "direccion": "izquierda"},
    {"x": 5 * tamaño_celda, "y": 5 * tamaño_celda, "velocidad": 1, "estado": "normal", "direccion": "derecha"},
    {"x": 15 * tamaño_celda, "y": 5 * tamaño_celda, "velocidad": 1, "estado": "normal", "direccion": "abajo"}
]

# Duración del superpoder
superpoder = False
duracion_superpoder = 800  # El superpoder dura 800 ciclos

# Función para dibujar el laberinto
def dibujar_laberinto():
    pantalla.fill(NEGRO)
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[fila])):
            if laberinto[fila][columna] == "*":
                pygame.draw.rect(pantalla, AZUL, (columna * tamaño_celda, fila * tamaño_celda, tamaño_celda, tamaño_celda))
            elif laberinto[fila][columna] == ".":
                pygame.draw.circle(pantalla, (255, 255, 255), (columna * tamaño_celda + tamaño_celda // 2, fila * tamaño_celda + tamaño_celda // 2), tamaño_celda // 10)
            elif laberinto[fila][columna] == "C":
                pantalla.blit(cereza_img, (columna * tamaño_celda, fila * tamaño_celda))

    # Dibujar Pac-Man
    pantalla.blit(pacman_imgs[indice_pacman], (pacman_x, pacman_y))
    
    # Dibujar Fantasmas
    for fantasma in fantasmas:
        if fantasma["estado"] == "normal":
            pantalla.blit(fantasma_img, (fantasma["x"], fantasma["y"]))
        elif fantasma["estado"] == "muerto":
            pantalla.blit(fantasma_muerto_img, (fantasma["x"], fantasma["y"]))
        elif fantasma["estado"] == "powerup":
            pantalla.blit(fantasma_powerup_img, (fantasma["x"], fantasma["y"]))

    # Dibujar puntaje y vidas
    fuente = pygame.font.SysFont(None, 36)
    texto_puntos = fuente.render(f'Puntos: {puntos}', True, (255, 255, 255))
    texto_vidas = fuente.render(f'Vidas: {vidas}', True, (255, 255, 255))
    pantalla.blit(texto_puntos, (10, 10))
    pantalla.blit(texto_vidas, (10, 50))
    
    pygame.display.update()

# Función para mover Pac-Man de manera continua
def mover_pacman():
    global pacman_x, pacman_y, direccion_pacman, direccion_proxima, indice_pacman, reloj_pacman
    if direccion_proxima and es_valido_movimiento(direccion_proxima, pacman_x, pacman_y):
        direccion_pacman = direccion_proxima
        direccion_proxima = None

    if direccion_pacman == "arriba" and es_valido_movimiento(direccion_pacman, pacman_x, pacman_y):
        pacman_y -= velocidad_pacman
    elif direccion_pacman == "abajo" and es_valido_movimiento(direccion_pacman, pacman_x, pacman_y):
        pacman_y += velocidad_pacman
    elif direccion_pacman == "izquierda" and es_valido_movimiento(direccion_pacman, pacman_x, pacman_y):
        pacman_x -= velocidad_pacman
    elif direccion_pacman == "derecha" and es_valido_movimiento(direccion_pacman, pacman_x, pacman_y):
        pacman_x += velocidad_pacman

    # Actualizar la animación de Pac-Man
    reloj_pacman += 1
    if reloj_pacman % 10 == 0:  # Cambiar la imagen cada 10 ciclos
        indice_pacman = (indice_pacman + 1) % 4

# Función para verificar si el movimiento es válido
def es_valido_movimiento(direccion, x, y):
    if direccion == "arriba":
        return laberinto[int((y - velocidad_pacman) // tamaño_celda)][int(x // tamaño_celda)] != "*"
    elif direccion == "abajo":
        return laberinto[int((y + tamaño_celda) // tamaño_celda)][int(x // tamaño_celda)] != "*"
    elif direccion == "izquierda":
        return laberinto[int(y // tamaño_celda)][int((x - velocidad_pacman) // tamaño_celda)] != "*"
    elif direccion == "derecha":
        return laberinto[int(y // tamaño_celda)][int((x + tamaño_celda) // tamaño_celda)] != "*"
    return False

# Función para mover fantasmas de manera más organizada
def mover_fantasmas():
    for fantasma in fantasmas:
        if superpoder and fantasma["estado"] != "muerto":
            fantasma["estado"] = "powerup"
        if not superpoder:
            fantasma["estado"] = "normal"

        direccion = fantasma["direccion"]
        if direccion == "arriba" and es_valido_movimiento(direccion, fantasma["x"], fantasma["y"]):
            fantasma["y"] -= fantasma["velocidad"]
        elif direccion == "abajo" and es_valido_movimiento(direccion, fantasma["x"], fantasma["y"]):
            fantasma["y"] += fantasma["velocidad"]
        elif direccion == "izquierda" and es_valido_movimiento(direccion, fantasma["x"], fantasma["y"]):
            fantasma["x"] -= fantasma["velocidad"]
        elif direccion == "derecha" and es_valido_movimiento(direccion, fantasma["x"], fantasma["y"]):
            fantasma["x"] += fantasma["velocidad"]
        else:
            # Cambiar dirección si choca con un muro
            fantasma["direccion"] = random.choice(["arriba", "abajo", "izquierda", "derecha"])

# Función para detectar colisiones entre Pac-Man y los fantasmas
def detectar_colisiones():
    global vidas, pacman_x, pacman_y
    for fantasma in fantasmas:
        distancia = math.sqrt((pacman_x - fantasma["x"])**2 + (pacman_y - fantasma["y"])**2)
        if distancia < tamaño_celda // 2:
            if fantasma["estado"] == "normal":
                vidas -= 1
                pacman_x, pacman_y = 1 * tamaño_celda, 1 * tamaño_celda  # Reiniciar Pac-Man
            elif fantasma["estado"] == "powerup":
                fantasma["estado"] = "muerto"
                fantasma["x"], fantasma["y"] = 10 * tamaño_celda, 10 * tamaño_celda  # Fantasma vuelve a la base

# Función para mostrar el mensaje de "Perdiste" con opciones
def mostrar_mensaje_perdida():
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 72)
    texto = fuente.render("¡Perdiste!", True, (255, 0, 0))
    pantalla.blit(texto, (ancho_pantalla // 2 - 150, alto_pantalla // 2 - 50))
    
    fuente_pequeña = pygame.font.SysFont(None, 48)
    boton_cerrar = pygame.Rect(ancho_pantalla // 2 - 150, alto_pantalla // 2 + 50, 300, 50)
    pygame.draw.rect(pantalla, (200, 0, 0), boton_cerrar)
    texto_cerrar = fuente_pequeña.render("Cerrar", True, (255, 255, 255))
    pantalla.blit(texto_cerrar, (ancho_pantalla // 2 - 50, alto_pantalla // 2 + 55))

    pygame.display.update()

    esperando_respuesta = True
    while esperando_respuesta:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando_respuesta = False
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_cerrar.collidepoint(evento.pos):
                    esperando_respuesta = False
                    pygame.quit()
                    exit()

# Función para reproducir música al perder todas las vidas
def reproducir_musica_perdida():
    url_cancion = "tu_url_de_la_cancion"  # Deja aquí la URL de la canción que quieres usar
    pygame.mixer.music.load(url_cancion)
    pygame.mixer.music.play()

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                direccion_proxima = "arriba"
            elif evento.key == pygame.K_DOWN:
                direccion_proxima = "abajo"
            elif evento.key == pygame.K_LEFT:
                direccion_proxima = "izquierda"
            elif evento.key == pygame.K_RIGHT:
                direccion_proxima = "derecha"

    mover_pacman()

    # Verificar si Pac-Man come una cereza
    if laberinto[int(pacman_y // tamaño_celda)][int(pacman_x // tamaño_celda)] == "C":
        superpoder = True
        duracion_superpoder = 800  # El superpoder dura 800 ciclos
        laberinto[int(pacman_y // tamaño_celda)][int(pacman_x // tamaño_celda)] = "."
        puntos += 100  # Sumar puntos por la cereza
    
    # Verificar si Pac-Man come un punto pequeño
    if laberinto[int(pacman_y // tamaño_celda)][int(pacman_x // tamaño_celda)] == ".":
        laberinto[int(pacman_y // tamaño_celda)][int(pacman_x // tamaño_celda)] = " "  # Vaciar la celda
        puntos += 10  # Sumar puntos por el punto pequeño

    mover_fantasmas()
    detectar_colisiones()

    if superpoder:
        duracion_superpoder -= 1
        if duracion_superpoder <= 0:
            superpoder = False

    dibujar_laberinto()

    if vidas == 0:
        reproducir_musica_perdida()
        mostrar_mensaje_perdida()
        ejecutando = False  # Fin del juego

pygame.quit()
