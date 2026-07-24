from datetime import date, datetime


def parse_date(value, field):
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError(f"{field} must use YYYY-MM-DD format")


def pagination(query, page, per_page):
    page = max(int(page or 1), 1)
    per_page = min(max(int(per_page or 20), 1), 100)
    result = query.paginate(page=page, per_page=per_page, error_out=False)
    return result.items, {"page": page, "per_page": per_page, "total": result.total, "pages": result.pages}
