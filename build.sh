#!/bin/bash

# build application execution file
pyinstaller --onedir app.py --noconsole

# create reports storage folder
mkdir ./dist/app/reports

# copy env variables to dist/app folder
# NOTE: add the env variables after building the app
cp -r .env ./dist/app/.env

# copy database to dist/app/database folder
mkdir ./dist/app/database
cp ./database/database.xlsx ./dist/app/database/database.xlsx

# copy drivers to dist/app folder
cp -r ./drivers ./dist/app