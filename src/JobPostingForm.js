import React, {useEffect, useState} from "react";
import './JobPostingForm.css';
import TextField from "@material-ui/core/TextField";
import Grid from '@material-ui/core/Grid';
import Dropdown from "./Dropdown";
import Button from "@material-ui/core/Button";
import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import {Field, withFormik} from "formik";
import {authFetch} from "./auth";
import jwtDecode from "jwt-decode";
import ProgressBar from "./components/ProgressBar";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";

class JobPostingFormController extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false,
            modelOptions: []
        }
    }

    componentDidMount() {
        let url = "http://localhost:5000/Models"
        authFetch(url)
            .then(
                response => response.json()
            )
            .then(
                data => this.setState({
                    modelOptions: data.fieldOfWorkOptions,
                    isLoaded: true
                })
            )
    }

    render() {
        {
            if (this.state.isLoaded){
                return <CreateJobPosting modelOptions={this.state.modelOptions}/>
            }
            else{
                return <ProgressBar/>
            }
        }
    }
}

    function JobPostingForm({
                            props,
                            errors,
                            handleBlur,
                            handleChange,
                            handleSubmit,
                            touched,
                            values,
                            setFieldValue,
                            status
                        }) {
    return (
        <Container component="main" >
            <CssBaseline />
            <h1>Create Job Posting</h1>
            <form onSubmit={handleSubmit}>
                <Grid   container
                        direction="row"
                        justify="center"
                        alignItems="center"
                spacing={2}>
                    <Grid item xs={6}>
                        <TextField id="PositionName" label="Position name" variant="outlined" required
                            // autoComplete="fname"
                                   name="positionName"
                                   fullWidth
                                   onChange={handleChange}
                                   onBlur={handleBlur}
                                   value={values.positionName}
                                   error={touched.positionName && Boolean(errors.positionName)}
                                   helperText={touched.positionName && errors.positionName}
                                   disabled={jwtDecode(localStorage.getItem('jwt_token'))['rls'] !== 'recruiter'}
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField id="Location" label="Location" variant="outlined" required
                            // autoComplete="fname"
                                   name="location"
                                   fullWidth
                                   onChange={handleChange}
                                   onBlur={handleBlur}
                                   value={values.location}
                                   error={touched.location && Boolean(errors.location)}
                                   helperText={touched.location && errors.location}
                        />
                    </Grid>
                    <Grid item xs>
                        <TextField id="Description" label="Description" variant="outlined" required
                            // autoComplete="fname"
                                   name="description"
                                   fullWidth
                                   onChange={handleChange}
                                   onBlur={handleBlur}
                                   value={values.description}
                                   error={touched.description && Boolean(errors.description)}
                                   helperText={touched.description && errors.description}
                        />
                    </Grid>
                    <Grid item xs>
                        <TextField id="KeyDetails" label="Key details" variant="outlined" required
                            // autoComplete="fname"
                                   name="keyDetails"
                                   fullWidth
                                   onChange={handleChange}
                                   onBlur={handleBlur}
                                   value={values.keyDetails}
                                   error={touched.keyDetails && Boolean(errors.keyDetails)}
                                   helperText={touched.keyDetails && errors.keyDetails}
                        />
                    </Grid>
                    <Grid item xs={4}>
                        <TextField id="PayType" label="Pay type" variant="outlined"
                            // autoComplete="fname"
                                   name="payType"
                                   fullWidth
                                   onChange={handleChange}
                                   onBlur={handleBlur}
                                   value={values.payType}
                                   error={touched.payType && Boolean(errors.payType)}
                                   helperText={touched.payType && errors.payType}
                        />
                    </Grid>
                    <Grid item xs={4}>
                        <TextField id="PayAmount" label="Pay amount" variant="outlined"
                            // autoComplete="fname"
                                   name="payAmount"
                                   fullWidth
                                   onChange={handleChange}
                                   onBlur={handleBlur}
                                   value={values.payAmount}
                                   error={touched.payAmount && Boolean(errors.payAmount)}
                                   helperText={touched.payAmount && errors.payAmount}
                        />
                    </Grid>

                    <Grid id='DatetimeGrid' item xs={4}>
                        <TextField
                            id="datetime-local"
                            label="Deadline"
                            type="datetime-local"
                            InputLabelProps={{
                                shrink: true,
                            }}
                            name="deadline"
                            onChange={handleChange}
                            onBlur={handleBlur}
                            value={values.deadline}
                            error={touched.deadline && Boolean(errors.deadline)}
                            helperText={touched.deadline && errors.deadline}
                            disabled={jwtDecode(localStorage.getItem('jwt_token'))['rls'] !== 'recruiter'}
                        />
                    </Grid>
                </Grid>
                <h1>Resume ranking settings:</h1>
                <Grid   container
                        direction="row"
                        justify="center"
                        alignItems="center"
                        spacing={1}
                >
                    <Grid item xs={4}>
                        <Field name='fieldOfWork' component={Dropdown}
                               label="Field of work"
                               menuItems={values.modelOptions.map(option =>
                                   ({
                                       weight: option.model_id,
                                       label: option.description})
                               )}
                        />
                    </Grid>
                    <Grid item xs={4}>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    name="useEducation"
                                    checked={values.useEducation}
                                    onChange={() => setFieldValue("useEducation", !values.useEducation)}
                                    color="primary"
                                />
                            }
                            label="Consider Education"
                        />
                    </Grid>
                </Grid>
                <br/>
                <br/>
                <br/>
                <div id="SubmitDiv">
                 <Grid item xs={12} sm={12}>
                        <Button id="Submit" type="submit"
                                variant="contained"
                                color="primary"
                                disabled={jwtDecode(localStorage.getItem('jwt_token'))['rls'] !== 'recruiter'}>Create job posting
                        </Button>
                    </Grid>
                </div>
            </form>
        </Container>
    );
}

const CreateJobPosting = withFormik({
    enableReinitialize: true,
    mapPropsToValues: (props) => ({
        positionName: '',
        location: '',
        description: '',
        keyDetails: '',
        payType: '',
        payAmount: '',
        deadline: '',
        fieldOfWork: '',
        useEducation: true,
        modelOptions: props.modelOptions
    }),

    validate: values => {
        let errors = {};

        // if (!values.firstName) {
        //     errors.positionName = "Position name is required";
        // }
        // if (!values.location) {
        //     errors.location = "Location is required";
        // }
        // if (!values.description) {
        //     errors.description = "Description is required";
        // }
        // if (!values.keyDetails) {
        //     errors.keyDetails = "Key Details is required";
        // }
        return errors;
    },

    handleSubmit: (values, { props, setStatus} ) => {
            let opts = {
                positionName: values.positionName,
                location: values.location,
                description: values.description,
                keyDetails: values.keyDetails,
                payType: values.payType,
                payAmount: values.payAmount,
                deadline: values.deadline,
                fieldOfWork: values.fieldOfWork,
                useEducation: values.useEducation
            }
            let url = `http://localhost:5000/JobPostingForm`;
            console.log(opts)
            authFetch(url, {
                method: 'post',
                body: JSON.stringify(opts)
            })
                .then(response => {
                    if (!response.ok) {
                        throw response
                    }
                    return response.json()
                })
                .then(
                    json_response => {
                        props.history.push({
                            pathname: '/JobPosting',
                            state: {message: json_response.message, from: {pathname: "/"}},
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
})(JobPostingForm);

export default JobPostingFormController;

