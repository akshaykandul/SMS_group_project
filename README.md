# SMS_group_project

## Installation
Pre-requisite: python3.5

#### Steps:
- `pip install virtualenv`
- `virtualenv webappenv`
- `source mypython/bin/activate`
- `pip install -r requirements.txt` 

## Database Initialization
Initialize SQLite db using this command `python sql_lite_initiliazer.py`. 
This will initialize the SQLite with local db by creating a "local.db" file.

## Run the application 
`python app.py --port=<port_number>`

Above command starts the webapplication and binds with the mentioned port to listen. 

Note: If options `--port` is not provided the application will start the server with 8000 as default listening port.
