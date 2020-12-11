import React from "react";
import {classes} from "istanbul-lib-coverage";
import TextField from "@material-ui/core/TextField";



function DateTimeField(props) {
    const {label, onChange, onBlur, value, error, helperText} = props;

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


