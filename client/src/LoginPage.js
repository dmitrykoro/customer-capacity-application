import React, { useState } from 'react';

import './css/design.css';

export default function LoginPage({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    async function handleClick() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, password: password })
        }

        const response = await (fetch(`/login`, requestOptions));
        const dataJson = await response.json();

        if (dataJson.error) {
            alert('Incorrect credentials');
            return;
        }

        onLogin( {dataJson} );
    }

    return (
        <div>
            <center>
                <h1>Welcome to Customer Capacity Service</h1>
                <input
                    type="text"
                    className='username'
                    required='required'
                    placeholder='Username'
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                /><br/>

                <input type='password'
                       type="text"
                       className='password'
                       required='required'
                       placeholder='Password'
                       value={password}
                       onChange={e => setPassword(e.target.value)}
                /><br/>

                <button type='submit' className="button-brown" onClick={handleClick}>Login</button><br/>
            </center>
        </div>
    )
}
