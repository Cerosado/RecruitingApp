import {makeStyles} from "@material-ui/core/styles";
import React from "react";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";


const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));



const Dropdown = ({
                      field,
                      ...props
                  }) => {
    const classes = useStyles();

    return (
        <FormControl className={classes.formControl}>
            <InputLabel id="DropdownLabel">{props.label}</InputLabel>
            <Select
                labelId="DropdownLabel"
                id="DropdownSelect"
                {...field}
            >
                {props.menuItems.map((item) =>
                    <MenuItem key={item.weight} value={item.weight}>{item.label}</MenuItem>)}
            </Select>
        </FormControl>
    );
}

export default Dropdown;


