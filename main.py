import tkinter as tk
from tkinter import filedialog
import pygame

class AudioPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Player")
        self.master.geometry("400x200")


        self.background_image = tk.PhotoImage(file="1.png")

        # Установка фона главного окна
        self.master.configure(bg="#cc9f66")
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Инициализация Pygame
        pygame.init()

        # Создание плеера
        self.player = None
        self.current_position = 0
        self.playing = False
        self.sound = None
        self.total_length = 0

        # Добавляем атрибут для отслеживания перемещения ползунка
        self.slider_moving = False

        self.error_label = tk.Label(self.master, text="", fg="red", bg="#cc9f66")
        self.error_label.pack(pady=10)

        # Создание ползунка прогресса
        self.progress_slider = tk.Scale(self.master, from_=0, to=100, orient="horizontal")
        self.progress_slider.pack(fill="x", padx=10)
        self.progress_slider.configure(troughcolor="gray", background="purple")


        self.initialize_gui()

        # Обновление позиции ползунка прогресса
        self.update_position()

    def initialize_gui(self):
        # Создание кнопок
        self.play_button = tk.Button(self.master, text="Play", fg="#000000", bg="#cc9f66", command=self.play)
        self.play_button.pack(pady=10)

        self.stop_button = tk.Button(self.master, text="Stop", fg="#000000", bg="#cc9f66", command=self.stop)
        self.stop_button.pack(pady=5)

        self.load_button = tk.Button(self.master, text="Load Audio", fg="#000000", bg="#cc9f66", command=self.load_audio)
        self.load_button.pack(pady=10)

        # Обработчики событий для отслеживания перемещения ползунка
        self.progress_slider.bind("<ButtonPress>", lambda e: self.slider_start_move())
        self.progress_slider.bind("<ButtonRelease>", self.slider_end_move)
        self.progress_slider.bind("<Motion>", self.slider_move)

    def slider_start_move(self):
        self.slider_moving = True

    def slider_end_move(self, event):
        try:
            if self.player:
                new_position = self.progress_slider.get()
                pygame.mixer.music.set_pos(new_position)  # Устанавливаем новую позицию воспроизведения музыки
                self.current_position = new_position * 1000  # Обновляем текущую позицию в миллисекундах
        except pygame.error as e:
            self.show_error(str(e))

    def slider_move(self, event):
        pass

    def play(self):
        try:
            if self.player and not self.playing:
                pygame.mixer.music.load(self.player)
                pygame.mixer.music.play(start=self.current_position)
                self.playing = True
            elif not self.player:
                raise pygame.error("No audio loaded")
            elif self.playing:
                raise pygame.error("Music is already playing")
        except pygame.error as e:
            self.show_error(str(e))

    def show_error(self, message):
        self.error_label.config(text=message)
        self.master.after(3000, self.hide_error)

    def hide_error(self):
        self.error_label.config(text="")

    def stop(self):
        try:
            if self.playing:
                pygame.mixer.music.stop()
                self.playing = False
                self.current_position = 0
        except pygame.error as e:
            self.show_error(str(e))

    def load_audio(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
            if file_path:
                self.player = file_path
                self.sound = pygame.mixer.Sound(file_path)
                self.total_length = self.sound.get_length()
                self.progress_slider.config(to=self.total_length)  # Устанавливаем максимальное значение ползунка
                self.update_position()
        except pygame.error as e:
            self.show_error(str(e))

    def set_position(self, value):
        try:
            if self.player and not self.slider_moving:  # Учитываем положение ползунка только если он не перемещается
                position = int(value) * self.total_length // 100
                self.current_position = position
        except pygame.error as e:
            self.show_error(str(e))

    def update_position(self):
        try:
            if self.playing and not self.slider_moving:
                position = pygame.mixer.music.get_pos() / 1000  # Позиция в секундах
                self.progress_slider.set(position)  # Устанавливаем позицию ползунка
            self.master.after(100, self.update_position)
        except pygame.error as e:
            self.show_error(str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayerApp(root)
    root.mainloop()
