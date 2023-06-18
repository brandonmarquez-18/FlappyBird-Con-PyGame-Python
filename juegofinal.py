import random 
import sys
import pygame
from pygame.locals import * 
# variables globales para el sistema
FPS = 32
ANCHO = 289
ALTO = 511
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
TERRENO = ALTO * 0.8
MULTIMEDIA = {}
SONIDOS = {}
JUGADOR = 'ajolote.png'
FONDO = 'fondo.png'
BOBCHOLO = 'bob.jpg'
def saludoPANTALLA():
    """
    muestra el saludo en la pantalla
    """
    JUGADORx = int(ANCHO/5)
    JUGADORy = int((ALTO - MULTIMEDIA['JUGADOR'].get_height())/2)
    imboxx = int((ANCHO - MULTIMEDIA['imbox'].get_width())/2)
    imboxy = int(ALTO*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # cerrar el juego
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # inicio de juego
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                PANTALLA.blit(MULTIMEDIA['FONDO'], (0, 0))    
                PANTALLA.blit(MULTIMEDIA['JUGADOR'], (JUGADORx, JUGADORy))    
                PANTALLA.blit(MULTIMEDIA['imbox'], (imboxx,imboxy ))    
                PANTALLA.blit(MULTIMEDIA['base'], (basex, TERRENO))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def mainGame():
    PUNTAJE = 0
    JUGADORx = int(ANCHO/5)
    JUGADORy = int(ANCHO/2)
    basex = 0
    # crea los obstaculos dentro del mapa
    newBOBCHOLO1 = getRandomBOBCHOLO()
    newBOBCHOLO2 = getRandomBOBCHOLO()
    # obstaculos superiores
    upperBOBCHOLOs = [
        {'x': ANCHO+200, 'y':newBOBCHOLO1[0]['y']},
        {'x': ANCHO+200+(ANCHO/2), 'y':newBOBCHOLO2[0]['y']},
    ]
    # obstaculos inferiores
    lowerBOBCHOLOs = [
        {'x': ANCHO+200, 'y':newBOBCHOLO1[1]['y']},
        {'x': ANCHO+200+(ANCHO/2), 'y':newBOBCHOLO2[1]['y']},
    ]
    BOBCHOLOVelX = -4
    JUGADORVelY = -9
    JUGADORMaxVelY = 10
    JUGADORMinVelY = -8
    JUGADORAccY = 1
    JUGADORFlapAccv = -8 # velocidad volando
    JUGADORFlapped = False 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if JUGADORy > 0:
                    JUGADORVelY = JUGADORFlapAccv
                    JUGADORFlapped = True
                    SONIDOS['xd'].play()
        colision = isCollide(JUGADORx, JUGADORy, upperBOBCHOLOs, lowerBOBCHOLOs)
        if colision:
            return     
        # el puntaje
        JUGADORMidPos = JUGADORx + MULTIMEDIA['JUGADOR'].get_width()/2
        for BOBCHOLO in upperBOBCHOLOs:
            BOBCHOLOMidPos = BOBCHOLO['x'] + MULTIMEDIA['BOBCHOLO'][0].get_width()/2
            if BOBCHOLOMidPos<= JUGADORMidPos < BOBCHOLOMidPos +4:
                PUNTAJE +=1
                print(f"Tu puntaje es: {PUNTAJE}") 
                SONIDOS['punto'].play()
        if JUGADORVelY <JUGADORMaxVelY and not JUGADORFlapped:
            JUGADORVelY += JUGADORAccY
        if JUGADORFlapped:
            JUGADORFlapped = False            
        JUGADORHeight = MULTIMEDIA['JUGADOR'].get_height()
        JUGADORy = JUGADORy + min(JUGADORVelY, TERRENO - JUGADORy - JUGADORHeight)
        for upperBOBCHOLO , lowerBOBCHOLO in zip(upperBOBCHOLOs, lowerBOBCHOLOs):
            upperBOBCHOLO['x'] += BOBCHOLOVelX
            lowerBOBCHOLO['x'] += BOBCHOLOVelX
        # añade obstaculos nuevos mientras se superan los otros
        if 0<upperBOBCHOLOs[0]['x']<5:
            newBOBCHOLO = getRandomBOBCHOLO()
            upperBOBCHOLOs.append(newBOBCHOLO[0])
            lowerBOBCHOLOs.append(newBOBCHOLO[1])
        # eliminar obstaculos que salen de la pantalla
        if upperBOBCHOLOs[0]['x'] < -MULTIMEDIA['BOBCHOLO'][0].get_width():
            upperBOBCHOLOs.pop(0)
            lowerBOBCHOLOs.pop(0)
        PANTALLA.blit(MULTIMEDIA['FONDO'], (0, 0))
        for upperBOBCHOLO, lowerBOBCHOLO in zip(upperBOBCHOLOs, lowerBOBCHOLOs):
            PANTALLA.blit(MULTIMEDIA['BOBCHOLO'][0], (upperBOBCHOLO['x'], upperBOBCHOLO['y']))
            PANTALLA.blit(MULTIMEDIA['BOBCHOLO'][1], (lowerBOBCHOLO['x'], lowerBOBCHOLO['y']))
        PANTALLA.blit(MULTIMEDIA['base'], (basex, TERRENO))
        PANTALLA.blit(MULTIMEDIA['JUGADOR'], (JUGADORx, JUGADORy))
        nmeros = [int(x) for x in list(str(PUNTAJE))]
        width = 0
        for valores2 in nmeros:
            width += MULTIMEDIA['valores'][valores2].get_width()
        Xoffset = (ANCHO - width)/2

        for valores2 in nmeros:
            PANTALLA.blit(MULTIMEDIA['valores'][valores2], (Xoffset, ALTO*0.12))
            Xoffset += MULTIMEDIA['valores'][valores2].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(JUGADORx, JUGADORy, upperBOBCHOLOs, lowerBOBCHOLOs):
    if JUGADORy> TERRENO - 25  or JUGADORy<0:
        SONIDOS['golpe'].play()
        return True    
    for BOBCHOLO in upperBOBCHOLOs:
        BOBCHOLOHeight = MULTIMEDIA['BOBCHOLO'][0].get_height()
        if(JUGADORy < BOBCHOLOHeight + BOBCHOLO['y'] and abs(JUGADORx - BOBCHOLO['x']) < MULTIMEDIA['BOBCHOLO'][0].get_width()):
            SONIDOS['golpe'].play()
            return True
    for BOBCHOLO in lowerBOBCHOLOs:
        if (JUGADORy + MULTIMEDIA['JUGADOR'].get_height() > BOBCHOLO['y']) and abs(JUGADORx - BOBCHOLO['x']) < MULTIMEDIA['BOBCHOLO'][0].get_width():
            SONIDOS['golpe'].play()
            return True
    return False
def getRandomBOBCHOLO():
    """
    genera las posiciones de los obstaculos de manera aleatoria
    """
    BOBCHOLOHeight = MULTIMEDIA['BOBCHOLO'][0].get_height()
    offset = ALTO/3
    y2 = offset + random.randrange(0, int(ALTO - MULTIMEDIA['base'].get_height()  - 1.2 *offset))
    BOBCHOLOX = ANCHO + 10
    y1 = BOBCHOLOHeight - y2 + offset
    BOBCHOLO = [
        {'x': BOBCHOLOX, 'y': -y1},
        {'x': BOBCHOLOX, 'y': y2}
    ]
    return BOBCHOLO
if __name__ == "__main__":
    # punto de inicio del juego
    pygame.init() # inicializamos los modulos que creamos
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('ISW 3° "A"')
    MULTIMEDIA['valores'] = ( 
        pygame.image.load('ajolote.png').convert_alpha(),
        pygame.image.load('ajolote.png').convert_alpha(),
        pygame.image.load('ajolote.png').convert_alpha(),
        pygame.image.load('ajolote.png').convert_alpha(),
        pygame.image.load('ajolote.png').convert_alpha(),
        pygame.image.load('ajolote.png').convert_alpha(),
        pygame.image.load('ajolote.png').convert_alpha(),
        pygame.image.load('ajolote.png').convert_alpha(),
        pygame.image.load('ajolote.png').convert_alpha(),
        pygame.image.load('ajolote.png').convert_alpha(),
    )
    MULTIMEDIA['imbox'] =pygame.image.load('ajolote.png').convert_alpha()
    MULTIMEDIA['base'] =pygame.image.load('base.png').convert_alpha()
    MULTIMEDIA['BOBCHOLO'] =(pygame.transform.rotate(pygame.image.load(BOBCHOLO).convert_alpha(), 180), 
    pygame.image.load(BOBCHOLO).convert_alpha()
    )
    # sonidazos como no
    SONIDOS['muerte'] = pygame.mixer.Sound('muerte.wav')
    SONIDOS['golpe'] = pygame.mixer.Sound('golpe.wav')
    SONIDOS['punto'] = pygame.mixer.Sound('punto.mp3')
    SONIDOS['fiund'] = pygame.mixer.Sound('fiund.wav')
    SONIDOS['xd'] = pygame.mixer.Sound('xd.wav')
    MULTIMEDIA['FONDO'] = pygame.image.load(FONDO).convert()
    MULTIMEDIA['JUGADOR'] = pygame.image.load(JUGADOR).convert_alpha()
    while True:
        saludoPANTALLA() # muestra la upp
        mainGame() # el juego
