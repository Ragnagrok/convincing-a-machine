function relativeTime(date, now) {
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  if (seconds < 60) return "hace un momento";

  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `hace ${minutes} ${minutes === 1 ? "minuto" : "minutos"}`;

  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `hace ${hours} ${hours === 1 ? "hora" : "horas"}`;

  const days = Math.floor(hours / 24);
  return `hace ${days} ${days === 1 ? "día" : "días"}`;
}

export function notificationText(event, now = new Date()) {
  return `${event.user} ${event.action} ${relativeTime(event.at, now)}`;
}
