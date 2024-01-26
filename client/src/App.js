import React, { useState, useEffect } from 'react';
import { CookiesProvider, useCookies } from 'react-cookie';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import LoginPage from './LoginPage.js';
import HomePage from './HomePage.js';
import RegisterFacility from "./admin/RegisterFacility";
import ManageFacilities from "./admin/ManageFacilities";


function App() {
    const [cookies, setCookie, removeCookie] = useCookies(['user']);
    const [isLoggedIn, setIsLoggedIn] = useState(!!cookies.user);
    const [role, setRole] = useState('');

    function handleLogin(user) {
        setCookie('user', user, { path: '/' });
        setIsLoggedIn(true);
        setRole(user.dataJson.role);
    }

    function handleLogout() {
        removeCookie('user', { path: '/' })
        setIsLoggedIn(false);
        setRole('');
    }

    return (
        <CookiesProvider>
                    <Routes>
                        <Route path="/" element={
                            isLoggedIn ? (
                                <HomePage user={cookies.user} onLogout={handleLogout} />
                            ) : (
                                <LoginPage onLogin={handleLogin} />
                            )}
                        />
                        <Route path="/register-facility" element={
                            isLoggedIn ? (
                                <RegisterFacility user={cookies.user} onLogout={handleLogout}/>
                            ) : (
                                <LoginPage onLogin={handleLogin} />
                            )}
                        />
                        <Route path="/manage-facilities" element={
                            isLoggedIn ? (
                                    <ManageFacilities user={cookies.user} onLogout={handleLogout}/>
                            ) : (
                                <LoginPage onLogin={handleLogin} />
                            )}
                        />
                    </Routes>
        </CookiesProvider>
    );
}

function MC(){
    return (
        <Router>
            <App />
        </Router>
    );
}

export default MC;
