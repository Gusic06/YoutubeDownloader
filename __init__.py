import PyInstaller.__main__

PyInstaller.__main__.run([
    'YoutubeDownloader.py',
    '--onefile',
    '-i=.\icon.ico'
])
