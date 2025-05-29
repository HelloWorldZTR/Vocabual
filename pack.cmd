pyinstaller --add-data "bookdata;bookdata"  --add-data "settings;settings" --add-data "layouts/favico.png;layouts/favico.png" --icon "favico.ico" --collect-data pyecharts --noconsole .\main.py
if %errorlevel% neq 0 (
    echo "PyInstaller failed to build the executable."
    exit /b %errorlevel%
)
copy ffmpeg.exe dist\main\ffmpeg.exe
copy ffprobe.exe dist\main\ffprobe.exe
copy ffplay.exe dist\main\ffplay.exe