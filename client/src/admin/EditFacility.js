import React, { useState } from 'react';


export default function EditFacility({ user, onLogout, facilityName, facilityID }) {
    const [facilityCapacity, setFacilityCapacity] = useState('');
    const [Notes, setNotes] = useState('');

    async function updatefacility() {
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_key: user.dataJson.session_key,
                account_id: user.dataJson.account_id,
                facility_id: facilityID,
                max_capacity: facilityCapacity,
                notes: Notes
            })
        }

        const response = await (fetch(`/facility`, requestOptions));
        const dataJson = await response.json();

        if (dataJson.facility_id) {
            alert('facility updated successfully!');

            setFacilityCapacity('');
            setNotes('');
        } else if (dataJson.error === 'invalid-session-key') {
            onLogout();
        }
    }

    return (
        <div>
            <center>
                <h1>Edit {facilityName}</h1>

                <input
                    type='text'
                    className='facility_capacity'
                    required='required'
                    placeholder='New max capacity'
                    value={facilityCapacity}
                    onChange={e => setFacilityCapacity(e.target.value)}
                /><br/>

                <input
                    type='text'
                    className='notes'
                    required='required'
                    placeholder='New notes'
                    value={Notes}
                    onChange={e => setNotes(e.target.value)}
                /><br/>

                <button type='submit' className="button" onClick={updatefacility}>Submit</button>
            </center>
        </div>
    )
}