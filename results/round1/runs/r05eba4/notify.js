function plural(n, singular, pluralForm) {
  return `${n} ${n === 1 ? singular : pluralForm}`;
}

// Tiempo relativo en español: "hace un momento", "hace 3 minutos", "hace 2 horas", "hace 5 días".
export function timeAgo(date, now = new Date()) {
  const elapsedMs = Math.max(0, Number(now) - Number(date));
  const minutes = Math.floor(elapsedMs / 60_000);
  if (minutes < 1) return 'hace un momento';
  if (minutes < 60) return `hace ${plural(minutes, 'minuto', 'minutos')}`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `hace ${plural(hours, 'hora', 'horas')}`;
  const days = Math.floor(hours / 24);
  return `hace ${plural(days, 'día', 'días')}`;
}

export function notificationText(event, now = new Date()) {
  const base = `${event.user} ${event.action}`;
  if (!(event.at instanceof Date) || Number.isNaN(event.at.getTime())) return base;
  return `${base} ${timeAgo(event.at, now)}`;
}
