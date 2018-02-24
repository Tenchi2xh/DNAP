@echo off

call clean.bat

:: todo: generate .ico

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
    entrypoint.py

::     --icon build/DNAP.icns ^
rm entrypoint.py
rm DNAP.spec
