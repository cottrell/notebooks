pip install sanic
pip install -U sanic-cors
pip install sanic-gunicorn
# gunicorn --bind localhost:8000 --worker-class sanic_gunicorn.Worker your_app_module:app
pip install sanic-openapi
https://github.com/channelcat/sanic-openapi
python sample.py
# see /swagger
