import React from "react";
import { useState } from 'react';
import DatePicker from "react-datepicker";
import {classes} from "istanbul-lib-coverage";
import TextField from "@material-ui/core/TextField";

function DateTimeField(props) {
    const {label} = props;
    const [value, onChange] = useState(new Date());

    return (
        <form id='Datetime' className={classes.container} noValidate>
            <TextField
                id="datetime-local"
                label={label}
                type="datetime-local"
                defaultValue="2017-05-24T10:30"
                className={classes.textField}
                InputLabelProps={{
                    shrink: true,
                }}
            />
        </form>
    );
}

export default DateTimeField;


