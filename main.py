import pygame
import random
import math

pygame.init()

ancho_pantalla = 900
alto_pantalla = 700

pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Pac-Man")

NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

tamaño_celda = 47

pacman_imgs = [
    pygame.transform.scale(pygame.image.load('assets/player_images/policia.png'), (tamaño_celda, tamaño_celda)),
    pygame.transform.scale(pygame.image.load('assets/player_images/policia.png'), (tamaño_celda, tamaño_celda)),
    pygame.transform.scale(pygame.image.load('assets/player_images/policia.png'), (tamaño_celda, tamaño_celda)),
    pygame.transform.scale(pygame.image.load('assets/player_images/policia.png'), (tamaño_celda, tamaño_celda))
]

fantasma_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/ponchoRojo.png'), (tamaño_celda, tamaño_celda))
fantasma_muerto_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/dead.png'), (tamaño_celda, tamaño_celda))
fantasma_powerup_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/powerup.png'), (tamaño_celda, tamaño_celda))
cereza_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/cerveza.png'), (tamaño_celda, tamaño_celda)) 

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

pacman_x = 1 * tamaño_celda
pacman_y = 1 * tamaño_celda
velocidad_pacman = 0.5
direccion_pacman = None
direccion_proxima = None


indice_pacman = 0
reloj_pacman = 0

puntos = 0
vidas = 3

fantasmas = [
    {"x": 10 * tamaño_celda, "y": 10 * tamaño_celda, "velocidad": 0.5, "estado": "normal", "direccion": "izquierda"},
    {"x": 5 * tamaño_celda, "y": 5 * tamaño_celda, "velocidad": 0.5, "estado": "normal", "direccion": "derecha"},
    {"x": 15 * tamaño_celda, "y": 5 * tamaño_celda, "velocidad": 0.5, "estado": "normal", "direccion": "abajo"}
]

superpoder = False
duracion_superpoder = 800 

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
    if reloj_pacman % 10 == 0: 
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

# Función para mover fantasmas 
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

def mostrar_mensaje_perdida():
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 72)
    texto = fuente.render("¡Perdiste!", True, (255, 0, 0))
    pantalla.blit(texto, (ancho_pantalla // 2 - 150, alto_pantalla // 2 - 50))
    
    fuente_pequeña = pygame.font.SysFont(None, 48)
    
    boton_jugar_de_nuevo = pygame.Rect(ancho_pantalla // 2 - 150, alto_pantalla // 2 + 50, 300, 50)
    pygame.draw.rect(pantalla, (0, 200, 0), boton_jugar_de_nuevo)
    texto_jugar_de_nuevo = fuente_pequeña.render("Jugar de nuevo", True, (255, 255, 255))
    pantalla.blit(texto_jugar_de_nuevo, (ancho_pantalla // 2 - 110, alto_pantalla // 2 + 55))
    
    boton_cerrar = pygame.Rect(ancho_pantalla // 2 - 150, alto_pantalla // 2 + 110, 300, 50)
    pygame.draw.rect(pantalla, (200, 0, 0), boton_cerrar)
    texto_cerrar = fuente_pequeña.render("Cerrar", True, (255, 255, 255))
    pantalla.blit(texto_cerrar, (ancho_pantalla // 2 - 50, alto_pantalla // 2 + 115))

    pygame.display.update()

    esperando_respuesta = True
    while esperando_respuesta:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando_respuesta = False
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar_de_nuevo.collidepoint(evento.pos):
                    esperando_respuesta = False
                    reiniciar_juego()  
                elif boton_cerrar.collidepoint(evento.pos):
                    esperando_respuesta = False
                    pygame.quit()
                    exit()
                    
def reiniciar_juego():
    global pacman_x, pacman_y, direccion_pacman, direccion_proxima, puntos, vidas, fantasmas, superpoder, duracion_superpoder
    pacman_x, pacman_y = 1 * tamaño_celda, 1 * tamaño_celda
    direccion_pacman, direccion_proxima = None, None
    puntos = 0
    vidas = 3
    superpoder = False
    duracion_superpoder = 0
    
    fantasmas = [
        {"x": 10 * tamaño_celda, "y": 10 * tamaño_celda, "velocidad": 0.5, "estado": "normal", "direccion": "izquierda"},
        {"x": 5 * tamaño_celda, "y": 5 * tamaño_celda, "velocidad": 0.5, "estado": "normal", "direccion": "derecha"},
        {"x": 15 * tamaño_celda, "y": 5 * tamaño_celda, "velocidad": 0.5, "estado": "normal", "direccion": "abajo"}
    ]

    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[fila])):
            if laberinto[fila][columna] == " ":
                laberinto[fila][columna] = "."
            elif laberinto[fila][columna] == "C":
                pass  

def reproducir_musica_perdida():
    url_cancion = "perdida.mpeg" 
    pygame.mixer.music.load(url_cancion)
    pygame.mixer.music.play()

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

    if laberinto[int(pacman_y // tamaño_celda)][int(pacman_x // tamaño_celda)] == "C":
        superpoder = True
        duracion_superpoder = 800
        laberinto[int(pacman_y // tamaño_celda)][int(pacman_x // tamaño_celda)] = "."
        puntos += 100 
    
    if laberinto[int(pacman_y // tamaño_celda)][int(pacman_x // tamaño_celda)] == ".":
        laberinto[int(pacman_y // tamaño_celda)][int(pacman_x // tamaño_celda)] = " " 
        puntos += 10 

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

pygame.quit()
