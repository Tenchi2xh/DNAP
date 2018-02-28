#!/bin/sh

./clean.sh

VERSION=${1:-0.0}

cat > entrypoint.py << EOF
from dnap.__main__ import main
main()
EOF

SCRAPY_PATH=$(python3 -c 'import os; import scrapy; print(os.path.dirname(scrapy.__file__))')

pyinstaller \
    --clean \
    --noupx \
    --onefile \
    --name DNAP \
    --add-data resources:resources \
    --add-data $SCRAPY_PATH:scrapy \
    --hidden-import email.mime \
    --hidden-import email.mime.multipart \
    --hidden-import email.mime.text \
    --hidden-import twisted.web.client \
    --hidden-import queuelib \
    --windowed \
    entrypoint.py

DESCRIPTION="Keep track of new vinyl albums releases, hassle-free"

cat > build/DNAP.desktop << EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=DNAP
Comment=$DESCRIPTION
Path=/usr/local/bin/
Exec=DNAP
Icon=/usr/share/icons/DNAP/DNAP.png
Terminal=false
Categories=Utility;Music;
EOF

cp resources/icon/color/128.png build/DNAP.png

package() {
    fpm -s dir \
        -t $1 \
        -n dnap \
        -p dist \
        -v "$VERSION" \
        -m "https://github.com/Tenchi2xh/DNAP" \
        --description "$DESCRIPTION" \
        ./dist/DNAP=/usr/local/bin/DNAP \
        ./build/DNAP.desktop=/usr/local/share/applications/DNAP.desktop \
        ./build/DNAP.png=/usr/share/icons/DNAP/DNAP.png
}

package deb
#package rpm

rm entrypoint.py
rm DNAP.spec
