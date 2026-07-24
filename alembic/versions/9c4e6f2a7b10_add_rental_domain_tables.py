"""add rental domain tables

Revision ID: 9c4e6f2a7b10
Revises: 6a2b07f05783
"""
from alembic import op
import sqlalchemy as sa

revision = "9c4e6f2a7b10"
down_revision = "6a2b07f05783"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("units", sa.Column("id", sa.Integer, primary_key=True), sa.Column("property_id", sa.Integer, sa.ForeignKey("properties.id"), nullable=False), sa.Column("unit_number", sa.String(50), nullable=False), sa.Column("bedrooms", sa.Integer, nullable=False), sa.Column("bathrooms", sa.Numeric(3, 1), nullable=False), sa.Column("monthly_rent", sa.Numeric(12, 2), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime, nullable=False), sa.UniqueConstraint("property_id", "unit_number", name="uq_unit_property_number"))
    op.create_index("ix_units_property_id", "units", ["property_id"])
    op.create_table("leases", sa.Column("id", sa.Integer, primary_key=True), sa.Column("unit_id", sa.Integer, sa.ForeignKey("units.id"), nullable=False), sa.Column("tenant_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False), sa.Column("start_date", sa.Date, nullable=False), sa.Column("end_date", sa.Date, nullable=False), sa.Column("monthly_rent", sa.Numeric(12, 2), nullable=False), sa.Column("deposit_amount", sa.Numeric(12, 2), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime, nullable=False))
    op.create_index("ix_leases_unit_id", "leases", ["unit_id"]); op.create_index("ix_leases_tenant_id", "leases", ["tenant_id"])
    op.create_table("payments", sa.Column("id", sa.Integer, primary_key=True), sa.Column("lease_id", sa.Integer, sa.ForeignKey("leases.id"), nullable=False), sa.Column("amount", sa.Numeric(12, 2), nullable=False), sa.Column("paid_on", sa.Date, nullable=False), sa.Column("method", sa.String(40), nullable=False), sa.Column("reference", sa.String(100), unique=True), sa.Column("status", sa.String(20), nullable=False), sa.Column("notes", sa.Text), sa.Column("created_at", sa.DateTime, nullable=False))
    op.create_index("ix_payments_lease_id", "payments", ["lease_id"])
    op.create_table("expenses", sa.Column("id", sa.Integer, primary_key=True), sa.Column("property_id", sa.Integer, sa.ForeignKey("properties.id"), nullable=False), sa.Column("category", sa.String(80), nullable=False), sa.Column("amount", sa.Numeric(12, 2), nullable=False), sa.Column("incurred_on", sa.Date, nullable=False), sa.Column("description", sa.Text), sa.Column("created_at", sa.DateTime, nullable=False))
    op.create_index("ix_expenses_property_id", "expenses", ["property_id"])
    op.create_table("maintenance_requests", sa.Column("id", sa.Integer, primary_key=True), sa.Column("property_id", sa.Integer, sa.ForeignKey("properties.id"), nullable=False), sa.Column("unit_id", sa.Integer, sa.ForeignKey("units.id")), sa.Column("requested_by_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False), sa.Column("title", sa.String(160), nullable=False), sa.Column("description", sa.Text, nullable=False), sa.Column("priority", sa.String(20), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime, nullable=False))
    op.create_index("ix_maintenance_requests_property_id", "maintenance_requests", ["property_id"]); op.create_index("ix_maintenance_requests_unit_id", "maintenance_requests", ["unit_id"])
    op.create_table("notifications", sa.Column("id", sa.Integer, primary_key=True), sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False), sa.Column("title", sa.String(160), nullable=False), sa.Column("message", sa.Text, nullable=False), sa.Column("notification_type", sa.String(40), nullable=False), sa.Column("is_read", sa.Boolean, nullable=False), sa.Column("created_at", sa.DateTime, nullable=False))
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_table("documents", sa.Column("id", sa.Integer, primary_key=True), sa.Column("uploaded_by_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False), sa.Column("lease_id", sa.Integer, sa.ForeignKey("leases.id")), sa.Column("property_id", sa.Integer, sa.ForeignKey("properties.id")), sa.Column("filename", sa.String(255), nullable=False), sa.Column("path", sa.String(500), nullable=False), sa.Column("document_type", sa.String(50), nullable=False), sa.Column("created_at", sa.DateTime, nullable=False))
    op.create_index("ix_documents_lease_id", "documents", ["lease_id"]); op.create_index("ix_documents_property_id", "documents", ["property_id"])
    op.create_table("invoices", sa.Column("id", sa.Integer, primary_key=True), sa.Column("lease_id", sa.Integer, sa.ForeignKey("leases.id"), nullable=False), sa.Column("invoice_number", sa.String(50), nullable=False, unique=True), sa.Column("amount", sa.Numeric(12, 2), nullable=False), sa.Column("due_date", sa.Date, nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime, nullable=False))
    op.create_index("ix_invoices_lease_id", "invoices", ["lease_id"])
    op.create_table("audit_logs", sa.Column("id", sa.Integer, primary_key=True), sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")), sa.Column("action", sa.String(100), nullable=False), sa.Column("entity_type", sa.String(80), nullable=False), sa.Column("entity_id", sa.Integer), sa.Column("details", sa.JSON), sa.Column("created_at", sa.DateTime, nullable=False))
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])


def downgrade():
    for table in ("audit_logs", "invoices", "documents", "notifications", "maintenance_requests", "expenses", "payments", "leases", "units"):
        op.drop_table(table)
