const MINUTE = 60 * 1000;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;

function plural(n, singular, pluralForm) {
  return `${n} ${n === 1 ? singular : pluralForm}`;
}

function relativeTime(date, now) {
  const diff = Math.max(0, now.getTime() - date.getTime());
  if (diff < MINUTE) return "hace unos segundos";
  if (diff < HOUR) return `hace ${plural(Math.floor(diff / MINUTE), "minuto", "minutos")}`;
  if (diff < DAY) return `hace ${plural(Math.floor(diff / HOUR), "hora", "horas")}`;
  return `hace ${plural(Math.floor(diff / DAY), "día", "días")}`;
}

export function notificationText(event, now = new Date()) {
  return `${event.user} ${event.action} ${relativeTime(event.at, now)}`;
}
