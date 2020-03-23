import logging


class StatusCheckFilter(logging.Filter):
    def filter(self, record):
        if (
            record.status_code == 503
            and hasattr(record, "request")
            and "status_check" in record.request.path
        ):
            return False
        return True
