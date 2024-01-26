# Client-Server Web Application Overview

This is an example of a simple client-server web application designed as an imaginary customer capacity 
management system. The application comprises a React client interacting with a Python backend server that 
encapsulates the underlying database schema.

## System Components

### React Client Application
- The client application is built using React and serves as the user interface for interacting with the database.

### Python Backend Server
- The Python backend server handles requests for the UI.

### Database Schema
- The database schema stores information about facilities, representing various 
businesses or organizations, along with their respective defined maximum capacities.

## Roles and Functionality

### Roles
1. **Administrator:**
    - The Administrator role has privileged access to all facilities in the system.
    - Administrator can edit or delete existing facilities.
    - Administrator can register new facilities into the system.

2. **Bouncer:**
    - The Bouncer role is responsible for managing customer check-ins and check-outs.
    - Bouncer can not register a new customer when a facility is full.


# Project Setup and Execution Guide

## Backend Server
1. **Create a Virtual Environment:**
    - Set up a virtual environment with the required packages from `requirements.txt`.

        ```bash
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```

2. **Start Backend Server:**
    - Execute the following script to start the backend server:

        ```bash
        ./runserver.sh
        ```

    - The backend server runs on port 4999.

## Client Application
1. **Install React:**
    - Install React for the client-side.

        ```bash
        npm install -g create-react-app
        ```

2. **Run Client Application:**
    - Execute the following script to start the client app:

        ```bash
        ./runclient.sh
        ```

    - The client app runs on port 3000.

## Accessing the Application
- Access the application in the browser by visiting:

    ```bash
    https://<server_ip>:3000
    ```

## Database Initialization
1. **Initialize Database Schema:**
    - Before the first run, initialize the database schema.

        ```bash
        ./init_schema.sh
        ```

2. **Generate Default Data:**
    - Install default accounts and a default facility "Nightclub" with the script `generate_data.sh`.

        ```bash
        ./generate_data.sh
        ```

    - This script can also be used to re-install accounts and reset Nightclub data.

## Default Accounts
- Default accounts for the admin and bouncer roles are pre-installed with the following credentials:

  **Admin:**
    - Username: a
    - Password: p

  **Bouncer:**
    - Username: b
    - Password: p

    - The bouncer account is associated with the default "Nightclub" facility, so customer check-ins/outs will be linked to that facility.

## Database API Tests
- Run tests for the database API using the following script:

    ```bash
    ./starttests.sh
    ```

- Note: Starting tests will erase the data in the database.
