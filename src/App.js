import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ApplicantsList from "./Applicants";
import JobPostingsList from "./CompanyPostings";
import PrimarySearchAppBar from "./NavBar";
import {Container} from "@material-ui/core";

class App extends React.Component{
  render() {
    return (
        <Router>
          <div>
            <PrimarySearchAppBar/>
            <Container maxWidth={"md"}>
              <Switch>
                <Route path="/JobPostings/:id"
                       render={routerProps => (
                           <ApplicantsList {...routerProps}/>
                       )}>
                </Route>
                <Route path="/JobPostings"
                       render={routerProps => (
                           <JobPostingsList {...routerProps}/>
                       )}>
                </Route>
                <Route path="/">
                  <JobPostingsList/>
                </Route>
              </Switch>
            </Container>
          </div>
        </Router>
    );
  }
}

export default App;
