import React from 'react';
import './Applicants.css';
import icon from './Resources/resume.jpg';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import {List} from "@material-ui/core";
import {withRouter} from "react-router-dom";
import {authFetch} from "./auth";
import Select from '@material-ui/core/Select';
import FormControl from "@material-ui/core/FormControl";
import MenuItem from "@material-ui/core/MenuItem";
import InputLabel from "@material-ui/core/InputLabel";
import {classes} from "istanbul-lib-coverage";
import Dropdown from "./Dropdown";
import Grid from "@material-ui/core/Grid";
import jwtDecode from "jwt-decode";
import ListItemLink from "./ListItemLink";
import RankedParticipantItem from "./RankedParticipantItem";
import Divider from "@material-ui/core/Divider";


class Applicant extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            Name: null,
            University: null,
            Gpa: null,
            // Resume: resume,
            Rank: null,
        };
    }

    render() {
        return (
            <Card className='applicant' variant="outlined">
                <CardContent>
                    <div className='container' row>
                        <Typography className='' gutterBottom variant="h5" component="h2">
                            {this.props.Name}
                        </Typography>
                        <Typography className='' variant="h5" component="h2">
                            {this.props.University}
                        </Typography>
                        <Typography className='' color="textSecondary" variant="h5">
                            {this.props.Gpa}
                        </Typography>
                        <CardActions className=''>
                            <Button
                                href={this.props.Link}
                                target="_blank"
                            >
                                <img className='' src={icon} alt="View resume"/>
                            </Button>
                        </CardActions>
                        <Typography className="" variant="body2" component="p">
                            {this.props.Rank}
                        </Typography>
                    </div>
                </CardContent>
            </Card>

        );
    }
}


class ApplicantsList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            posting: null,
            applicants: []
        }
    }

    componentDidMount() {
        let url_applicants = `http://localhost:5000/JobPosting/${this.props.match.params.id}`;
        authFetch(url_applicants)
            .then(response => response.json())
            .then(
                (data) => {
                    this.setState({
                        isLoaded: true,
                        posting: data.posting,
                        applicants: data.applicants
                    })
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
        const { error, isLoaded, posting, applicants } = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div>
                    <h1 className="MainTitle"> {`${posting.position_name} (${posting.location})`} Applicants List</h1>
                    <div className='titleContainer' row>
                        <div >
                            <Grid   container
                                    direction="row"
                                    justify="center"
                                    alignItems="center"
                                    spacing={0}>
                                <Grid item xs={4}>
                                    <p id="PositionName">
                                        Position name: <b>{posting.position_name}</b>
                                    </p>

                                </Grid>
                                <Grid item xs={4}>
                                    <p id="Location">
                                        Location: <b>{posting.location}</b>
                                    </p>

                                </Grid>
                                <Grid id='DatetimeGrid' item xs={4}>
                                    <p id="Deadline">
                                        Deadline: <b>{formatDate(posting.deadline)}</b>
                                    </p>
                                </Grid>
                                </Grid>
                            <Grid   container
                                    direction="column"
                                    justify="left"
                                    alignItems="left"
                                    spacing={0}>
                                <Grid item xs={6}>
                                    <p id="Description">
                                        Description: <b>{posting.description}</b>
                                    </p>

                                </Grid>
                                <Grid item xs={6}>
                                    <p id="KeyDetails">
                                        Key details: <b>{posting.key_details}</b>
                                    </p>

                                </Grid>
                            </Grid>
                        </div>
                        <br/>
                        <div>
                            <Grid   container
                                    direction="row"
                                    justify="left"
                                    alignItems="center"
                                    spacing={2}>
                                <Grid item xs={2}>
                                    <Typography className=' title' gutterBottom variant="h5" component="h2">
                                        Name
                                    </Typography>
                                </Grid>
                                <Grid item xs={3}>
                                    <Typography className=' title' variant="h5" component="h2">
                                        University
                                    </Typography>
                                </Grid>
                                <Grid item xs={2}>
                                    <Typography className=' title' color="textSecondary" variant="h5" style={{paddingLeft: "20px"}}>
                                        GPA
                                    </Typography>
                                </Grid>
                                <Grid item xs={2}>
                                    <Typography className=' title' variant="h5">
                                        View Resume
                                    </Typography>
                                </Grid>
                                <Grid item xs={2}>
                                    <Typography className=" title" variant="h5" style={{textAlign: "center"}}>
                                        Rank
                                    </Typography>
                                </Grid>
                            </Grid>
                        </div>
                    </div>
                    <Divider/>
                    <div>
                        {/*<List>*/}
                        {/*    {applicants.map(applicant => (*/}
                        {/*        <li key={applicant.user_id}>*/}
                        {/*            <Applicant*/}
                        {/*                Name={applicant.first_name + applicant.last_name}*/}
                        {/*                University={'Placeholder university'}*/}
                        {/*                Gpa={'4.00'}*/}
                        {/*                Rank={applicant.rank}*/}
                        {/*                Link={base64ToLink(applicant.resume_data, applicant.resume_extension)}*/}
                        {/*            />*/}
                        {/*        </li>*/}
                        {/*    ))}*/}
                        {/*</List>*/}
                        <List>
                            {applicants.map(applicant => (
                                <RankedParticipantItem
                                    key={applicant.user_id}
                                    name = {applicant.first_name + applicant.last_name}
                                    university={'Placeholder university'}
                                    gpa={'4.00'}
                                    resume= {base64ToLink(applicant.resume_data, applicant.resume_extension)}
                                    rank={applicant.rank}
                                    to={'/EventForm/' + applicant.user_id}
                                >
                                </RankedParticipantItem>
                            ))}
                        </List>
                    </div>
                </div>
            );
        }
    }
}

function base64ToLink(base64, ext) {
    let binaryString = window.atob(base64);
    let binaryLen = binaryString.length;
    let bytes = new Uint8Array(binaryLen);
    for (let i = 0; i < binaryLen; i++) {
        let ascii = binaryString.charCodeAt(i);
        bytes[i] = ascii;
    }
    let blob = new Blob([bytes], {type: `application/${ext}`});
    return window.URL.createObjectURL(blob);
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

export default withRouter(ApplicantsList);



//install material - npm install @material-ui/core
//install material icons - npm install  @material-ui/icons
