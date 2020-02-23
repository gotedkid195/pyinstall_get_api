# Pyinstall get APIs
Python/Tkinter desktop GUI app to retrieve data returned via APIs. This app uses Sqlite3 to store data.

## Install dependencies
- [Python 3.7.0 ](https://www.python.org/downloads/release/python-370/)
- [Pipenv](https://pypi.org/project/pipenv/)

## Compile and run python script on Ubuntu
```bash
cd pyinstall_get_api/
pipenv shell
pipenv install
python main.py
```

## Use pyinstaller to build the app on Windows
- Git clone source
- Install python 3.7.0 [Windows x86-64 executable installer ](https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe) 
- Install pipenv
```bash
python -m pip install pipenv
```
- cd pyinstall_get_api/
- Install library
```bash
pipenv shell
pipenv install
python -m pip install pyinstaller
```
- Build app
```bash
pyinstaller --onefile --windowed main.py
```

## Use pyinstaller to build the app on Mac
```bash
pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' main.py
```

## License
- [MIT](https://choosealicense.com/licenses/mit/)
- Version: 1.0.0
- Author: Canh Nguyen
