import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import {Link as RouterLink} from "react-router-dom";
import Switch from "@material-ui/core/Switch";
import {withFormik} from "formik";
import MuiAlert from "@material-ui/lab/Alert";
import Snackbar from "@material-ui/core/Snackbar";
import './SignUp.css';

// function Copyright() {
//     return (
//         <Typography variant="body2" color="textSecondary" align="center">
//             {'Copyright © '}
//             <Link color="inherit" href="https://material-ui.com/">
//                 Your Website
//             </Link>{' '}
//             {new Date().getFullYear()}
//             {'.'}
//         </Typography>
//     );
// }

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props}/>;
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
        marginTop: theme.spacing(3),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
}));

function SignUpForm({
                        errors,
                        handleBlur,
                        handleChange,
                        handleSubmit,
                        touched,
                        values,
                        setFieldValue,
                        status
                    }) {
    const classes = useStyles();

    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            {status && status.msg &&
                <Snackbar open={status.error}>
                    <Alert severity={status.error? "error": "info"}>
                        {status.msg}
                    </Alert>
                </Snackbar>
            }
            <div className={classes.paper}>
                <Avatar className={classes.avatar}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign up
                </Typography>
                <form className={classes.form} onSubmit={handleSubmit}>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={!values.isCompany? 6 : 12}>
                            <TextField
                                autoComplete="fname"
                                name="firstName"
                                variant="outlined"
                                required
                                fullWidth
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.firstName}
                                id="firstName"
                                label={!values.isCompany? "First Name" : "Company Name"}
                                error={touched.firstName && Boolean(errors.firstName)}
                                helperText={touched.firstName && errors.firstName}
                            />
                        </Grid>
                        {!values.isCompany
                            ? <Grid item xs={12} sm={6}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    value={values.lastName}
                                    id="lastName"
                                    label="Last Name"
                                    name="lastName"
                                    error={touched.lastName && Boolean(errors.lastName)}
                                    helperText={touched.lastName && errors.lastName}
                                    autoComplete="lname"
                                />
                            </Grid>
                            : null}

                        <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.username}
                                id="username"
                                label="Username"
                                name="username"
                                error={touched.username && Boolean(errors.username)}
                                helperText={touched.username && errors.username}
                                autoComplete="username"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.email}
                                id="email"
                                label="Email Address"
                                name="email"
                                error={touched.email && Boolean(errors.email)}
                                helperText={touched.email && errors.email}
                                autoComplete="email"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.password}
                                name="password"
                                label="Password"
                                type="password"
                                id="password"
                                error={touched.password && Boolean(errors.password)}
                                helperText={touched.password && errors.password}
                                autoComplete="current-password"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.cPassword}
                                name="cPassword"
                                label="Confirm Password"
                                type="password"
                                id="cPassword"
                                error={touched.password && Boolean(errors.password)}
                                autoComplete="current-password"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControlLabel
                                control={
                                    <Switch checked={values.isCompany}
                                            onChange={() => setFieldValue("isCompany", !values.isCompany)}
                                            onBlur={handleBlur}
                                            name="isCompany"
                                    />
                                }
                                label="I am a company's recruiter"
                            />
                        </Grid>
                    </Grid>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                    >
                        Sign Up
                    </Button>
                    <Grid container justify="flex-end">
                        <Grid item>
                            <Link component={RouterLink} to={'/Login'} color="inherit" variant="body2">
                                Already have an account? Sign in
                            </Link>
                        </Grid>
                    </Grid>
                </form>
            </div>
            {/*<Box mt={8}>*/}
            {/*    <Copyright />*/}
            {/*</Box>*/}
        </Container>
    );
}

const SignUp = withFormik({
    mapPropsToValues: () => ({
        firstName: '',
        lastName: '',
        username: '',
        email: '',
        password: '',
        cPassword: '',
        isCompany: false,
    }),

    validate: values => {
        let errors = {};
        const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;

        if (!values.firstName) {
            errors.firstName = `${!values.isCompany? "First Name":"Company Name"} is required`;
        }
        if (!values.lastName && !values.isCompany) {
            errors.lastName = "Last Name is required";
        }
        if (!values.username) {
            errors.username = "Username is required";
        } else if (values.username.length > 50){
            errors.username = "Username is too long"
        }
        if (!values.email) {
            errors.email = "Email is required";
        } else if (!email_regex.test(values.email)){
            errors.email = "Invalid Email";
        }
        if (!values.password) {
            errors.password = "Password is required";
        } else if (values.password !== values.cPassword){
            errors.password = "Passwords must match"
        }

        return errors;
    },

    handleSubmit: (values, { props, setStatus} ) => {
        let opts = {
            firstName: values.firstName,
            lastName: !values.isCompany? values.lastName : '',
            username: values.username,
            email: values.email,
            password: values.password,
            cPassword: values.cPassword,
            isCompany: values.isCompany,
        }
        let url = `http://localhost:5000/api/register`;
        fetch(url, {
            method: 'post',
            body: JSON.stringify(opts)
        })
            .then(response => {
                if (!response.ok) { throw response}
                return response.json()
            })
            .then(
                json_response => {
                    props.history.push({
                        pathname: '/Login',
                        state: { message: json_response.message, from: {pathname: "/"}},
                        from: '/'
                    });
                    console.log(json_response.message)
                }
            )
            .catch(error => {
                error.json().then(err => {
                    setStatus({
                        error: true,
                        msg: err.Error
                    })
                })
            })
    },
})(SignUpForm);

export default SignUp;