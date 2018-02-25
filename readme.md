
<h1>
    <img src=resources/icon/color/256.png width=128 height=128 />
    <br/>
    DNAP<sup>*</sup>
</h1>

DISCLOSURE: The author is not responsible any damages caused to your wallet.

*<sub>Does Not Affect Purchase</sub>

## Usage

### Bundled

Download and launch the applications from the [releases](https://github.com/Tenchi2xh/DNAP/releases) page.

### Run from source

Install dependencies using the requirements file relevant to your operating system:

```bash
pip3 install -r requirements_macos.txt
```

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
