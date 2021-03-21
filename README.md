# Project on the course Lean Software Development BS18
Audio tracker team 1

## Install
1) Install [Python 3.8](https://www.python.org/downloads/)
2) Clone this repository and go to project folder
```shell
git clone https://github.com/KamilKhairullin/LeanSWDevelopement_team1.git
cd LeanSWDevelopement_team1
```
3) Install poetry
- MacOS / Linux / Bash on Windows 
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
(replace `python` with `python3` or `python3.8` if you have several python version)
- Windows Powershell
```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```
Note, you also might need to add `poetry` directory to `PATH` variable.
- Unix: `$HOME/.poetry/bin`
- Windows: `%USERPROFILE%\.poetry\bin`
4) Install required packages
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

## Change number of emotions
By default, there is a recognition of three emotions: sad, happy, neutral.
You can change the model to 2 emotions (sad and happy) by:
1. rename the file "model.pkl" to any name (example: "twoEmotions.pkl")
2. rename the file "twoEmotions.pkl" to "model.pkl"
3. rerun peogram by "poetry run audio"
