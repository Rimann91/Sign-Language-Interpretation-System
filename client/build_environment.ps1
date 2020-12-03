Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
$python_path=$args[0]

# Build the virtual environment using provided python interpreter
Write-Host "createing virtual environment... "
& $python_path -m venv env

# ACtivate the virtual environment
.\env\Scripts\activate.bat

# install dependencies
pip install -r requirements.txt

Set-ExecutionPolicy Default -Scope CurrentUser