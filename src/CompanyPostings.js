import React from "react";
import ListItemLink from "./ListItemLink";
import List from "@material-ui/core/List";
import {Paper} from "@material-ui/core";
import './CompanyPostings.css';
import Divider from "@material-ui/core/Divider";
import Button from "@material-ui/core/Button";
import {withRouter} from "react-router";
import {authFetch} from "./auth";
import jwtDecode from "jwt-decode";
import {Link as RouterLink} from "react-router-dom";
import Grid from "@material-ui/core/Grid";


class JobPostingsList extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            postings: []
        };
    }

    componentDidMount() {
        let url = `http://localhost:5000/JobPosting`;
        authFetch(url, {
            method: 'get',
        })
            .then(response => response.json())
            .then(
                (data) => {
                    this.setState({
                        isLoaded: true,
                        postings: data
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            );
    }

    render() {
        const { error, isLoaded, postings } = this.state;

        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>
        } else {
            const localToken = localStorage.getItem('jwt_token');
            const decoded = jwtDecode(localToken);
            let url = ''
            if (decoded['rls'] === 'recruiter') {
                url = '/jobPostings/';
            }
            else {
                url = '/JobPostingApplication/';
            }
            return (
                <Paper className='jobPostingsList' elevation={0}>
                    <h1>My Job Postings</h1>
                    <Button component={RouterLink} color='primary' variant='contained' to="/JobPostingForm">New job posting</Button>
                    <div className=''>
                        <Grid   container
                                direction="row"
                                justify="left"
                                alignItems="left"
                                spacing={3}>
                            {(decoded['rls'] === 'applicant') ?
                                <Grid item xs={2}><div className=' positionName JobPostingTitle' ><p>Company</p></div></Grid>:null}
                            <Grid item xs={2}>
                                <div className=' JobPostingTitle' ><p>Position</p></div>
                            </Grid>
                            <Grid item xs={2}>
                                <div className='JobPostingTitle'><p>Location</p></div>
                            </Grid>
                            <Grid item xs={3}>
                                <div className='JobPostingTitle'><p>Presentation Date</p></div>
                            </Grid>
                            <Grid item xs={2}>
                                <div className='JobPostingTitle'><p>Deadline</p></div>
                            </Grid>
                        </Grid>
                    </div>
                    <Divider/>
                    <List>
                        {postings.map(posting => (
                            <ListItemLink
                                key={posting.posting_id}
                                companyName = {posting.first_name}
                                primary={posting.position_name}
                                to={url + posting.posting_id}
                                location={posting.location}
                                presentationDate={formatDate(posting.presentationdate)}
                                deadline={formatDate(posting.deadline)}
                                isApplicant = {decoded['rls'] === 'applicant'}
                            >
                            </ListItemLink>
                        ))}
                    </List>
                </Paper>
            );
        }

    }
}

function formatDate(timestamp) {
    var date = new Date(timestamp)
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return (date.getMonth()+1) + "/" + date.getDate() + "/" + date.getFullYear() + "  " + strTime;
}

export default withRouter(JobPostingsList);
