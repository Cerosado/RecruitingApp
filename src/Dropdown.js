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



function Dropdown(props) {
    const {label, menuItems} = props;
    const classes = useStyles();

    const [value, setValue] = React.useState('');

    const handleChange = (event) => {
        setValue(event.target.value);
    };

    return (
        <FormControl className={classes.formControl}>
            <InputLabel id="DropdownLabel">{label}</InputLabel>
            <Select
                labelId="DropdownLabel"
                id="DropdownSelect"
                value={value}
                onChange={handleChange}
            >
                {menuItems.map((item) =>
                    <MenuItem value={item.weight}>{item.label}</MenuItem>)}
            </Select>
        </FormControl>
    );
}

export default Dropdown;


