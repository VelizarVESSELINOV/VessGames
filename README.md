# Steps

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
1. Install tailwindcss
   ```bash
   npm install -D tailwindcss @tailwindcss/forms @tailwindcss/typography postcss autoprefixer prettier prettier-plugin-organize-attributes prettier-plugin-organize-imports prettier-plugin-tailwindcs
   npx tailwindcss init
   npx prettier . --write # added as a task
   npx tailwindcss -i ./src/input.css -o ./static/css/output.css --minify --watch # added as a task
   ```

# Design

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

# Architectural options

1. Minimal instance (low cost testing)

   ```mermaid
   flowchart TD

   U((User)):::user
   A{{Auth0 Google}}:::auth
   UI[/UI single-instance\]:::ui
   D[(local SQL Database: SQLite)]:::db
   B[(Database backup)]:::backup
   U <--> UI
   U <--> A
   UI <--> A
   UI <--> D
   D -.-> B

   classDef auth stroke:#f00
   classDef ui stroke:#0f0
   classDef user stroke:#00f
   classDef db stroke:pink
   classDef backup stroke:gray
   ```

1. Scalable solution: multi-UI instances, database as a service

   ```mermaid
   flowchart TD

   U((User)):::user
   A{{Auth0 Google}}:::auth
   UI[/UI multiple-instances\]:::ui
   D[(SQL Database as service: Vercel PostgreSQL)]:::db
   B[(Database backup)]:::backup
   U <--> UI
   U <--> A
   UI <--> A
   UI <--> D
   D -.-> B

   classDef auth stroke:#f00
   classDef ui stroke:#0f0
   classDef user stroke:#00f
   classDef db stroke:pink
   classDef backup stroke:gray
   ```
