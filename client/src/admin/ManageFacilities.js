import React from 'react';
import ReactPaginate from 'react-paginate';
import {useState, useEffect} from 'react';

import ClipLoader from 'react-spinners/ClipLoader';

import EditFacility from './EditFacility';
import FacilityEntry from './FacilityEntry';

import '../css/design.css';


export default function ManageFacilities({ user, onLogout }) {
    const [showFacilityPage, setShowFacilityPage] = useState(false);
    const [showFacilityID, setShowFacilityID] = useState('');
    const [showFacilityName, setShowFacilityName] = useState('');

    const [showEditPage, setShowEditPage] = useState(false);
    const [EditFacilityName, setEditFacilityName] = useState('');
    const [EditFacilityID, setEditFacilityID] = useState('');

    const [loading, setLoading] = useState(true);
    const [facilityList, setFacilityList] = useState([]);
    const [subList, setSubList] = useState([]);

    const [pageCount, setPageCount] = useState(1);
    const [currentPage, setCurrentPage] = useState(0);
    const itemsPerPage = 3;

    const [filteringNumber, setFilteringNumber] = useState(null);
    const [filterBy, setFilterBy] = useState('total_population');
    const [filteringCriteria, setFilteringCriteria] = useState('=');


    useEffect(() => {
        const controller = new AbortController();
        const signal = controller.signal;

        const requestOptions = {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                facility_id: user.dataJson.facility_id,
                session_key: user.dataJson.session_key,
                account_id: user.dataJson.account_id
            }),
            signal
        };

        fetch(`/manage-facilities/full`, requestOptions)
            .then(response => response.json())
            .then((dataJson) => {
                setLoading(false);

                if (dataJson.error && dataJson.error === 'invalid-session-key') {
                    alert('Invalid session key. Logging out.');
                    onLogout();
                } else {
                    setFacilityList(dataJson);
                }
            })
    }, [])

    const startIndex = currentPage * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    useEffect(() => {
        if (facilityList && facilityList.length > 0) {
            setSubList(facilityList.slice(startIndex, endIndex));
            setLoading(false);
            setPageCount(Math.ceil(facilityList.length / itemsPerPage));
        }
    }, [facilityList, startIndex, endIndex, itemsPerPage]);

    const handlePageChange = (selectedPage) => {
        setCurrentPage(selectedPage.selected);
    };

    async function onDelete(id_to_del) {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                facility_id: user.dataJson.facility_id,
                session_key: user.dataJson.session_key,
                account_id: user.dataJson.account_id,
                uuid_to_del: id_to_del
            }),
        };

        const response = await (fetch(`/manage-facilities/delete`, requestOptions));
        const dataJson = await response.json();

        if (dataJson.hasOwnProperty('success') && dataJson.success) {
            alert('facility deleted successfully!');

        } else if (dataJson.hasOwnProperty('success')) {
            alert('Error in deletion!');
        }
    }

    function onEdit(facilityName, facilityID) {
        setShowEditPage(true);
        setEditFacilityName(facilityName);
        setEditFacilityID(facilityID);
    }

    function onBack() {
        setShowFacilityPage(false);
        setShowEditPage(false);
    }

    async function onFilter() {
        const requestOptions = {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                facility_id: user.dataJson.facility_id,
                session_key: user.dataJson.session_key,
                account_id: user.dataJson.account_id,
                filter_by: filterBy,
                filter_criteria: filteringCriteria,
                filter_amount: filteringNumber
            }),
        };

        const response = await (fetch(`/manage-facilities/filter`, requestOptions));
        const dataJson = await response.json();

        if (dataJson.error) {
            alert('Please specify filter params!');
            return;
        }
        if (dataJson.length > 0) {
            setFacilityList(dataJson);
        } else {
            setFacilityList([{}]);
        }
    }

    const handleSetFilterBy = (event) => {
        setFilterBy(event.target.value);
    };

    const handleSetFilterCriteria = (event) => {
        setFilteringCriteria(event.target.value);
    };

    if (loading) {
        return <div style={{display: 'flex',  justifyContent: 'center', alignItems: 'center'}}>
            <ClipLoader
                size={50}
                aria-label='Loading Spinner'
                data-testid='loader'
            />
        </div>;
    }

    if (showEditPage) {
        return (
            <div>
                <center>
                    <button type='submit' className='button-brown' onClick={onBack}>Back</button>
                    <br/>
                    <EditFacility user={user} onLogout={onLogout} facilityName={EditFacilityName} facilityID={EditFacilityID}/>
                </center>
            </div>
        )
    } else {
        return (
            <div>
                <center>
                    <div>
                        <select value={filterBy} onChange={handleSetFilterBy}>
                            <option value='total_population'>Total Customers</option>
                            <option value='total_income'>Income</option>
                        </select>

                        <select value={filteringCriteria} onChange={handleSetFilterCriteria}>
                            <option value='='>Equals</option>
                            <option value='<'>Less than</option>
                            <option value='>'>Greater than</option>
                        </select>

                        <input
                            placeholder='Amount'
                            style={{width: '30%'}}
                            onChange={e => setFilteringNumber(e.target.value)}
                        />

                        <button type='submit' className='button-green' onClick={onFilter}>Search</button>
                    </div>

                    {subList.map((item) => (
                        <FacilityEntry
                            facilityID={item.facility_id}
                            facilityName={item.name}
                            facilityOccupancy={item.occupancy}
                            facilityIncome={item.income}
                            facilityPopulation={item.population}
                            onEdit={onEdit}
                            onDelete={onDelete}
                        />
                    ))}
                    <ReactPaginate
                        pageCount={pageCount}
                        onPageChange={handlePageChange}
                        forcePage={currentPage}
                        previousLabel={'Prev'}
                        nextLabel={'Next'}
                        containerClassName={'pagination'}
                        pageLinkClassName={'page-number'}
                        previousLinkClassName={'page-number'}
                        nextLinkClassName={'page-number'}
                        activeLinkClassName={'active'}
                    />
                </center>
            </div>
        );
    }
}
