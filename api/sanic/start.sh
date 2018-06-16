#!/bin/bash
gunicorn sample:app --bind localhost:8000 --worker-class sanic.worker.GunicornWorker --reload
