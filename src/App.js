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

function PrivateRoute({component: Component, ...rest}){
    const [logged] = useAuth();

    return (
        <Route {...rest} render={(props) => (
            logged
                ? <Component {...props} />
                : <Redirect to={{pathname:'/login', state: {from: props.location}}}/>
        )}
        />
    );
}

class App extends React.Component{
    render() {
        return (
            <Router>
                <div>
                    <PrimarySearchAppBar/>
                    <Container maxWidth={"md"}>
                        <Switch>
                            <PrivateRoute path="/JobPostings/:id" component={ApplicantsList}>
                            </PrivateRoute>
                            <PrivateRoute path="/JobPostings" component={JobPostingsList}>
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
                            <PrivateRoute path="/secret"
                                          component={Secret}>
                            </PrivateRoute>
                            <Route path="/home" component={Homepage}>
                            </Route>
                            <PrivateRoute path="/" component={JobPostingsList}>
                            </PrivateRoute>
                        </Switch>
                    </Container>
                </div>
            </Router>
        );
    }
}

export default App;
