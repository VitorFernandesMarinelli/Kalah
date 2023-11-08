import tkinter as tk
import cv2
from PIL import Image, ImageTk
from enum import Enum
import keyboard
import threading
import Audio

class videos(Enum):
    abertura = "abertura.mp4"
    titulo = "telaAbertura.mp4"
    trasicaoTituloMenu = "transicaoAberturaMenu.mp4"
    menu = "menu.png"
    trasicaoMenuConfi = "TransicaoMenuConfig.mp4"
    config = "config.png"
    trasicaoConfiMenu = "TransicaoConfigMenu.mp4"
    trasicaoMenuCredi = "TransicaoMenuCreditos.mp4"
    creditos = "Creditos.png"
    trasicaoCrediMenu = "TrasincaoCreditosMenu.mp4"
    trasicaoMenuJogo = "TransicaoMenuJogo.mp4"
    telaJogo = "mesaJogo.png"
    trasicaoJogoMenu = "TransicaoJogoMenu.mp4"



telaAtual = "Abertura"
isLoop = False
janela = tk.Tk() #janela

#tratamento de video
class VideoPlayer(tk.Frame):
    def __init__(self, video_source="", master=None):
        #'cria" o video
        global isLoop, telaAtual
        super().__init__(master)
        self.master = master
        self.pack()
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        self.loop = isLoop
        # Obtenha a taxa de quadros do vídeo (fps)
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        # Adiciona o video na janela
        self.canvas = tk.Canvas(self, width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Otmiza a reprodução
        self.delay = int(1000 / self.fps)
        # Faz a fução ficar sendo chamado na trhead principal em loop
        self.after(self.delay, self.update)

    def update(self):
        # Verifica se acabou o video e se tem que coloca-lo em loop
        ret, frame = self.vid.read()
        if not ret: #se video acabou
            if self.loop:
                self.vid.release()
                self.vid = cv2.VideoCapture(self.video_source)
                ret, frame = self.vid.read()  
            if not ret:
                proximo()
                return
        else: #se não acabou ele le frame por frame e mostra na tela (reproduz o video)
            verificador()
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Redimensiona a imagem com base no tamanho do canvas
            img = img.resize((self.canvas.winfo_width(), self.canvas.winfo_height()))

            self.photo = ImageTk.PhotoImage(image = img)
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

        #Faz a fução ficar sendo chamado na trhead principal em loop
        self.after(self.delay, self.update)


def play_video(caminho_video):
    #recbe um caminho e manda para gerar um video
    global janela
    limpaTela()
    VideoPlayer(caminho_video, janela)


def adicionar_imagem(caminho_imagem):
    global janela
    # Abre a imagem
    img = Image.open(caminho_imagem)

    # Redimensiona a imagem para caber na tela
    img = img.resize((1250, 600))

    # Converte a imagem para um formato Tkinter pode usar
    foto = ImageTk.PhotoImage(img)

    # Cria um label para a imagem e adiciona à janela
    label_imagem = tk.Label(janela, image = foto)
    label_imagem.image = foto  # Mantém uma referência da imagem
    label_imagem.pack()  # Posiciona a imagem na janela

def botoeCredito():
    global janela
    voltar = tk.Button(janela, text="voltar", command=botaovoltar, width=50, height=2)
    voltar.place(x=480,y=350)

def botoesJogar():
    global janela
    voltar = tk.Button(janela, text="pausar", command=Pausa, width=10, height=2)
    voltar.place(x=5,y=5)

def botoesMenu():
    global janela
    imagem_original = Image.open("engrenagem.png")
    imagem_redimensionada = imagem_original.resize((150, 130))
    imagem_botao = ImageTk.PhotoImage(imagem_redimensionada)
    canvas  = tk.Canvas(janela, width=150, height=130)
    Jogar = tk.Button(janela, text="jogar", command=botaoJogar, width=50, height=5)
    Creditos = tk.Button(janela, text="creditos", command=botaoCreditos, width=50, height=5)
    canvas.imagem_botao = imagem_botao
    canvas.create_image(0,0,anchor= 'nw', image = canvas.imagem_botao)
    canvas.bind("<Button-1>", botaoConfig)
    # Configura posição do Label
    canvas.place(x=30, y=100)
    Jogar.place(x=480,y=200)
    Creditos.place(x=480,y=300)

def botoesConfig():
    global janela
    voltar = tk.Button(janela, text="voltar", command=botaovoltarConfig, width=50, height=4)
    voltar.place(x=340,y=450)
    slider = tk.Scale(janela, from_=0, to=1, resolution=0.01, orient='horizontal', command=Audio.ajustar_volume, length=170)
    slider.set(Audio.getVolumeAtual())  # Definir o valor inicial
    slider.place(x=450, y=295)  # Definir a posição do slider

def limpaTela():
    global janela
    for widget in janela.winfo_children():
        widget.destroy() #limpa a janela para poder colocar outro video

def criar_janela():
    global janela
    #Configuração da janela
    janela.title("Kalah")
    janela.geometry("1250x600")
    janela.resizable(False, False)
    #Verifica se a janela foi fechada
    def on_close():
        Audio.desligarSom()
        janela.destroy()  #Destroi a janela
    #Configura o protocolo WM_DELETE_WINDOW para chamar a função on_close
    janela.protocol("WM_DELETE_WINDOW", on_close)
    janela.mainloop()
    
def botaoCreditos():
    global telaAtual
    telaAtual = "TrasCred"
    play_video(videos.trasicaoMenuCredi.value)

def botaoJogar():
    global telaAtual
    telaAtual = "TransJogo"
    play_video(videos.trasicaoMenuJogo.value)

def botaoConfig(event):
    global telaAtual
    telaAtual = "TransConf"
    play_video(videos.trasicaoMenuConfi.value)

def botaovoltar():
    global telaAtual
    telaAtual = "TransMenu"
    play_video(videos.trasicaoCrediMenu.value)


def botaovoltarConfig():
    global telaAtual
    telaAtual = "TransMenu"
    play_video(videos.trasicaoConfiMenu.value)

def proximo():
    global telaAtual, isLoop
    if telaAtual == "Abertura":
        telaAtual = "Titulo"
        isLoop = True
        Audio.setIsMusicaPrincipal()
        play_video(videos.titulo.value)
    elif telaAtual == "TransMenu":
        telaAtual = "Menu"
        limpaTela()
        adicionar_imagem(videos.menu.value)
        botoesMenu()
    elif telaAtual == "TrasCred":
        isLoop =False
        telaAtual = "credito"
        limpaTela()
        adicionar_imagem(videos.creditos.value)
        botoeCredito()
    elif telaAtual == "TransConf":
        telaAtual = "config"
        limpaTela()
        adicionar_imagem(videos.config.value)
        botoesConfig()
    elif telaAtual == "TransJogo":
        telaAtual = "Jogo"
        limpaTela()
        adicionar_imagem(videos.telaJogo.value)
        botoesJogar()

def verificador():
    global telaAtual
    if telaAtual == "Titulo":
        keyboard.on_press(TituloMenu)
    
def TituloMenu(evento):
    global telaAtual, isLoop
    if telaAtual == "Titulo":
        telaAtual =  "TransMenu"
        isLoop = False
        play_video(videos.trasicaoTituloMenu.value)

def botao2_click(popup):
    global telaAtual
    telaAtual = "TransMenu"
    popup.destroy()
    VideoPlayer(videos.trasicaoConfiMenu.value)

def Pausa():
    def botao1_click():
        popup.destroy()
    popup = tk.Tk()
    popup.wm_title("Pausa")
    
    label = tk.Label(popup, text="Jogo Pausado")
    label.pack(side='top', fill='x', pady=10)
    
    botao1 = tk.Button(popup, text="retomar", command=botao1_click)
    botao1.pack()
    
    botao2 = tk.Button(popup, text="menu", command=botao2_click(popup))
    botao2.pack()
    
    popup.mainloop()

threadAudio = threading.Thread(target=Audio.gerenteAudio)
threadAudio.start()
play_video(videos.abertura.value)
criar_janela()
threadAudio.join()


