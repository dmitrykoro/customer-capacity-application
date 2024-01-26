

class CustomerService:
    def __init__(
            self,
            dbapi
    ):
        self.dbapi = dbapi

    def ensure_can_be_checked_in(
            self,
            document_id: str,
            facility_id: str
    ) -> dict:

        facility_is_full = self.dbapi.facility.is_full(facility_id)
        if facility_is_full:
            return dict(error='facility-is-full')

        is_already_checked_in = self.dbapi.customer_visit.is_open(document_id)
        if is_already_checked_in:
            return dict(error='customer-already-checked-in')

        return dict(success=True)

    def do_check_in(
            self,
            facility_id: str,
            name: str,
            document_id: str,
            age: int
    ) -> dict:

        try:
            self.dbapi.customer_visit.create_one(
                name=name,
                document_id=document_id,
                age=age,
                facility_id=facility_id
            )
            return dict(success=True)

        except Exception as e:
            return dict(error=e)

    def ensure_can_be_checked_out(
            self,
            document_id: str
    ) -> dict:

        is_checked_in = self.dbapi.customer_visit.is_open(document_id)
        if not is_checked_in:
            return dict(error='customer-does-not-exist')

        return dict(success=True)

    def do_check_out(
            self,
            document_id: str,
            charge: float
    ) -> dict:
        try:
            self.dbapi.customer_visit.check_out(
                document_id=document_id,
                charge=charge
            )
            return dict(success=True)

        except Exception as e:
            return dict(error=e)
