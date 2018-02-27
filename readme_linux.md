# DNAP on Linux

## Compiling dependencies

On most distributions that use `apt` as a package manager, installing the Python dependencies with `pip` will compile them. You will need the following dependencies to compile successfully:

```
sudo apt-get update
sudo apt-get install libnotify-dev libjpeg-dev libtiff-dev libgtk-3-dev freeglut3 freeglut3-dev libgstreamer-plugins-base1.0-dev libwebkit2gtk-4.0-dev libxtst-dev
pip3 install -r requirements.txt
```

## Debian binaries

If you don't want to compile, binaries exists on Debian. But they are as troublesome to use, as they are in the `testing` repository. Warning: this will also probably critically mess up) some of your other packages (Gnome depends on Python 3.5 for example).

DNAP needs wxPython 4 (Phoenix), which only exists in the `testing` repository and depends on Python 3.6, which is also only in the `testing` repository.

To add the `testing` repository to `apt`, add this to `/etc/apt/sources.list`:

```bash
# Replace 'nl' with your closest Debian mirror
deb http://ftp.nl.debian.org/debian/ testing main non-free contrib
deb-src http://ftp.nl.debian.org/debian/ testing main non-free contrib
```

To make sure `apt-get` will prioritize `stable` over `testing`, add these pinning settings to `/etc/apt/preferences`:

```
Package: *
Pin: release a=stable
Pin-Priority: 700

Package: *
Pin: release a=testing
Pin-Priority: 650
```

Then, run:

```bash
sudo apt-get update
sudo apt-get install libc-bin/testing \
                      python3/testing \
                      python3-sip/testing \
                      python3-pip/testing \
                      libwxbase3.0-0v5/testing \
                      libwxgtk3.0-0v5/testing \
                      python3-wxgtk4.0/testing \
                      python3-libxml2/testing \
                      python3-lxml/testing \
                      python3-twisted/testing \
                      python3-w3lib/testing \
                      python3-openssl/testing \
                      python3-parsel/testing \
                      python3-service-identity/testing \
                      python3-cryptography/testing \
                      python3-zope.interface/testing \
                      python3-twisted-bin/testing \
                      python3-cffi-backend/testing \
                      
pip3 install requests
```
