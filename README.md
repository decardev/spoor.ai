# Spoor.ai test task

## Commands used to init project

```console
poetry new spoor.ai
pyenv local 3.9.6
git init -b main
git add RADME.md && git commit -m "initial commit"
gh repo create

poetry install
poetry add black pre-commit typer opencv-python
poetry add @(parse-pip .\yolov3\requirements.txt) # custom command
touch .pre-commit-config.yaml
pre-commit install

```

## Brainstorming implementation

- Opencv creates jpg images from mp4
- yolov3 models jpg into pandas dataframe to export in csv
- pandas saves csv to sqlite
- peewee queries sqlite into matplotlib figure
- Everything should be managed with prefect task manager

## Problems with current implementation

As every block is working linearly and depends on execution of previous blocks to finish, the code is extremily inneficient.
Ways to mitigate such problem:

- Create a E-T-L workflow per unit of extraction.
- async extraction of frames from mp4 video into variables
- individual or grouped loading of frames to yolov3 model (depends on memory limits)
- async saving of yolov3 model into sqlite database
- result of all blocks is passed to the block creating graphs
