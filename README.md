## Installtion steps (One time setup)

We're using pipenv as a package manager

### Install pipenv

```
pip install pipenv
```

### Install project dependencies

```
pipenv install
```

### Change Python's interpreter path to detect packages (VSCODE users)

```
Open VSCODE & goto project's root directory
then Press : "Ctrl + Shift + P"
then Type : "Python Select Interpreter" (without double quotes)
then Select the Interpreter present in .venv folder
```

---

# Note: please make sure you're in the pipenv's shell environment before doing anything!!!

### To go in pipenv's shell environment

for vscode users shell environment will be automatically activated, I'd recommend always do it manually

```
pipenv shell
```

### To install packages

```
pipenv install <package_name>

Example: pipenv install PyQt5
```
