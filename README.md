--python virtual env

py -3.9 -m venv env 
 env\Scripts\activate

 --Requirments
 pip install fastapi
 pip install uvicorn  --provide a server to run api

 --run api
 uvicorn main:app --reload

 -- query method
 get,post,delete,put
ex: http://amazon.com/iteam?q=jacket
q denode to query parameter

------------
 pip install sqlalchemy
----sync await sqlalch orm, sessions, core database file. getdb , test cases, test_client, pytese test client for session,

---------
pip install fastapi uvicorn jinja2
