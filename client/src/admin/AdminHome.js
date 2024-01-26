import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import '../css/design.css';


export default function AdminPage({ user, onLogout }) {
    async function handleLogout() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_key:user.dataJson.session_key,
                account_id:user.dataJson.account_id
            })
        }
        const response = await (fetch(`/logout`, requestOptions));
        onLogout();
    }

    return(
        <div>
            <center>
                <button type='submit' className="button-brown" onClick={handleLogout}>Log out</button>
                <h3>Name: {user.dataJson.name}</h3>
                <h3>Role: {user.dataJson.role}</h3>
                <Link to="/register-facility">
                    <button type='submit' className="button">Register a new facility</button><br/><br/>
                </Link>
                <Link to="/manage-facilities">
                    <button type='submit' className="button">Manage facilities</button><br/><br/>
                </Link>
            </center>
        </div>
    )
}
