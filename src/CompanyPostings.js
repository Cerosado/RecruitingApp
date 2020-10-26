import React, {useState, useEffect} from "react";
import ListItemLink from "./ListItemLink";
import List from "@material-ui/core/List";
import {Paper} from "@material-ui/core";
import './CompanyPostings.css';
import Card from "@material-ui/core/Card";
import Divider from "@material-ui/core/Divider";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import CardActions from "@material-ui/core/CardActions";
import Button from "@material-ui/core/Button";
import icon from "./Resources/resume.jpg";
import {withRouter} from "react-router";

// function JobPostingList() {
//     const [postingList, setPostingList] = useState([])
//
//
//     useEffect(() => {
//         fetch(url).then(response => response.json()).then(data => {
//            setPostingList(data.results);
//         });
//     })
//
//     return (
//         <div>
//             <ul>
//                 {postingList.map(posting => (
//                     <li key={posting.id}>{posting.position_name}</li>
//                 ))}
//             </ul>
//         </div>
//     );
// }

class JobPosting extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            PositionName: null,
            Location: null,
            PresentationDate: null,
            Deadline: null,
        };
    }

    render() {
        return (
            <Card className='applicant' variant="outlined">
                <CardContent>
                    <div className='container' row>
                        <Typography className='positionName' gutterBottom variant="h5" component="h2">
                            {this.props.PositionName}
                        </Typography>
                        <Typography className='location' variant="h5" component="h2">
                            {this.props.Location}
                        </Typography>
                        <Typography className='presentationDate' color="textSecondary" variant="h5">
                            {this.props.PresentationDate}
                        </Typography>
                        <Typography className="Deadline" variant="body2" component="p">
                            {this.props.Deadline}
                        </Typography>
                    </div>
                </CardContent>
                <Divider></Divider>
            </Card>
        );
    }
}


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
        let url = `http://localhost:5000/JobPosting?user_id=2`;
        fetch(url)
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
            return (
                <Paper className='jobPostingsList' elevation={0}>
                    <h1>My Job Postings</h1>
                    <div className='JobPostingsContainer' row>
                    <div className='positionName JobPostingTitle' ><p>Position Name</p></div>
                    <div className='JobPostingTitle'><p>Location</p></div>
                    <div className='JobPostingTitle'><p>Presentation Date</p></div>
                    <div className='JobPostingTitle'><p>Deadline</p></div>
                    </div>
                    <Divider/>
                    <List>
                        {postings.map(posting => (
                            <ListItemLink
                                key={posting.posting_id}
                                primary={posting.position_name}
                                to={'/jobPostings/' + posting.posting_id}
                                location={posting.location}
                                presentationDate={formatDate(posting.presentationdate)}
                                deadline={formatDate(posting.deadline)}
                            >
                            </ListItemLink>
                            // <li key={posting.posting_id}>
                            //     <JobPosting
                            //         PositionName={posting.position_name}
                            //         Location={posting.location}
                            //         PresentationDate={posting.presentationDate}
                            //         Deadline={posting.deadline}
                            //         // new Intl.DateTimeFormat('en-US').format(date)
                            //     />
                            // </li>
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
