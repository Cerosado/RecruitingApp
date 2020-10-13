import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Applicants from './Applicants.js';
import PrimarySearchAppBar from './NavBar.js'
import * as serviceWorker from './serviceWorker';


ReactDOM.render(
    <Applicants/>,
    document.getElementById('root')
);

ReactDOM.render(
    <PrimarySearchAppBar />,
    document.getElementById('navbar')
);



// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
