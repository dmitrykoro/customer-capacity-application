import React, { useState } from 'react';

import '../css/design.css';


export default function BouncerPage({ user , onLogout}) {
    const [name, setName] = useState('');
    const [age, setAge] = useState('');
    const [chckin_document_id, setChckinDocument_id] = useState('');
    const [chckout_document_id, setChckoutDocument_id] = useState('');
    const [charge, setCharge] = useState('');

    async function handleLogout() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({facility_id: user.dataJson.facility_id, session_key:user.dataJson.session_key, account_id:user.dataJson.account_id})
        }

        const response = await (fetch(`/logout`, requestOptions));
        const dataJson = await response.json();

        onLogout();
    }

    async function onCheckin() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name, age: age, document_id: chckin_document_id,
                facility_id: user.dataJson.facility_id, session_key:user.dataJson.session_key, account_id:user.dataJson.account_id})
        }

        const response = await (fetch(`/customer/checkin`, requestOptions));
        const dataJson = await response.json();

        if (dataJson.hasOwnProperty('success') && dataJson.success) {
            alert('Checked in successfully!');
            return;
        }
        else if (dataJson.error === 'customer-already-checked-in') {
            alert('Customer is already checked in!');
            return;
        }
        else if (dataJson.error === 'facility-id-incorrect') {
            alert('Incorrect facility ID!');
            return;
        }
        else if (dataJson.error === 'facility-is-full') {
            alert('facility is full!');
            return;
        }
        else if (dataJson.error === 'invalid-session-key') {
            alert('Invalid session key. Please log in again!');
            return;
        }
        else {
            alert(dataJson.error);
            return;
        }
    }

    async function onCheckout() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ document_id: chckout_document_id, charge: charge,
                facility_id: user.dataJson.facility_id, session_key:user.dataJson.session_key, account_id:user.dataJson.account_id})
        }

        const response = await (fetch(`/customer/checkout`, requestOptions));
        const dataJson = await response.json();

        if (dataJson.success) {
            alert('Checked-out successfully!');
            return;
        }
        if (dataJson.error === 'customer-does-not-exist') {
            alert('Customer does not exist!');
            return;
        }
        else if (dataJson.error === 'invalid-session-key') {
            alert('Invalid session key. Please log in again!');
            return;
        }
        else {
            alert(dataJson.error);
            return;
        }
    }

    return (
        <div>
            <center>
                 <h3>Name: {user.dataJson.name}</h3>
                <h3>Role: {user.dataJson.role}</h3>
            <button type='submit' className="button-brown" onClick={handleLogout}>Log out</button>
            <h1>Check-in a new customer</h1>
                <label htmlFor="fname">Name</label><br/>
                <input
                    type="text"
                    className='name'
                    required='required'
                    value={name}
                    onChange={e => setName(e.target.value)}
                /><br/>
                <label htmlFor="fname">Age</label> <br/>
                <input
                    type="text"
                       className='age'
                       required='required'
                       value={age}
                       onChange={e => setAge(e.target.value)}
                /><br/>
                <label htmlFor="fname">Document ID</label><br/>
                <input
                    type="text"
                       className='document_id'
                       required='required'
                       value={chckin_document_id}
                       onChange={e => setChckinDocument_id(e.target.value)}
                /><br/><br/>

                <button type='submit' className="button" onClick={onCheckin}>Check In</button><br/>

                <h1>Check-out a customer</h1>
                <label htmlFor="fname">Document ID</label><br/>
                <input
                    type="text"
                       className='doc_id'
                       required='required'
                       value={chckout_document_id}
                       onChange={e => setChckoutDocument_id(e.target.value)}
                /><br/>
                <label htmlFor="fname">Charge</label><br/>
                <input
                    type="text"
                       className='charge'
                       required='required'
                       value={charge}
                       onChange={e => setCharge(e.target.value)}
                /><br/><br/>

                <button type='submit' className="button" onClick={onCheckout}>Check Out</button><br/>
            </center>
        </div>
    )
}
