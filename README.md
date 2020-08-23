# Requirements
* Python3
* Postgres
* Redis
* .envrc (direnv allow)
    * export ETHERSCAN_API_KEY=[ETHERSCAN_API_KEY]
    * export DATABASE_URL=postgres://[USER]:[PASSWORD]@[IP]:[PORT]/[DATABASE]
    * export REDIS_URL=redis://[IP]:[PORT]
    * export PYTHON_PATH=`pwd`
    * export INFURA_WS_URI=[INFURA_WEBSOCKET_NODE]

# Installation
* virtualenv build
* source build/bin/activate
* ./start.sh 
