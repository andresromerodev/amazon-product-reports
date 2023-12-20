# amazon-product-reports
A Python application for scraping product data to generate automated reports.

## Running the Project
Environment Variables:
```shell
PYTHON_ENV=development
SENDGRID_API_KEY=secretkey
SENDGRID_TO_EMAIL=janedoe@mail.com
SENDGRID_FROM_EMAIL=joedoe@mail.com
```
Installing:
```shell
pip install -r requirements.txt
```
Running:
```shell
python app.py
```

## Creating a New Executable
```shell
./build.sh  SENDGRID_API_KEY="super_secret_key" SENDGRID_FROM_EMAIL="joedoe@mail.com" SENDGRID_TO_EMAIL="janedoe@mail.com"
```
