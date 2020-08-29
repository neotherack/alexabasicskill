export FLASK_APP=app.py

pkill flask
pkill ngrok

rm test.log
rm ngrok.log

nohup flask run --host=0.0.0.0 --port=5443 &> test.log &
nohup ngrok http 5443 &> ngrok.log &
