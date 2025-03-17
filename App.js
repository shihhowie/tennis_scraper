import React, { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import axios from 'axios';

const App = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    axios.get("http://172.31.24.168:5000/api/availability").then(response => {
      const formattedEvents = response.data.map(item => ({
        title: item.slots>0 ? "Available" : "Fully Booked",
        start: `${item.date}T${String(item.start).padStart(2, '0')}:00:00`,
        backgroundColor: item.slots>0 ? "green" : "red"
      }));
      setEvents(formattedEvents);
    });
  }, []);

  return (
    <div>
      <h1>Tennis Court Availability</h1>
      <FullCalendar plugins={[dayGridPlugin]} initialView="dayGridMonth" events={events} />
    </div>
  );
};

export default App;

