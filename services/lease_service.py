from extensions import db
from models.lease import Lease


def close_expired_leases(today):
    expired = Lease.query.filter(Lease.status == "active", Lease.end_date < today).all()
    for lease in expired:
        lease.status = "expired"
        lease.unit.status = "vacant"
    db.session.commit()
    return len(expired)
