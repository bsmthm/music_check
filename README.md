music_check/
├── main.py                     # точка входа
│
├── ui/
│   ├── __init__.py
│   └── app.py                  # Tkinter GUI
│
├── services/
│   ├── __init__.py
│   ├── audio_probe.py          # ffprobe: длительность, битрейт, каналы
│   ├── audio_analysis.py       # loudness, артефакты (to do)
│   └── audio_fix.py            # исправления (to do)
│
├── core/
│   ├── __init__.py
│   └── models.py               # AudioTrack, результаты анализа
│
└── utils/
    ├── __init__.py
    └── filename_parser.py      # разбор имени файла
