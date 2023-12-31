import React from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);

const myEventsList = [
    {
        title: "Evento 1",
        start: new Date("2023-09-15T10:00:00"),
        end: new Date("2023-09-15T12:00:00"),
    },
    {
        title: "Evento 2",
        start: new Date("2023-09-16T14:00:00"),
        end: new Date("2023-09-16T16:00:00"),
    },
];

function MyCalendar() {
    return (
        <div>
            <Calendar
                localizer={localizer}
                events={myEventsList}
                startAccessor="start"
                endAccessor="end"
                style={{ height: 500 }}
            />
        </div>
    );
}

export default MyCalendar;