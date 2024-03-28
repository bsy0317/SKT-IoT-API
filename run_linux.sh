#!/bin/bash
gunicorn -c gunicorn.conf.py smarthome:app