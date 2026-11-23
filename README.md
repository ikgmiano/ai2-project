## setup instructions

### 1. clone the repo
```
git clone https://github.com/ikgmiano/ai2-project.git
cd ai2-project
```

### 2. create python virtual environemnt (venv)
```
python -m venv .venv
```

### 3. activate venv
- Windows (CMD):
```
.venv\Scripts\activate
```
- Windows (PowerShell):
```
.venv\Scripts\Activate.ps1
```
- Mac / Linux:
```
source .venv/bin/activate
```

### 4. install dependencies
```
pip install -r requirements.txt
```

## contributing
Follow the steps when working on a task to avoid merge conflicts:

### 1. get latest changes
Before working, pull latest change to main first.
```
git checkout main
git pull origin main
```

### 2. create new branch for your task
Don't push directly to main (blocked), create a branch named after what you're working on.
```
git checkout -b feature/your-task-name
```

### 3. update requirements.txt (only if you installed new packages)
If you ran `pip install <package>` while working, update `requirements.txt` before committing so the rest can get it:
```
pip freeze > requirements.txt
```

### 4. pushing
```
git add .
git commit -m "concise description of what you did"
git push -u origin feature/your-task-name
```

### 5. open Pull Request (PR)
1. go to the repo on GitHub
2. Click **Compare & pull request** for you branch (or navigate to **Pull requests** tab if it's not showing and create one there)
3. ask group to review nad merge it into `main`


## notes
1. never commit .venv or huge datasets
2. pull before creating your branch
3. you can delete .gitkeep when working on empty directories, I added that to push the directories.