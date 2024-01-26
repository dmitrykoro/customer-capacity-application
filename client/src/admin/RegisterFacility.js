import React, {useState} from 'react';


export default function RegisterFacility({user, onLogout}) {
    const [facilityName, setFacilityName] = useState('');
    const [facilityCity, setFacilityCity] = useState('');
    const [facilityCapacity, setFacilityCapacity] = useState('');
    const [Notes, setNotes] = useState('');

    async function RegisterFacility() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                    session_key: user.dataJson.session_key,
                    account_id: user.dataJson.account_id,
                    name: facilityName,
                    city: facilityCity,
                    max_capacity: facilityCapacity,
                    notes: Notes
            })
        }

        const response = await (fetch(`/facility`, requestOptions));
        const dataJson = await response.json();

        if (dataJson.facility_id) {
            alert('facility registered successfully!');
            setFacilityName('');
            setFacilityCity('');
            setFacilityCapacity('');
            setNotes('');
        } else if (dataJson.error === 'facility-exists') {
            alert('facility already exists!');
        } else if (dataJson.error === 'invalid-session-key') {
            onLogout();
        }
    }

    return (
        <div>
            <center>
                <h1>Register a new facility:</h1>
                <input
                    type='text'
                    className='facility_name'
                    required='required'
                    placeholder='facility name'
                    value={facilityName}
                    onChange={e => setFacilityName(e.target.value)}
                /><br/>

                <input
                    type='text'
                    className='facility_city'
                    required='required'
                    placeholder='City'
                    value={facilityCity}
                    onChange={e => setFacilityCity(e.target.value)}
                /><br/>

                <input
                    type='text'
                    className='facility_capacity'
                    required='required'
                    placeholder='Max capacity'
                    value={facilityCapacity}
                    onChange={e => setFacilityCapacity(e.target.value)}
                /><br/>

                <input
                    type='text'
                    className='notes'
                    required='required'
                    placeholder='Notes'
                    value={Notes}
                    onChange={e => setNotes(e.target.value)}
                /><br/>

                <button type='submit' className='button-green' onClick={RegisterFacility}>Submit</button>
            </center>
        </div>
    )
}