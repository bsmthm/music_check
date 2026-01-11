import subprocess
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".aac", ".mp4"}


def get_audio_info(file_path: Path) -> dict | None:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=bit_rate",
        "-show_entries", "format=duration",
        "-of", "json",
        str(file_path)
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError:
        return None

    data = json.loads(result.stdout)

    return {
        "duration": float(data["format"]["duration"]),
        "bitrate": int(data["streams"][0]["bit_rate"]) // 1000
    }

def parse_filename(file_path: Path) -> tuple[str, str]:
    name = file_path.stem

    if " " not in name:
        return "", name

    number, title = name.split(" ", 1)
    return number, title



class AudioCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Audio Checker")
        self.geometry("700x400")

        self._create_widgets()

    def _create_widgets(self):
        # Кнопка выбора папки
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        select_btn = ttk.Button(
            top_frame,
            text="Выбрать папку",
            command=self.select_folder
        )
        select_btn.pack(side=tk.LEFT)

        self.folder_label = ttk.Label(top_frame, text="Папка не выбрана")
        self.folder_label.pack(side=tk.LEFT, padx=10)

        # Таблица
        columns = ("number", "title", "format" ,"duration", "bitrate")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )

        self.tree.heading("number", text="№")
        self.tree.heading("title", text="Название")
        self.tree.heading("format", text="Расширение")
        self.tree.heading("duration", text="Длительность (сек)")
        self.tree.heading("bitrate", text="Битрейт (kbps)")

        self.tree.column("number", width=100, anchor=tk.CENTER)
        self.tree.column("title", width=300)
        self.tree.column("format", width=30)
        self.tree.column("duration", width=120, anchor=tk.CENTER)
        self.tree.column("bitrate", width=150, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Скроллбар
        scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.place(relx=1.0, rely=0.18, relheight=0.75, anchor="ne")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        folder_path = Path(folder)
        self.folder_label.config(text=str(folder_path))

        self._load_audio_files(folder_path)

    def _load_audio_files(self, folder: Path):
        self.tree.delete(*self.tree.get_children())

        audio_files = [
            p for p in folder.iterdir()
            if p.suffix.lower() in AUDIO_EXTENSIONS
        ]

        if not audio_files:
            messagebox.showinfo("Информация", "Аудиофайлы не найдены")
            return

        for audio_file in audio_files:
            info = get_audio_info(audio_file)
            if info is None:
                continue

            audio_format = audio_file.suffix.lstrip(".").lower()
            number, title = parse_filename(audio_file)

            self.tree.insert(
                "",
                tk.END,
                values=(
                    number,
                title,
                audio_format,
                f"{info['duration']:.2f}",
                info["bitrate"]
            )
    )



if __name__ == "__main__":
    app = AudioCheckerApp()
    app.mainloop()
