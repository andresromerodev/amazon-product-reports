#!/bin/bash

#######################################################
### USE THIS FILE TO CREATE A NEW APPLICATION BUILD ###
#######################################################

# remove old build
rm -r -f ./dist ./build

# build application execution file
pyinstaller --onedir app.py --noconsole

# create reports storage folder
mkdir ./dist/app/reports

for ARGUMENT in "$@"
do

    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   

    case "$KEY" in
            SENDGRID_API_KEY)              SENDGRID_API_KEY=${VALUE} ;;
            SENDGRID_FROM_EMAIL)    SENDGRID_FROM_EMAIL=${VALUE} ;; 
            SENDGRID_TO_EMAIL)    SENDGRID_TO_EMAIL=${VALUE} ;;       
            *)   
    esac    


done

# create .env file using arguments
echo "PYTHON_ENV=production
SENDGRID_API_KEY=$SENDGRID_API_KEY
SENDGRID_FROM_EMAIL=$SENDGRID_FROM_EMAIL
SENDGRID_TO_EMAIL=$SENDGRID_TO_EMAIL" >> ./dist/app/.env

# copy database to dist/app/database folder (set the database file name to your own)
mkdir ./dist/app/database
cp ./database/database.xlsx ./dist/app/database/database.xlsx

# copy drivers to dist/app folder
cp -r ./drivers ./dist/app
