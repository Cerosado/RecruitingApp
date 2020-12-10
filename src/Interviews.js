import {authFetch} from "./auth";
import {Container} from "@material-ui/core";
import React from "react";
import Grid from "@material-ui/core/Grid";
import CssBaseline from "@material-ui/core/CssBaseline";
import Typography from "@material-ui/core/Typography";
import {Link as RouterLink} from "react-router-dom";

class InterviewList extends React.Component{
    constructor(props) {
        super(props);
        this.setState({
            interviews: [],
            isLoaded: false
        })
    }

    componentDidMount() {
        // let url = 'http://localhost:5000/Events';
        // authFetch(url)
        //     .then(response => response.json())
        //     .then(data => {
        //         this.setState({
        //             interviews: data.events,
        //             isLoaded: true
        //         })
        //     })
    }

    render() {
        return (
            <Container component={"main"}>
                <CssBaseline />
                <Grid container direction={"row"} justify={"flex-start"}
                      alignItems={"center"} spacing={1}>
                    <Grid item xs={12} alignItems={"center"}>
                        <Typography className='title' gutterBottom variant="h2" component={"h1"}>
                            My events
                        </Typography>
                    </Grid>
                    <Grid container item xs={12} spacing={3}>
                        <Grid item xs={4}>
                            <Typography className='title' gutterBottom variant="h5"
                                        component="h2" align={"center"}>
                                Company
                            </Typography>
                        </Grid>
                        <Grid item xs={4}>
                            <Typography className='title' gutterBottom variant="h5"
                                        component="h2" align={"center"}>
                                Location
                            </Typography>
                        </Grid>
                        <Grid item xs={4}>
                            <Typography className='title' gutterBottom variant="h5"
                                        component="h2" align={"center"}>
                                Date
                            </Typography>
                        </Grid>
                    </Grid>
                </Grid>
            </Container>
        )
    }
}

function EventLinkItem(props) {
    const {company, event_location, event_date} = this.props;

    const renderLink = React.useMemo(
        () => React.forwardRef((itemProps, ref) => <RouterLink to={to} ref={ref} {...itemProps} />),
        [to],
    );
}


export default InterviewList;