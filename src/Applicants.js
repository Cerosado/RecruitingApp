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
import ListItem from "@material-ui/core/ListItem";


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
                        <Typography className='name' gutterBottom variant="h5" component="h2">
                            {this.props.Name}
                        </Typography>
                        <Typography className='university' variant="h5" component="h2">
                            {this.props.University}
                        </Typography>
                        <Typography className='gpa' color="textSecondary" variant="h5">
                            {this.props.Gpa}
                        </Typography>
                        <CardActions className='Icon'>
                            <Button
                                href={this.props.Link}
                                target="_blank"
                            >
                                <img className='icon' src={icon} alt="View resume"/>
                            </Button>
                        </CardActions>
                        <Typography className="Rank" variant="body2" component="p">
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
            applicants: []
        }
    }

    renderApplicant(Name, University, Gpa, Rank) {
        return (
            <Applicant
                Name = {Name}
                University = {University}
                Gpa = {Gpa}
                Rank = {Rank}
            />
        );
    }

    componentDidMount() {
        let url = 'http://localhost:5000/JobPosting/1';
        fetch(url)
            .then(response => response.json())
            .then(
                (data) => {
                    this.setState({
                        isLoaded: true,
                        applicants: data
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
        const { error, isLoaded, applicants } = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div>
                    <h1 className="MainTitle"> Job Posting #1 Applicants List</h1>
                    <div className='titleContainer' row>
                        <Typography className='name title' gutterBottom variant="h5" component="h2">
                            Name
                        </Typography>
                        <Typography className='university title' variant="h5" component="h2">
                            University
                        </Typography>
                        <Typography className='gpa title' color="textSecondary" variant="h5">
                            GPA
                        </Typography>
                        <Typography className='Icon title' variant="h5">
                            View Resume
                        </Typography>
                        <Typography className="RankTitle title" variant="h5">
                            Rank
                        </Typography>
                    </div>
                    <div>
                        <List>
                            {applicants.map(applicant => (
                                <li key={applicant.user_id}>
                                    <Applicant
                                        Name={applicant.first_name + applicant.last_name}
                                        University={'Placeholder university'}
                                        Gpa={'4.00'}
                                        Rank={applicant.rank}
                                        Link={base64ToLink(applicant.resume_data, applicant.resume_extension)}
                                    />
                                </li>
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

export default ApplicantsList;



//install material - npm install @material-ui/core
//install material icons - npm install  @material-ui/icons
