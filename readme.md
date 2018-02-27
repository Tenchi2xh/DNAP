
<h1>
    <img src=resources/icon/color/256.png width=128 height=128 />
    <br/>
    DNAP<sup>*</sup>
</h1>

Keep track of new vinyl albums releases, hassle-free.

_DISCLOSURE: The author is not responsible any damages caused to your wallet_ 😉

What does it do?

- Uses web crawlers to periodically **check for new releases** on select labels
- Fires native OS **notifications** when new releases are scraped
- **Browse** all previously scraped titles with links to the store

<img width="1120" alt="dnap" src="https://user-images.githubusercontent.com/4116708/36647147-7b174f48-1a81-11e8-9852-e84662fbdcf4.png">

<p align=center><i>Never miss new releases from your favorite labels anymore!</i></p>

Supported labels:

[Black Screen Records](http://blackscreenrecords.limitedrun.com), [DATA DISCS](https://data-discs.com/collections/all), [Fangamer](https://www.fangamer.com/collections/music), [iam8bit](https://store.iam8bit.co.uk/collections/vinyl),
<br> [Laced Records](https://www.lacedrecords.co/collections/vinyl), [Minority Records](https://www.minorityrecords.com/en/releases), [Mondo](https://mondotees.com/collections/music), [Ship to Shore PhonoCo.](https://www.shiptoshoremedia.com/store),
<br> [The Yetee](https://theyetee.com/collections/all/Music), [ThinkGeek](https://www.thinkgeek.com/collectibles/vinyl-records), [Turntable Lab](https://www.turntablelab.com/collections/vinyl-cds-date)

---

## Contents

- [Usage](#usage)
    - [Download](#download)
    - [Run from source](#run-from-source)
- [Building](#building)
    - [Mac](#mac)
    - [Windows](#windows)
- [Attribution](#attribution)

## Usage

### Download

Download and launch the application from the [releases](https://github.com/Tenchi2xh/DNAP/releases) page.

When using the standalone application, logs are written in `~/.dnap/dnap.log` instead of `stdout`.

### Run from source

Install dependencies using the requirements file relevant to your operating system:

```bash
pip3 install -r requirements_macos.txt
```

To install the dependencies on Linux, [follow these instructions](readme_linux.md)

Run the application as a module:

```bash
python3 -m dnap
```

## Building

Common dependencies:

```bash
pip3 install requirements_[macos|windows].txt
pip3 install pyInstaller
```

### Mac

Just run `build_macos.sh`

### Windows

The [Visual C++ Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools) are required for some of the dependencies.

If you want an icon to be generated for the executable, you will need to install [ImageMagick](https://www.imagemagick.org/script/download.php#windows). Install using the option `Install legacy utilities`.

Then, run `build_windows.bat`

## Attribution

- Tray icon made by [Those Icons](https://thoseicons.com/) from www.flaticon.com (CC 3.0 BY)
- Application icon made by [Freepik](http://www.freepik.com") from www.flaticon.com (CC 3.0 BY)

*<sub>Does Not Affect Purchase</sub>
