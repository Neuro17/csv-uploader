# Note

This code has been tested with python 3.8

# How to run

1. install python requirements -> `cd backend; pip install -r requirements.txt; cd ..`
2. install npm requirements -> `npm install`
3. start the redis service with `docker run --name redis -d -p 6379:6379 redis`
4. start the frontend -> `npm start`
5. start the web server -> `cd backend; python main.py; cd ..`
6. start at least one worker -> `cd backend; arq worker.WorkerSettings; cd ..`
7. go to `localhost:3000` in your browser