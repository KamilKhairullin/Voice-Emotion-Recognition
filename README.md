# Project on the course Lean Software Development BS18
Audio tracker team 1

## Install
1) Install python 3.8
2) Install poetry
- MacOS / Linux / Bash on Windows 
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
```

- Windows Powershell
```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python3 -
```
3) Install required packages
```shell
poetry install --no-dev
```

## Run
```shell
poetry run audio
```

## Team members
* Kamil Khayrullin
* Tagir Shigapov
* Aidar Garikhanov
* Alina Paukova
* Alexander Trushin
## Project description
We created an audio recorder with gui that is able to record audio, classify user's speech emotion.
