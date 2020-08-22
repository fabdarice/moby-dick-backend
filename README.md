# Requirements
* Python3
* .envrc (direnv allow)
    * export DATABASE_URI=postgres://[USER]:[PASSWORD]@[IP]:[PORT]/[DATABASE]
    * export PYTHON_PATH=`pwd`

# Installation
* virtualenv build
* source build/bin/activate
* pip install -r requirements.txt
* make start
