import React from "react";


export default function FacilityEntry(
    { facilityID, facilityName, facilityOccupancy, facilityIncome, facilityPopulation, onEdit, onDelete }
) {
    return (
        <div className='data-container'>
            <h2 className='data-heading'>{facilityName}</h2>
            <p className='data-item'>Current Occupancy:
                <span className='highlight'> {facilityOccupancy}</span></p>
            <p className='data-item'>Total Income:
                <span className='highlight'> {facilityIncome}</span></p>
            <p className='data-item'>Total Customers:
                <span className='highlight'> {facilityPopulation}</span></p>

            <button type='submit' className='button' onClick={() => onEdit(facilityName, facilityID)}>Edit</button>
            <button type='submit' className={'button-red'} onClick={() => onDelete(facilityID)}>Delete</button>
            <br/>
        </div>
    );
}
