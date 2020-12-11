---
driveId: 19KEK7ZoycH5kxVOl379oyhCP0ODlbHR3/preview
---
# Streamline: A Platform to Enable an Efficient Recruitment Process Proposal

A web application for screening/ranking resumes while also providing a platform for straightforward job recruitment and applications.

{% include googleDrivePlayer.html id=page.driveId %}

## Description
Created using React and the Material UI framework as front end, with Python's Flask framework providing a RESTful api for backend database handling. The resume ranking algorithm is a logistic regression algorithm trained using SKLearn.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
## Dependencies
#### Javascript
    material-ui
    json-server
    react-router-dom
    formik
    jwt-decode
    react-token-auth
#### Python
    Pyreparser
    Spacy
    scikit-learn
    docx2txt
    pandas
    joblib
    flask
    flask-praetorian
    pyscopg2
#### Additional steps for python
    python -m spacy download en_core_web_sm
    python -m nltk.downloader words
## Available Scripts
In ./src/backend, you can run:
## set FLASK_APP=app.py
(or equivalent export expression)
## flask run
This runs the Flask server.

Then, in the project directory you can run:
### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.


