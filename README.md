# ReCodEx file server
[![Build 
Status](https://img.shields.io/travis/ReCodEx/fileserver/master.svg?label=Build%20status)](https://travis-ci.org/ReCodEx/fileserver)

An app that serves as storage for submissions and supplementary files for 
assignments. The files are exposed via HTTP.

## Installation

1. Clone this repository
2. Install dependencies using `pip`
```
pip install -r requirements.txt
```

## Running in development mode

```
python3 fileserver.py runserver
```

Use the `--help` switch to find how to set e.g. port on which the server 
listens.

## Running using WSGI

If you need features such as HTTP authentication or efficient serving of static 
files, it is recommended to run the app in a full-fledged web server (such as 
Apache or Nginx) using WSGI.
