import React, { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid'; // Import timeGridPlugin
import axios from 'axios';
import './App.css'

const App = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    axios.get("/api/availability").then(response => {
	console.log(response.data);
      const formattedEvents = response.data.map(item => ({
        title: item.court.split("_").join(" "),
        start: `${item.date}T${String(item.start).padStart(2, '0')}:00:00`,
        end: `${item.date}T${String(item.end).padStart(2, '0')}:00:00`,
        backgroundColor: item.slots>0 ? "green" : "red",
        url: item.url
        // className: 'half-width-event' // Add custom class to events
      }));
      setEvents(formattedEvents);
    });
  }, []);

  const renderEventContent = (eventInfo) => {
    return (
      <div>
        <div style={{ fontSize: '0.8em', fontWeight: 'bold' }}>{eventInfo.timeText}</div>
        <div style={{ fontSize: '0.8em' }}>{eventInfo.event.title}</div>
      </div>
    );
  };
  
  const handleEventClassNames = (arg) => {
    // Detect overlapping events manually
    const eventStart = new Date(arg.event.start).getTime();
  
    const isOverlapping = events.some((e) => {
      const otherStart = new Date(e.start).getTime();
      return (
        e.title !== arg.event.title && // Exclude the current event
        eventStart === otherStart
      );
    });
  
    // Apply the 'half-width-event' class to all overlapping events
    return isOverlapping ? ['half-width-event'] : [];
  };

  const handleEventClick = (clickInfo) => {
    // Open the booking link in a new tab
    if (clickInfo.event.extendedProps.url) {
      window.open(clickInfo.event.extendedProps.url, '_blank');
    }
  };

  return (
    <div>
      <h1>Tennis Court Availability</h1>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin]} // Use both plugins
        initialView="timeGridWeek" // Set to monthly view
        events={events}
        slotMinTime="00:00:00" // Start the grid at midnight
        slotMaxTime="24:00:00" // End the grid at midnight of the next day
        eventTimeFormat={{
          hour: '2-digit',
          minute: '2-digit',
          hour12: false,
          meridiem: false, // Use 24-hour format
        }} // Show time details for events
        eventDisplay="block" // Ensure events are displayed as blocks
        eventContent={renderEventContent}
        eventClassNames={handleEventClassNames}
        eventClick={handleEventClick}
        eventOverlap={false}
      />
    </div>
  );
};

export default App;

