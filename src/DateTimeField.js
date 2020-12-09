import React from "react";
import { useState } from 'react';
import DatePicker from "react-datepicker";
import {classes} from "istanbul-lib-coverage";
import TextField from "@material-ui/core/TextField";



function DateTimeField(props) {
    const {label, onChange, onBlur, value, error, helperText} = props;
    const [valueDate, onChangeDate] = useState(new Date());

    return (
            <TextField
                id="datetime-local"
                label={label}
                type="datetime-local"
                className={classes.textField}
                InputLabelProps={{
                    shrink: true,
                }}
                onChange={onChange}
                onBlur={onBlur}
                value={value}
                error={error}
                helperText={helperText}
            />
    );
}

export default DateTimeField;


