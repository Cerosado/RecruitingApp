import React, {Component, useEffect, useState} from 'react'
import {authFetch, login} from "../auth";
import CircularProgress from "@material-ui/core/CircularProgress";
import {Redirect} from "react-router-dom";
import {useLocation} from "react-router-dom";

function useQuery() {
    return new URLSearchParams(useLocation().search)
}

export default function EmailConfirm() {
    const [confirming, setConfirming] = useState(true)
    const query = useQuery();

    useEffect( () => {
        const url = 'http://localhost:5000/finalize';
        const confirmToken = query.get("token");
        fetch(url, {
            method: 'post',
            headers: new Headers({
                'Authorization': `Bearer ${confirmToken}`,
                'Content-Type': 'application/x-www-form-urlencoded'})
        })
            .then(res => res.json())
            .then(token => {
                login(token);
                setConfirming(false);
            })
            .catch(err => console.log(err))
    });

    return (
        <div className="confirm">
            {confirming
                ? <CircularProgress/>
                : <Redirect to="/"/>
            }
        </div>
    )

}