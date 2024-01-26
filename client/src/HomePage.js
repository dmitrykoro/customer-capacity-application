import React, { useState } from 'react';

import BouncerPage from './bouncer/BouncerHome.js';
import AdminPage from './admin/AdminHome.js';

export default function HomePage({ user , onLogout }) {

    function Logout() {
        onLogout();
    }

    if ( user.dataJson.role === 'bouncer') {
        return <BouncerPage user={user} onLogout={Logout}/>
    }
    else if (user.dataJson.role === 'admin') {
        return <AdminPage user={user} onLogout={Logout}/>
    }
}