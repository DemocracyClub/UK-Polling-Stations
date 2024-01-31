from councils.models import Council
from data_importers.event_types import DataEventType
from data_importers.models import DataEvent


def record_teardown_event(council_id):
    DataEvent.objects.create(
        council=Council.objects.get(council_id=council_id),
        event_type=DataEventType.TEARDOWN,
    )
