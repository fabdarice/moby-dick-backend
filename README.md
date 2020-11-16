# Requirements
* Python3
* Postgres
* Redis
* .envrc (direnv allow)
    * export ETHERSCAN_API_KEY=[ETHERSCAN_API_KEY]
    * export DATABASE_URL=postgres://[USER]:[PASSWORD]@[IP]:[PORT]/[DATABASE]
    * export REDIS_URL=redis://[IP]:[PORT]
    * export PYTHON_PATH=`pwd`
    * export GETH_WS_URI=[GETH_WEBSOCKET_NODE]
    * export TWILIO_ACCOUNT_SID=[TWILIO_ACCOUNT_SID]
    * export TWILIO_AUTH_TOKEN=[TWILIO_AUTH_TOKEN]
    * export AGENT_PHONE_NUMBERS=[LIST OF PHONE NUMBERS COMMA SEPARATED]
    * export TWILIO_FROM_NUMBER=[TWILIO_FROM_NUMBER]

# Installation
* virtualenv build
* source build/bin/activate
* ./start.sh


# Endpoints
* POST /tokens
    * Create tokens and fetch (celery) all top hodlers
* GET /tokens
    * Fetch all supported Tokens
* GET /hodlers?token=[TOKEN]&limit=[LIMIT]
    * Fetch top hodlers for a token - Limit (Default: top 100)
