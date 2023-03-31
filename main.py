from file_choiser import request_client
from player_display import open_player_display

if __name__ == '__main__':
    while True:
        open_player_display(request_client())
