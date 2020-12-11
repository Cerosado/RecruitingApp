import React, {useEffect, useState} from 'react';
import './App.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import ApplicantsList from "./Applicants";
import JobPostingsList from "./CompanyPostings";
import PrimarySearchAppBar from "./NavBar";
import {Container} from "@material-ui/core";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import {authFetch, useAuth} from "./auth";
import Homepage from "./components/Homepage";
import EmailConfirm from "./components/EmailConfirm";
import EventForm from "./EventForm";
import jwtDecode from "jwt-decode";
import Profile from "./components/Profile"
import Applications from "./components/Applications"
import JobPostingApplication from "./JobPostingApplication";
import JobPostingFormController from "./JobPostingForm";
import InterviewList from "./Interviews";

function Secret() {
    const [message, setMessage] = useState('')

    useEffect(() => {
        authFetch("http://localhost:5000/api/protected").then(response => {
            if (response.status === 401){
                setMessage("Sorry you aren't authorized!")
                return null
            }
            return response.json()
        }).then(response => {
            if (response && response.message){
                setMessage(response.message)
            }
        })
    }, [])
    return (
        <h2>Secret: {message}</h2>
    )
}

function PrivateRoute({component: Component, roles, ...rest}){
    const [logged] = useAuth();

    if (!logged) {
        return <Redirect to={{pathname:'/login', state: {from: rest.location}}}/>
    }

    const localToken = localStorage.getItem('jwt_token');
    const decoded = jwtDecode(localToken);

    if (roles && roles.indexOf(decoded['rls']) === -1){
        return <Redirect to={{ pathname: '/Home'}} />
    }

    return <Route {...rest}
                  render={({location, ...routeProps}) => <Component {...routeProps}/>}
    />
}

class App extends React.Component{
    render() {
        return (
            <Router>
                <div>
                    <PrimarySearchAppBar/>
                    <Container maxWidth={"md"}>
                        <Switch>
                            <PrivateRoute path="/JobPostings/:id" component={ApplicantsList} roles={["recruiter"]}>
                            </PrivateRoute>
                            <PrivateRoute path="/JobPostings" component={JobPostingsList}>
                            </PrivateRoute>
                            <PrivateRoute path="/Profile" component={Profile}>
                            </PrivateRoute>
                            <PrivateRoute path="/Applications" component={Applications}>
                            </PrivateRoute>
                            <Route path="/Login"
                                   render={routerProps => (
                                       <SignIn {...routerProps}/>
                                   )}>
                            </Route>
                            <Route path="/SignUp"
                                   render={routerProps => (
                                       <SignUp {...routerProps}/>
                                   )}>
                            </Route>
                            <Route path="/Auth/Confirm" component={EmailConfirm}>
                            </Route>
                            <PrivateRoute path="/secret"
                                          component={Secret}
                                          roles={["applicant"]}>
                            </PrivateRoute>
                            <Route path="/JobPostingForm" roles={["recruiter"]}
                                   render={routerProps => (
                                       <JobPostingFormController {...routerProps}/>
                                   )}>
                            </Route>
                            <Route path="/JobPostingApplication/:id" roles={["applicant"]}
                                   render={routerProps => (
                                       <JobPostingApplication {...routerProps}/>
                                   )}>
                            </Route>
                            <Route path="/EventForm/:id" roles={["recruiter"]}
                                   render={routerProps => (
                                       <EventForm {...routerProps}/>
                                   )}>
                            </Route>
                            <PrivateRoute path="/Events"
                                   component={InterviewList} roles={["recruiter", "applicant"]}>
                            </PrivateRoute>
                            <Route path="/home" component={Homepage}>
                            </Route>
                            <PrivateRoute path="/" component={JobPostingsList} roles={["recruiter", "applicant"]}>
                            </PrivateRoute>
                        </Switch>
                    </Container>
                </div>
            </Router>
        );
    }
}

export default App;
