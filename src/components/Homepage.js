import React from "react";
import {makeStyles} from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import {Typography} from "@material-ui/core";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import Link from "@material-ui/core/Link";
import {Link as RouterLink} from "react-router-dom";
import {useAuth} from "../auth";

export default function Homepage(props){
    const classes = useStyles();

    const [logged] = useAuth();

    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <div className={classes.paper}>
                <Typography variant="h1" component="h2">
                    Recruiting Made Easy
                </Typography>
                <Typography variant={"body1"}>
                        As a recruiter you can create job postings for job positions open in your company. Users looking for
                    job can simply apply for this positions with a copy of their resume. The platform provides
                    recruiters a ranked list of all applicants for each position, where they can select the top
                    prospects and offer them an interview.
                </Typography>
            </div>
            {!logged &&
                <Box mt={8}>
                    <Grid container>
                        <Grid item xs>
                            <Link component={RouterLink} to="/SignUp" variant="body2">Create an account</Link>
                        </Grid>
                        <Grid item>
                            <Link component={RouterLink} to="/Login" variant="body2">Already have an account? Sign in</Link>
                        </Grid>
                    </Grid>
                </Box>
            }
        </Container>
    );
}

const useStyles = makeStyles((theme) => ({
    paper: {
        marginTop: theme.spacing(8),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
}));