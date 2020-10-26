# Streamline: A Platform to Enable an Efficient Recruitment Process Proposal

A web application for screening/ranking resumes while also providing a platform for straightforward job recruitment and applications.

## Description
Created using React and the Material UI framework as front end, with Python's Flask framework providing a RESTful api for backend database handling. The resume ranking algorithm is a logistic regression algorithm trained using SKLearn.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
## Dependencies
#### Javascript
    material-ui
    json-server
    react-router-dom
#### Python
    Pyreparser
    Spacy
    Sklearn
    pandas
    joblib
    flask
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

### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: https://facebook.github.io/create-react-app/docs/code-splitting

### Analyzing the Bundle Size

This section has moved here: https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

### Making a Progressive Web App

This section has moved here: https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

### Advanced Configuration

This section has moved here: https://facebook.github.io/create-react-app/docs/advanced-configuration

### Deployment

This section has moved here: https://facebook.github.io/create-react-app/docs/deployment

### `npm run build` fails to minify

This section has moved here: https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify
