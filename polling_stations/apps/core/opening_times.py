import datetime
from datetime import date, time
from typing import Dict, List

from typing_extensions import OrderedDict


class OpeningTimes:
    __slots__ = ("dates", "date_fmt", "time_fmt")

    def __init__(self, date_fmt: str = None, time_fmt: str = None, tz=None):
        self.dates: Dict[date, List] = OrderedDict()
        if not date_fmt:
            date_fmt = "%Y-%m-%d"
        self.date_fmt = date_fmt
        if not time_fmt:
            time_fmt = "%H:%M"
        self.time_fmt = time_fmt

    def add_date(self, date: date) -> List:
        if not date in self.dates:
            self.dates[date]: List[time, time] = []
        return self.dates[date]

    def _parse_time(self, open_date, time):
        return datetime.datetime.strptime(
            f"{open_date} {time}", "%Y-%m-%d %H:%M"
        ).time()

    def add_open_time(self, open_date: str, open_time: str, close_time: str) -> None:
        open_date = datetime.datetime.strptime(open_date, "%Y-%m-%d").date()
        open_time = self._parse_time(open_date, open_time)
        close_time = self._parse_time(open_date, close_time)
        date = self.add_date(open_date)
        date.append((open_time, close_time))
        date.sort(key=lambda open_close: open_close[0])

    def as_string_table(self):
        return self.as_table(stringify=True)

    @classmethod
    def from_dict(cls, opening_times_dict):
        klass = cls()
        for row in opening_times_dict:
            klass.add_open_time(*row)
        return klass

    def as_table(self, stringify=False):
        table = []
        for open_date in sorted(self.dates.keys()):
            times = self.dates[open_date]
            for open_close in times:
                row = []
                if stringify:
                    row.append(open_date.strftime(self.date_fmt))
                    row.append(open_close[0].strftime(self.time_fmt))
                    row.append(open_close[1].strftime(self.time_fmt))
                else:
                    row.append(open_date)
                    row.append(open_close[0])
                    row.append(open_close[1])
                table.append(row)
        return table

    def __str__(self):
        return "\n".join(
            "\t".join(open_close for open_close in open_date)
            for open_date in self.as_string_table()
        )
