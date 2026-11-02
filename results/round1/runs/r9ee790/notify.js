const MINUTE = 60 * 1000;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;

function relativeTime(at, now) {
  const elapsed = Math.max(0, now.getTime() - at.getTime());

  if (elapsed < MINUTE) return "hace un momento";

  const plural = (n, unit) => `hace ${n} ${unit}${n === 1 ? "" : "s"}`;

  if (elapsed < HOUR) return plural(Math.floor(elapsed / MINUTE), "minuto");
  if (elapsed < DAY) return plural(Math.floor(elapsed / HOUR), "hora");
  return plural(Math.floor(elapsed / DAY), "día");
}

export function notificationText(event, now = new Date()) {
  return `${event.user} ${event.action} ${relativeTime(event.at, now)}`;
}
