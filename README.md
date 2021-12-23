## Project  Description
	Video-Membership App Using Python, FastApi, Casandra(Using datastax)
	Live Link : ***

## Project Feature
	Later 

## Astradb Connect
	Download astradb connector from datastax
    rename the zipfile as astradb_connect.zip
    put it in app folder inside folder named unencrypted


## ENV VARIABLE
	Create a .env file & put these ENV variable value
	ASTRADB_KEYSPACE=***********
    ASTRADB_CLIENT_ID=***********
    ASTRADB_CLIENT_SECRET=***********

## To Run This Project
	Install all the dependencies  
	Create virtual env 
	python3 -m venv ./venv
	Activate venv 
	source venv/bin/activate
	pip install -r requirements.txt
	Run the app 
	uvicorn app.main:app --reload