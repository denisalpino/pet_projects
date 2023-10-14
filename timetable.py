from datetime import datetime, timedelta

class Lecture:
    """This class describes some performance"""

    def __init__(self, title: str, start_time: str, duration: str) -> None:
        duration = datetime.strptime(duration, '%H:%M')
        self.title = title
        self.start = datetime.strptime(start_time, '%H:%M')
        self.duration = timedelta(hours=duration.hour, minutes=duration.minute)
        self.end = self.start + self.duration

class Conference:
    """A class describing a one-day conference. A conference is a set of
    consecutive presentations
    """

    def __init__(self) -> None:
        self.timetable = []

    def add(self, lecture: Lecture) -> None:
        """Method that takes a performance as an argument and adds it to
        the conference. If a speech overlaps in time with other speeches,
        a ValueError exception should be raised
        """
        if self.timetable:
            if any(
                any([
                    l.end > lecture.start > l.start,
                    l.start < lecture.end < l.end,
                    lecture.start <= l.start and lecture.end >= l.end
                    ])
                for l in self.timetable
                ):
                raise ValueError('Провести выступление в это время невозможно')
        self.timetable.append(lecture)

    def total(self) -> str:
        """Returns the total duration of all lectures as a string in the format HH:MM"""

        return self.formater(sum([l.duration for l in self.timetable], timedelta()).total_seconds())

    def longest_lecture(self) -> str:
        """Returns the duration of the longest lectures as a string in the format HH:MM"""

        return self.formater(max(l.duration for l in self.timetable).total_seconds())

    def longest_break(self) -> str:
        """Returns the duration of the longest break between lectures as a string in the format HH:MM"""

        srt = sorted(self.timetable, key=lambda x: x.start)
        longest = max(second.start - first.end for first, second in zip(srt[:-1], srt[1:])).total_seconds()
        return self.formater(longest)

    @staticmethod
    def formater(td: timedelta) -> str:
        h, m = (td // 60) // 60, (td // 60) % 60
        return datetime(1, 1, 1, int(h), int(m)).strftime('%H:%M')