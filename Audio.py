import pygame
import time
from enum import Enum

isMusicaPrincipal = False
isRodando = True
volumeAtual = 1

class musicas(Enum):
    abetura = "abertura.mp3"
    musica = "Sonata da fazenda.mp3"
    musicaLopp = "Sonata da fazenda (loop).mp3"

def getVolumeAtual():
    return volumeAtual

def ajustar_volume(volume):
    global volumeAtual
    novoVolume = float(volume)
    pygame.mixer.music.set_volume(novoVolume)
    volumeAtual = novoVolume


def setIsMusicaPrincipal():
    global isMusicaPrincipal
    isMusicaPrincipal = True

def desligarSom():
    global isRodando
    isRodando = False


def gerenteAudio():
    global isMusicaPrincipal
    time.sleep(1.5)
    tocar_musica(musicas.abetura.value)
    while isMusicaPrincipal == False:
        pass
    tocar_musica(musicas.musica.value)
    while isRodando == True:
        tocar_musica(musicas.musicaLopp.value)
    


def tocar_musica(caminho):
    # Inicialize o mixer de música do pygame
    pygame.mixer.init()
    # Carregar a música do caminho fornecido
    pygame.mixer.music.load(caminho)
    # Tocar a música
    pygame.mixer.music.play()
    verificar_musica()


def verificar_musica():
    global isRodando
    while pygame.mixer.music.get_busy() and isRodando == True:
        # A música ainda está tocando, então espere um pouco e verifique novamente
        time.sleep(1)
    print('A música acabou de tocar!')