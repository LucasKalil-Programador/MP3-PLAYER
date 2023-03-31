import threading
from os import listdir
from time import time_ns, sleep

from pygame import mixer
from pygame.mixer import Sound

mixer.init()


class MusicPlayer:
    def __init__(self, path: str):
        self.__musics: list[Sound] = []
        self.__musics_names: list[str] = []
        self.__get_musics(path)

        self.__init_time, self.__pause_time, self.__music_index = 0, 0, 0
        self.__SECOND = 1000000000

    def __get_musics(self, path: str):
        def get_musics():
            for file in listdir(path):
                if file.count(".wav") | file.count(".mp3") | file.count(".ogg") == 1:
                    self.__musics.append(Sound(path + file))
                    self.__musics_names.append(file.split(".")[0])
        thread: threading.Thread = threading.Thread(target=get_musics, daemon=True)
        thread.start()

        while len(self.__musics_names) <= 0 and thread.is_alive():
            sleep(1)

    def play(self):
        self.stop()
        self.get_music().play()
        self.__init_time, self.__pause_time = time_ns(), 0

    def stop(self):
        for music in self.__musics:
            music.stop()

    def pause(self):
        mixer.pause()
        self.__pause_time = time_ns()

    def resume(self):
        mixer.unpause()
        self.__pause_sub_event()
        self.__pause_time = 0

    def __pause_sub_event(self):
        if self.__pause_time != 0:
            atu_time_ns = time_ns()
            self.__init_time += atu_time_ns - self.__pause_time
            self.__pause_time = atu_time_ns

    def next(self):
        index, music_list_size = self.__music_index, len(self.__musics)
        self.__music_index = 0 if index >= music_list_size - 1 else index + 1
        self.play()

    def previous(self):
        index, music_list_size = self.__music_index, len(self.__musics)
        self.__music_index = music_list_size - 1 if index <= 0 else index - 1
        self.play()

    def set_volume(self, value: float):
        for music in self.__musics:
            music.set_volume(value)

    def is_end(self):
        return self.get_frame() > self.get_length()

    def get_music_name(self):
        return self.__musics_names[self.__music_index]

    def get_musics_size(self):
        return len(self.__musics)

    def get_music(self):
        return self.__musics[self.__music_index]

    def get_length(self):
        return self.get_music().get_length()

    def get_frame(self):
        self.__pause_sub_event()
        music_frame = (time_ns() - self.__init_time + self.get_length()) / self.__SECOND
        return music_frame if music_frame >= 1 else 0
