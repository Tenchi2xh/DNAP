@echo off

call clean.bat

convert -version >nul 2>&1 && (
    mkdir build
    convert resources/icon/color/16.png ^
            resources/icon/color/24.png ^
            resources/icon/color/32.png ^
            resources/icon/color/64.png ^
            resources/icon/color/128.png ^
            resources/icon/color/256.png ^
            resources/icon/color/512.png ^
            build/DNAP.ico
    set ICON_OPTION=--icon build/DNAP.ico
) || (
    echo ImageMagick not installed, not generating icon
    set ICON_OPTION= ^

)

(
    echo from dnap.__main__ import main
    echo main(^)
) > "entrypoint.py"

for /f %%i in ('python -c "import os; import scrapy; print(os.path.dirname(scrapy.__file__))"') do set SCRAPY_PATH=%%i

pyinstaller ^
    --clean ^
    --noupx ^
    --onefile ^
    --name DNAP ^
    --add-data resources;resources ^
    --add-data %SCRAPY_PATH%;scrapy ^
    --hidden-import email.mime ^
    --hidden-import email.mime.multipart ^
    --hidden-import email.mime.text ^
    --hidden-import twisted.web.client ^
    --hidden-import queuelib ^
    --windowed ^
    %ICON_OPTION% ^
    entrypoint.py

rm entrypoint.py
rm DNAP.spec
