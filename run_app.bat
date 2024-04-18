@echo off

set ENV_DIR=ENV

if not exist %ENV_DIR% (
    echo Creating virtual environment...
    python -m venv %ENV_DIR%

    echo Activating virtual environment...
    call %ENV_DIR%\Scripts\activate

    echo Installing packages from requirements.txt...
    pip install -r requirements.txt
	echo "Install the required browsers (if they were not installed before that)"
	playwright install

    echo Ready! Virtual environment is set up.
) else (
    echo Virtual environment is already exists.
    echo Activating virtual environment...
    call %ENV_DIR%\Scripts\activate
)

echo Running the application...
python app.py
