import {authFetch} from "./auth";
import {Container} from "@material-ui/core";
import React from "react";
import Grid from "@material-ui/core/Grid";
import CssBaseline from "@material-ui/core/CssBaseline";
import Typography from "@material-ui/core/Typography";
import {Link as RouterLink} from "react-router-dom";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import ProgressBar from "./components/ProgressBar";
import Divider from "@material-ui/core/Divider";

class InterviewList extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            interviews: [],
            isLoaded: false
        }
    }

    componentDidMount() {
        let url = 'http://localhost:5000/Events';
        authFetch(url)
            .then(response => response.json())
            .then(data => {
                this.setState({
                    interviews: data.events,
                    isLoaded: true
                })
            })
    }

    render() {
        if (!this.state.isLoaded){
            return <ProgressBar/>
        }
        else return (
            <Container component={"main"}>
                <CssBaseline />
                <Grid container direction={"row"} justify={"flex-start"}
                      alignItems={"center"} spacing={1}>
                    <Grid item xs={12}>
                        <Typography className='title' gutterBottom variant="h2" component={"h1"}>
                            My events
                        </Typography>
                    </Grid>
                    <Grid container item xs={12} justify={"space-evenly"}>
                        <Grid item xs={4}>
                            <Typography className='title' gutterBottom variant="h5"
                                        component="h2" align={"left"}>
                                Company
                            </Typography>
                        </Grid>
                        <Grid item xs={4}>
                            <Typography className='title' gutterBottom variant="h5"
                                        component="h2" align={"left"}>
                                Location
                            </Typography>
                        </Grid>
                        <Grid item xs={4}>
                            <Typography className='title' gutterBottom variant="h5"
                                        component="h2" align={"left"}>
                                Date
                            </Typography>
                        </Grid>
                    </Grid>
                    <Divider/>
                    {this.state.interviews.map(event => (
                        <Grid container item xs={12}>
                            <EventLinkItem
                                key={event.event_id}
                                company={event.first_name}
                                event_location = {event.location}
                                event_date = {formatDate(event.date)}
                            >
                            </EventLinkItem>
                        </Grid>
                    ))}
                </Grid>
            </Container>
        )
    }
}

function EventLinkItem(props) {
    const {company, event_location, event_date, to} = props;

    const renderLink = React.useMemo(
        () => React.forwardRef((itemProps, ref) => <RouterLink to={to} ref={ref} {...itemProps} />),
        [to],
    );

    return (
        <ListItem button component={renderLink}
                  style={{paddingLeft: "0px", paddingRight: "0px"}}>
            <Grid container item xs={4} alignContent={"center"}>
                <ListItemText primary={company}/>
            </Grid>
            <Grid container item xs={4} alignContent={"center"}>
                <ListItemText primary={event_location} />
            </Grid>
            <Grid container item xs={4} alignContent={"center"}>
                <ListItemText primary={event_date} />
            </Grid>
        </ListItem>
    )
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


export default InterviewList;