function tiempoRelativo(desde, ahora) {
  const segundos = Math.max(0, Math.floor((ahora - desde) / 1000));
  const minutos = Math.floor(segundos / 60);
  if (minutos < 1) return "hace un momento";
  if (minutos < 60) return `hace ${minutos} ${minutos === 1 ? "minuto" : "minutos"}`;
  const horas = Math.floor(minutos / 60);
  if (horas < 24) return `hace ${horas} ${horas === 1 ? "hora" : "horas"}`;
  const dias = Math.floor(horas / 24);
  return `hace ${dias} ${dias === 1 ? "día" : "días"}`;
}

export function notificationText(event, now = new Date()) {
  const base = `${event.user} ${event.action}`;
  if (!(event.at instanceof Date)) return base;
  return `${base} ${tiempoRelativo(event.at, now)}`;
}
