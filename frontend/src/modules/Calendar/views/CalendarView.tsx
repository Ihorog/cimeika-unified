/**
 * Calendar module main view
 * UI orchestration without business logic
 */
import React from 'react';
import { useCalendar } from '../hooks/useCalendar';

const CalendarView: React.FC = () => {
  const { status } = useCalendar();

  return (
    <div className="calendar-view">
      <h1>Календар - Час</h1>
      <p>Status: {status}</p>
    </div>
  );
};

export default CalendarView;
