# JCloud Setup

1. Clone the Jcloud repo
   ```
   git clone https://github.com/joshanjohn/jcloud-pass.git
   ```

2. create a `.env` file and replace the values for variable provide in `.env.example` file.

    > Note you need to have following things:
    > - monogodb service running
    > - Firebase Authentication with email and password enabled. 
   
4. Start Azure Blob Service

   Since we are running azure service on docker and wanted to store data and logs of azure service, we need to create a *data* folder.

   ```
   cd jcloud-pass
   mkdir data
   ```

   I have provided a ```docker-compose.yml``` file so you only need to replace the file path for `data` and `.logs` folders.
   
     ```
      volumes:
        - /your/full/path/jcloud-pass/azure/data:/data
        - /your/full/path/CSP/jcloud-pass/.logs:/logs
     ```

    then, run the azure on docker using provided ```docker-compose.yml``` using: 

    ```
    docker-compose up -d 
    ```

5. Installing project dependencies
   We are using UV as dependency manager, which is very fast and written in RUST. Firstly, we need to sync the project

   install [UV](https://docs.astral.sh/uv/getting-started/installation/#pypi)

   - command to install uv using curl
      ```
      curl -LsSf https://astral.sh/uv/install.sh | sh
      ```
   - command to install uv using home brew (recommended)
      ```
      brew install uv
      ````

   sync the uv project.
   ```
   uv sync
   ```

   the sync command automatically create a python virtual environment in `.venv` folder.

   ```
   source .venv/bin/activate
   ```

# Run JCloud 
To run the JCloud services simply run the command from root folder. 

```
uv run python main.py
```
