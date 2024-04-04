# Behery's OCR App Backend

This is the backend for Behery's OCR App.
It is a REST API built using the fastapi framework.

## How to run


1. Make sure you have Python 3.8 or higher installed and that you have [pip](https://pip.pypa.io/en/stable/installing/) installed as well. You can check if you have Python installed by running the following command

    ```bash
    python3 --version
    pip --version
    ```

1. Clone the repository and make sure you are in the root directory of the project


1. Run the following command to create a virtual environment

    ```bash
    python3 -m venv myenv
    ```

1. Activate the virtual environment

    ```bash
    source myenv/bin/activate
    ```
    
    If you are on Windows, you will need to run the following command instead

    ```bash
    myenv\Scripts\activate
    ```

1. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

    If you have added a new dependency, make sure to update the `requirements.txt` file by running the following command

    ```bash
    pip freeze > requirements.txt
    ```

1. Create a `.env` file in the root directory of the project and add the variables listed in the [`.env.example`](.env.example) file

    ```bash
    cp .env.example .env
    ```


1. Run the server. the --reload flag is optional and is used to reload the server when a change is made (during development)

    ```bash
    uvicorn src.main:app --reload --port <port>
    ```


## Creating a new module

In order to enforce the folder structure, we have created a script that will create a new module for you. To run the script, run the following command

```bash
./create_module.sh <module_name>
```

If you are on Windows, you will either need to enable the Windows Subsystem for Linux then run the following command. Or if you are using Git Bash, you can run the previous command. 

```bash
bash create_module.sh <module_name>
```

This will create a new folder in the `src` directory with the name `<module_name>` along with its files.

You are welcome to create a new module manually, but make sure you follow the folder structure.

Note that u will need to include the new router in the `src/routes.py` file.

## Adding a new dependency

If you want to add a new dependency, make sure you add it to the `requirements.txt` file by running the following command

```bash
pip freeze > requirements.txt
```