from PySimpleGUI import *

from music_player import MusicPlayer


def ask_for_musics():
    tkinter.Tk().withdraw()
    return filedialog.askdirectory().replace("/", "\\") + "\\"


def request_client():
    theme("DarkBlue3")

    input_text = InputText(size=(35, 5), font=("ArialBlack", 14))
    button_browse = Button("Procurar arquivo", size=(25, 1), font=("ArialBlack", 14))

    error_text = Text("", size=(570, 0), font=("ArialBlack", 11), text_color="red")
    canvas = Canvas(size=(570, 20))

    button_open = Button("Carregar musicas", size=(25, 2), font=("ArialBlack", 14))
    button_cancel = Button("Cancelar", size=(25, 2), font=("ArialBlack", 14))

    layout = [[error_text], [input_text, button_browse], [canvas], [button_open, button_cancel]]
    window = Window("Escolha a pasta onde se encontra a musica", layout, size=(600, 160))

    while True:
        event, values = window.read()
        if event == WIN_CLOSED or event == "Cancelar":  # if user closes window or clicks cancel
            sys.exit()
        elif event == "Procurar arquivo":
            input_text.update(ask_for_musics())
        elif event == "Carregar musicas":
            if os.path.exists(input_text.get()):
                music_player = MusicPlayer(input_text.get())
                if music_player.get_musics_size() >= 1:
                    window.close()
                    return music_player
                else:
                    error_text.update("Não existem musicas nessa pasta")
            else:
                error_text.update("Arquivo não existe")
