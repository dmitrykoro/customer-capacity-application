from flask import Flask
from flask_restful import Api

from api.controllers.management import Init, Version
from api.controllers.account import Account
from api.controllers.login import Login
from api.controllers.logout import Logout
from api.controllers.customer import Customer
from api.controllers.manage_facilities import ManageFacilities
from api.controllers.facility import Facility

from dbapi.capacity_database_api import CapacityDatabaseAPI
from api.services.auth_service import AuthenticationService


capacity_dbapi = CapacityDatabaseAPI(reinitialize_schema=False, install_accounts=False)
auth_service = AuthenticationService(capacity_dbapi)

app = Flask(__name__)
api = Api(app)

# Management API for initializing the DB
api.add_resource(
    Init,
    '/manage/init',
    resource_class_kwargs={'dbapi': capacity_dbapi}
)

# Management API for getting version
api.add_resource(
    Version,
    '/manage/version',
    resource_class_kwargs={'dbapi': capacity_dbapi}
)

# Get full Account info or create Account
api.add_resource(
    Account,
    '/accounts/<string:account_id>',    # get full Account info
    '/accounts/create',                 # create Account
    resource_class_kwargs={'dbapi': capacity_dbapi}
)

# Authenticate and authorize a user
api.add_resource(
    Login,
    '/login',
    resource_class_kwargs={'dbapi': capacity_dbapi, 'auth_service': auth_service}
)

# Remove a session key for a user
api.add_resource(
    Logout,
    '/logout',
    resource_class_kwargs={'dbapi': capacity_dbapi, 'auth_service': auth_service}
)

# Check-in or check-out a customer
api.add_resource(
    Customer,
    '/customer/<string:action>',
    resource_class_kwargs={'dbapi': capacity_dbapi, 'auth_service': auth_service}
)

# Manage facilities
api.add_resource(
    ManageFacilities,
    '/manage-facilities/<string:action>',
    resource_class_kwargs={'dbapi': capacity_dbapi, 'auth_service': auth_service}
)

# Register a new facility or update facility info
api.add_resource(
    Facility,
    '/facility',
    resource_class_kwargs={'dbapi': capacity_dbapi, 'auth_service': auth_service}
)


if __name__ == '__main__':
    app.run(debug=True, port=4999)
