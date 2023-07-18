# Widgets

Give immediate and accurate answers to common queries using widgets.

#### Installation

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

#### Usage

```bash
export FLASK_APP=serve.py; export FLASK_ENV=development; flask run
```

#### Structure 
```bash
+-- serve.py # entry to flask 
+-- gpt.py # utils for gpt
|   +-- widgets 
|   |   +-- core.py # core logic 
|   +-- prompts 
|   |   +-- classifier.yaml 
```
