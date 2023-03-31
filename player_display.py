import sys
from time import strftime, gmtime

import pygame.display
from pygame import *
from pygame.event import Event

from music_player import MusicPlayer

from resources.resources_loader import *


def open_player_display(music_player: MusicPlayer):
    window = display.set_mode((400, 140))
    display.set_caption("Music Player (MP3 | WAV | OGG)")
    clock = time.Clock()
    music_player.play()
    pygame.init()

    play_pause_button = PlayPauseButtons((167.5, 20))
    next_prev_buttons = NextPrevButtons((51.5, 20))
    progress_statistics = ProgressStatistics()

    while True:
        if music_player.is_end():
            music_player.next()

        for e in event.get():
            play_pause_button.event_handler(e, music_player)
            next_prev_buttons.event_handler(e, music_player)
            if e.type == QUIT:
                sys.exit()

        window.fill("black")
        play_pause_button.render(window)
        next_prev_buttons.render(window)
        progress_statistics.render(window, music_player)

        pygame.display.flip()
        clock.tick(30)


class ProgressStatistics:
    def __init__(self):
        self.__font = pygame.font.SysFont("arial", 20)

    def render(self, window: Surface, music_player: MusicPlayer):
        time_str = strftime('%H:%M:%S', gmtime(music_player.get_frame()))
        window.blit(self.__font.render(time_str, True, "blue"), (5, 95))

        window.blit(progress_bar, (0, 120))
        progress = 400 * music_player.get_frame() // music_player.get_length()
        pygame.draw.rect(window, "black", (progress, 120, 400 - progress, 25))


class NextPrevButtons:
    def __init__(self, pos: (int, int)):
        self.__pos = pos

        self.next_rect: list[Rect] = [Rect(pos[0] + 291, pos[1] + 5, 6, 54)]
        self.prev_rect: list[Rect] = [Rect(pos[0], pos[1] + 5, 6, 54)]

        for i in range(8):
            self.prev_rect.append(Rect(pos[0] + 58 - 6 * i, pos[1] + 4 * i, 6, 64 - 8 * i))
            self.next_rect.append(Rect(pos[0] + 233 + 6 * i, pos[1] + 4 * i, 6, 64 - 8 * i))

    def render(self, window: Surface):
        window.blit(prev_icon, self.__pos)
        window.blit(next_icon, (self.__pos[0] + 233, self.__pos[1]))

    def event_handler(self, e: Event, music_player: MusicPlayer):
        if e.type == MOUSEBUTTONDOWN:
            for r in self.prev_rect:
                if r.collidepoint(mouse.get_pos()):
                    music_player.previous()
            for r in self.next_rect:
                if r.collidepoint(mouse.get_pos()):
                    music_player.next()


class PlayPauseButtons:
    def __init__(self, pos: (int, int)):
        self.__paused = False
        self.__pos = pos

        self.music = None
        self.__pause_rect: Rect = Rect(pos[0] + 9, pos[1], 46, 64)
        self.__play_rects: list[Rect] = []
        for i in range(8):
            rect_temp = Rect(pos[0], pos[1] + 8 * i, 18 * ((i + 1) if i < 4 else (8 - i)), 8)
            self.__play_rects.append(rect_temp)

    def render(self, window: Surface):
        window.blit(pause_icon if self.__paused else play_icon, self.__pos)

    def event_handler(self, e: Event, music_player: MusicPlayer):
        if e.type == MOUSEBUTTONDOWN:
            if not self.__paused:
                for r in self.__play_rects:
                    self.__paused = r.collidepoint(mouse.get_pos())
                    if self.__paused:
                        music_player.pause()
                        break
            elif self.__pause_rect.collidepoint(mouse.get_pos()):
                music_player.resume()
                self.__paused = False

        if music_player.get_music() != self.music:
            self.music = music_player.get_music()
            self.__paused = False
