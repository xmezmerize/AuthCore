
from datetime import datetime
import uuid


class verify_helpers:
    def _is_valid_uuid(self, value: str) -> bool:
        try:
            uuid.UUID(str(value))
            return True
        except:
            return False

    def _try_parse_date(self, value: str):
        if not value: return None
        clean_value = value.replace('\\', '').strip().split(' ')[0] 
        
        for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d'):
            try:
                return datetime.strptime(clean_value, fmt).date()
            except ValueError:
                continue
        return None
