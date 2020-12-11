import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import Grid from "@material-ui/core/Grid";
import jwtDecode from "jwt-decode";
import Button from "@material-ui/core/Button";
import {withFormik} from "formik";
import {authFetch} from "./auth";
import React, {useEffect} from "react";
import {useParams} from "react-router-dom";

function JobPostingForm({
                            errors,
                            handleBlur,
                            handleChange,
                            handleSubmit,
                            touched,
                            values,
                            setFieldValue,
                            status
                        }) {
    const [posting, setPosting] = React.useState('');
    const [canApply, setCanApply] = React.useState(false);
    const { id } = useParams();
    useEffect(() => {
        let url = `http://localhost:5000/JobPostingForm/${id}`;
        authFetch(url, {
            method: 'get'
        }).then(response => response.json())
            .then(
                (data) => {
                    setPosting(data['posting']);  
                    data['application'].map(application=>{
                    if (application['posting_id']==id){setCanApply(true);}
                });
                },)
    }, [id]);

    return (
        <Container component="main" >
            <CssBaseline />
            <h1>Apply to job posting</h1>
            <form onSubmit={handleSubmit}>
                <Grid   container
                        direction="row"
                        justify="center"
                        alignItems="center"
                        spacing={2}>
                    <Grid item xs={4}>
                        <p id="CompanyName" style={{marginBottom: "0px", fontSize: "1.3rem"}}>
                            Company name:
                        </p>
                        <b style={{fontSize: "1.3rem"}}>{posting.first_name}</b>
                    </Grid>
                    <Grid item xs={4}>
                        <p id="PositionName" style={{marginBottom: "0px", fontSize: "1.3rem"}}>
                            Position name:
                        </p>
                        <b style={{fontSize: "1.3rem"}}>{posting.position_name}</b>
                    </Grid>
                    <Grid item xs={4}>
                        <p id="Location" style={{marginBottom: "0px", fontSize: "1.3rem"}}>
                            Location:
                        </p>
                        <b style={{fontSize: "1.3rem"}}>{posting.location}</b>
                    </Grid>
                    <Grid item xs>
                        <p id="Description" style={{marginBottom: "0px", fontSize: "1.3rem"}}>
                            Description:
                        </p>
                        <b style={{fontSize: "1.3rem"}}>{posting.description}</b>
                    </Grid>
                    <Grid item xs>
                        <p id="KeyDetails" style={{marginBottom: "0px", fontSize: "1.3rem"}}>
                            Key details:
                        </p>
                        <b style={{fontSize: "1.3rem"}}>{posting.key_details}</b>
                    </Grid>
                    <Grid item xs={4}>
                        <p id="PayType" style={{marginBottom: "0px", fontSize: "1.5rem"}}>
                            Pay type:
                        </p>
                        <b style={{fontSize: "1.3rem"}}>{posting.pay_type}</b>
                    </Grid>
                    <Grid item xs={4}>
                        <p id="PayAmount" style={{marginBottom: "0px", fontSize: "1.3rem"}}>
                            Pay amount:
                        </p>
                        <b style={{fontSize: "1.3rem"}}>{posting.pay_amount}</b>
                    </Grid>

                    <Grid id='DatetimeGrid' item xs={4}>
                        <p id="Deadline" style={{marginBottom: "0px"}}>
                            Deadline:
                        </p>
                        <b style={{fontSize: "1.33rem"}}>{formatDate(posting.deadline)}</b>
                    </Grid>
                </Grid>
                <br/>
                <br/>
                <br/>
                <div id="SubmitDiv">
                    <Grid item xs={12} sm={12}>
                            <Button id='submit_button' type="submit" variant="contained" color="primary"
                                    disabled={jwtDecode(localStorage.getItem('jwt_token'))['rls'] === 'recruiter' || canApply}>
                                Apply
                            </Button>
                    </Grid>
                </div>
            </form>
        </Container>
    );
}

const CreateJobPosting = withFormik({
    // mapPropsToValues: () => ({
    //     posting_id: '',
    //     location: '',
    //     description: '',
    //     keyDetails: '',
    //     payType: '',
    //     payAmount: '',
    //     deadline: '',
    // }),

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
            let url = `http://localhost:5000/Applications/${props.match.params.id}`;
            authFetch(url, {
                method: 'post',
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
                            pathname: '/JobPostings',
                            state: {message: json_response.message, from: {pathname: "/"}},
                            from: '/'
                        });
                        console.log(json_response.message)
                    }
                )
    },
})(JobPostingForm);

export default CreateJobPosting;

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
