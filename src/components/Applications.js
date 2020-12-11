import React from "react";
import {withRouter} from "react-router";
import ListItemLink from "../ListItemLink";
import List from "@material-ui/core/List";
import {Paper} from "@material-ui/core";
import '../CompanyPostings.css';
import Divider from "@material-ui/core/Divider";
import {authFetch} from "../auth";
import jwtDecode from "jwt-decode";
import Grid from "@material-ui/core/Grid";
import PropTypes from "prop-types";


class ApplicationsList extends React.Component{
    static propTypes = {
        match: PropTypes.object.isRequired,
        history: PropTypes.object.isRequired
    };

    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            postings: [],
        };
    }

    componentDidMount() {
        let url = `http://localhost:5000/Applications`;
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
            return (
                <Paper className='jobPostingsList' elevation={0}>
                    <h1>My Applications</h1> 
                    <div className=''>
                        <Grid container
                              direction="row"
                              justify="flex-start"
                              alignItems="flex-start"
                              spacing={3}>
                            {(decoded['rls'] === 'applicant') ?
                                <Grid item xs={3}>
                                    <div className=' positionName JobPostingTitle'><p>Company</p></div>
                                </Grid> : null}
                            <Grid item xs={3}>
                                <div className=' JobPostingTitle'><p>Position</p></div>
                            </Grid>
                            <Grid item xs={3}>
                                <div className='JobPostingTitle'><p>Location</p></div>
                            </Grid>
                            <Grid item xs={3}>
                                <div className='JobPostingTitle'><p>Deadline</p></div>
                            </Grid>
                        </Grid>
                    </div>
                    <Divider/>
                    <List>
                        {postings.map(posting => (
                            <ListItemLink
                                key={posting.posting_id}
                                companyName={posting.first_name}
                                primary={posting.position_name}
                                to={"jobPostingApplication/" + posting.posting_id}
                                location={posting.location}
                                deadline={formatDate(posting.deadline)}
                                isApplicant={decoded['rls'] === 'applicant'}
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

class Applications extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false
        }
    }

    render() {
            return (
                <ApplicationsList/>
            );
        }
    }

export default withRouter(Applications)