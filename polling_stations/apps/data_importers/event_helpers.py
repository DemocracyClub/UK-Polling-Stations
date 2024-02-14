from councils.models import Council
from data_importers.event_types import DataEventType
from data_importers.models import DataEvent
from pollingstations.models import PollingStation, VisibilityChoices


class EventValidationError(Exception):
    pass


def record_teardown_event(council_id):
    DataEvent.objects.create(
        council=Council.objects.get(council_id=council_id),
        event_type=DataEventType.TEARDOWN,
    )


def set_station_visibility(event):
    payload = event.payload
    if not (visibility := payload.get("visibility", None)):
        raise EventValidationError(f"{event} payload missing visibility.")
    if visibility not in VisibilityChoices:
        raise EventValidationError(
            f"DataEvent visibility not a valid choice. Visibility was '{visibility}', choices are {VisibilityChoices.choices}."
        )
    try:
        station = PollingStation.objects.get(
            internal_council_id=payload["internal_council_id"],
            council_id=event.council_id,
        )
    except PollingStation.DoesNotExist:
        # If the station doesn't exist this is a no op.
        return
    station.visibility = visibility
    station.save()


def set_station_field_from_event(event: DataEvent):
    if event.event_type not in DataEventType.station_update_event_types():
        raise EventValidationError(
            f"{event} event_type ('{event.event_type}') does not appear in DataEventType.station_update_event_types"
        )
    if not event.payload.get("internal_council_id", None):
        raise EventValidationError(f"{event} payload missing station id.")

    match event.event_type:
        case DataEventType.SET_STATION_VISIBILITY:
            set_station_visibility(event)
        case _:
            pass
