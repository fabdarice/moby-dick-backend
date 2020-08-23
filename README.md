# Requirements
* Python3
* Postgres
* .envrc (direnv allow)
    * export DATABASE_URI=postgres://[USER]:[PASSWORD]@[IP]:[PORT]/[DATABASE]
    * export PYTHON_PATH=`pwd`
    * export INFURA_WS_URI=[INFURA_WEBSOCKET_NODE]

# Installation
* virtualenv build
* source build/bin/activate
* pip install -r requirements.txt
* make start
