export FLASK_APP=app.py

pkill flask

rm test.log

nohup flask run --host=0.0.0.0 --port=5443 &> test.log &
