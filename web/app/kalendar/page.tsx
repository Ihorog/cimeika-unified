export default function KalendarPage() {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const firstDay = (new Date(year, month, 1).getDay() + 6) % 7;
  const today = now.getDate();
  const monthNames = ['Січень','Лютий','Березень','Квітень','Травень','Червень','Липень','Серпень','Вересень','Жовтень','Листопад','Грудень'];
  const dayNames = ['Пн','Вт','Ср','Чт','Пт','Сб','Нд'];
  const cells: (number | null)[] = [...Array(firstDay).fill(null), ...Array.from({ length: daysInMonth }, (_, i) => i + 1)];

  return (
    <div className="page-module">
      <div className="module-header">
        <div>
          <h1>Календар</h1>
          <p className="module-subtitle">Час, ритми, вузлові точки</p>
        </div>
      </div>
      <div className="calendar">
        <h2 className="calendar-title">{monthNames[month]} {year}</h2>
        <div className="calendar-grid">
          {dayNames.map(d => <div key={d} className="cal-dayname">{d}</div>)}
          {cells.map((d, i) => <div key={i} className={`cal-cell${d === today ? ' cal-cell--today' : ''}${!d ? ' cal-cell--empty' : ''}`}>{d}</div>)}
        </div>
      </div>
    </div>
  );
}
