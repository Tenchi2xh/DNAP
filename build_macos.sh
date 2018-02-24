./clean.sh

mkdir -p build/DNAP.iconset
cp resources/icon/color/16.png  build/DNAP.iconset/icon_16x16.png
cp resources/icon/color/32.png  build/DNAP.iconset/icon_16x16@2x.png
cp resources/icon/color/32.png  build/DNAP.iconset/icon_32x32.png
cp resources/icon/color/64.png  build/DNAP.iconset/icon_32x32@2x.png
cp resources/icon/color/128.png build/DNAP.iconset/icon_128x128.png
cp resources/icon/color/256.png build/DNAP.iconset/icon_128x128@2x.png
cp resources/icon/color/256.png build/DNAP.iconset/icon_256x256.png
cp resources/icon/color/512.png build/DNAP.iconset/icon_256x256@2x.png
cp resources/icon/color/512.png build/DNAP.iconset/icon_512x512.png
iconutil -c icns --output build/DNAP.icns build/DNAP.iconset 2> /dev/null

cat > entrypoint.py << EOF
from dnap.__main__ import main
main()
EOF

pyinstaller \
    --clean \
    --noupx \
    --onefile \
    --name DNAP \
    --add-data resources:resources \
    --windowed \
    --icon build/DNAP.icns \
    --osx-bundle-identifier net.team2xh.dnap \
    entrypoint.py

plutil -insert NSHighResolutionCapable -string True dist/DNAP.app/Contents/Info.plist

rm entrypoint.py
rm DNAP.spec
