import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

from core.models import AudioTrack
from services.audio_probe import probe_audio
from utils.filename_parser import parse_filename


AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".aac"}


class AudioCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Check")
        self.geometry("800x450")
        self._create_widgets()

    def _create_widgets(self):
        btn = ttk.Button(self, text="Выбрать папку", command=self.select_folder)
        btn.pack(padx=10, pady=10)

        columns = ("number", "title", "format", "duration", "bitrate")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("number", text="№")
        self.tree.heading("title", text="Название")
        self.tree.heading("format", text="Формат")
        self.tree.heading("duration", text="Длительность")
        self.tree.heading("bitrate", text="Битрейт")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.tree.delete(*self.tree.get_children())

        for path in Path(folder).iterdir():
            if path.suffix.lower() not in AUDIO_EXTENSIONS:
                continue

            number, title = parse_filename(path)
            track = AudioTrack(path=path, number=number, title=title)

            probe_audio(track)

            self.tree.insert(
                "",
                tk.END,
                values=(
                    track.number,
                    track.title,
                    track.audio_format,
                    f"{track.duration:.2f}" if track.duration else "",
                    track.bitrate or ""
                )
            )
