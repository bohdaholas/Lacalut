## Description
The aim of the project is to make learning poems easier. The user dictates the chosen poem, and the app indentifies mistakes and gives voice hints. The app is written in Python, has a simple GUI and uses Google APIs for speech recognition and text synthesizing.

## Installation
```Bash
$ git clone https://github.com/bohdaholas/Lacalut.git
$ cd Lacalut
$ pip install -r requirements.txt
```
You also need to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the JSON file that contains your service account key. This variable only applies to your current shell session, so if you open a new session, set the variable again.
### Linux or macOS
```Bash
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```
### Windows
#### With PowerShell
```PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```
#### With command prompt
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=[PATH]
```

## Credits
Bohdan Ivashko, Yaroslav Moskalyk, Oleksiy Hoyev, Anna-Alina Bondarets, Mykhailo-Taras Sobko
Ukrainian Catholic University, Apllied Sciences Faculty, 2021

## License
MIT License
