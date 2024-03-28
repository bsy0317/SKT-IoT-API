@echo off 
set cPath=%cd% 
waitress-serve --listen=0.0.0.0:5000 smarthome:app 