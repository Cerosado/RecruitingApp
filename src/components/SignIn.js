import React, {useEffect, useState} from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import {Link as RouterLink} from "react-router-dom";
import {login, useAuth, logout} from "../auth";

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props}/>;
}

function Copyright() {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            <Link color="inherit" href="https://material-ui.com/">
                Your Website
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
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
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(1),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
}));

export default function Login(props) {
    const classes = useStyles();
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [showAlert, setShowAlert] = useState(false)
    const [alertSeverity, setAlertSeverity] = useState('info')
    const [alertMessage, setAlertMessage] = useState('')

    const onSubmitClick = (e)=> {
        e.preventDefault()
        console.log("You pressed login")
        let opts = {
            'username': username,
            'password': password
        }
        let url = `http://localhost:5000/api/login`;
        fetch(url, {
            method: 'post',
            body: JSON.stringify(opts)
        }).then(r => r.json())
            .then(token => {
                if (token.access_token){
                    login(token)
                    history.replace(from)
                }
                else {
                    setAlertSeverity("error")
                    setAlertMessage("Please type in correct username/password")
                    setShowAlert(true)
                }
            })
    }

    const handleUsernameChange = (e) => {
        setUsername(e.target.value)
    }

    const handlePasswordChange = (e) => {
        setPassword(e.target.value)
    }

    let [logged] = useAuth();
    let history = props.history;
    let location = props.location;

    let { from } = location.state || { from : { pathname: "/" } };

    useEffect(() => {
        const msg = location.state && location.state.message;
        if (msg){
            setAlertMessage(msg);
            setShowAlert(true);
        }
    }, [location.state]);


    return (
        <Container component="main" maxWidth="xs">
            <Snackbar open={showAlert}>
                <Alert severity={alertSeverity}>
                    {alertMessage}
                </Alert>
            </Snackbar>
            <CssBaseline />
            <div className={classes.paper}>
                <Avatar className={classes.avatar}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign in
                </Typography>
                {!logged?
                    <form className={classes.form} noValidate>
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                            onChange={handleUsernameChange}
                            value={username}
                        />
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            onChange={handlePasswordChange}
                            value={password}
                        />
                        <FormControlLabel
                            control={<Checkbox value="remember" color="primary" />}
                            label="Remember me"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            className={classes.submit}
                            onClick={onSubmitClick}
                        >
                            Sign In
                        </Button>
                        <Grid container>
                            <Grid item xs>
                                <Link href="#" variant="body2">
                                    Forgot password?
                                </Link>
                            </Grid>
                            <Grid item>
                                <Link component={RouterLink} to={'/SignUp'} color="inherit" variant="body2">
                                    {"Don't have an account? Sign Up"}
                                </Link>
                            </Grid>
                        </Grid>
                    </form>
                    : <button onClick={() => logout()}>Logout</button>}
            </div>
            <Box mt={8}>
                <Copyright />
            </Box>
        </Container>
    );
}