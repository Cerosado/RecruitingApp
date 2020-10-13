import React from 'react';
import './Applicants.css';
import icon from './Resources/resume.jpg';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';


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
                            <Button><img className='icon' src={icon} alt="View resume"/>
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

    render() {
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
                    {this.renderApplicant('Eduardo A. Perez Vega', 'Popac', '4.00', '99')}
                    {this.renderApplicant('Cristian E. Rosado Montes', 'Universidad de Puerto Rico Mayaguez', '2.00', '54')}
                </div>
            </div>
        );
    }
}

export default ApplicantsList;



//install material - npm install @material-ui/core
//install material icons - npm install  @material-ui/icons
