# Steps:

1. Install (and update) VS Code (Visual Studio Code)
1. Install the latest Python 3.12
1. Install repo dependencies
    ```bash
    pip3.12 install -r requirements.txt
    ```
1. Install VS Code extensions (optional)
    ```bash
    cat vscode_extensions.txt | xargs -L 1 code --install-extension)
    ```
1. Run command line quiz
    ```bash
    python3.12 quiz_cmd.py
    ```
1. Run web UI
    ```bash
    python3.12 app.py
    ```

# Design:

1. [quiz_generator.py](quiz_generator.py) generates a data structure (list of dictionaries):

```JSON
questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Rome', 'Berlin'],
        'answer': 'Paris'
    },
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'answer': '4'
    },
    {
        'question': 'What is the capital of Italy?',
        'options': ['Madrid', 'Rome', 'Lisbon', 'Athens'],
        'answer': 'Rome'
    }
```

