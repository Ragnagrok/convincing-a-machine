const MINUTE = 60 * 1000;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;

function hace(n, singular, plural) {
  return `hace ${n} ${n === 1 ? singular : plural}`;
}

export function relativeTime(at, now = new Date()) {
  const diff = Math.max(0, now.getTime() - at.getTime());
  if (diff < MINUTE) return "hace menos de un minuto";
  if (diff < HOUR) return hace(Math.floor(diff / MINUTE), "minuto", "minutos");
  if (diff < DAY) return hace(Math.floor(diff / HOUR), "hora", "horas");
  return hace(Math.floor(diff / DAY), "día", "días");
}

export function notificationText(event, now = new Date()) {
  return `${event.user} ${event.action} ${relativeTime(event.at, now)}`;
}
