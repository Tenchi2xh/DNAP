## Debian setup

To run on Debian, DNAP needs wxPython 4 (Phoenix), which only exists in the `testing` repository and depends on Python 3.6, which is also only in the `testing` repository.

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
