#!/bin/bash

# build application execution file
pyinstaller --onedir app.py --noconsole

# create reports storage folder
mkdir ./dist/app/reports

# copy env variables to dist/app folder
# NOTE: add the env variables after building the app
cp -r .env.development ./dist/app/.env

# copy database to dist/app folder
cp -r ./database ./dist/app

# copy drivers to dist/app folder
cp -r ./drivers ./dist/app