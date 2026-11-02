import { test } from "node:test";
import assert from "node:assert/strict";
import { notificationText } from "./notify.js";

const now = new Date("2026-10-30T12:00:00Z");
const ago = (ms) => new Date(now.getTime() - ms);
const ev = (at) => ({ user: "ana", action: "pagó", at });
const MIN = 60_000, H = 3_600_000, D = 86_400_000;

test("minutos", () => {
  assert.equal(notificationText(ev(ago(3 * MIN)), now), "ana pagó hace 3 minutos");
  assert.equal(notificationText(ev(ago(1 * MIN)), now), "ana pagó hace 1 minuto");
});
test("horas", () => {
  assert.equal(notificationText(ev(ago(2 * H)), now), "ana pagó hace 2 horas");
  assert.equal(notificationText(ev(ago(1 * H)), now), "ana pagó hace 1 hora");
});
test("días", () => {
  assert.equal(notificationText(ev(ago(5 * D)), now), "ana pagó hace 5 días");
  assert.equal(notificationText(ev(ago(1 * D)), now), "ana pagó hace 1 día");
});
test("menos de un minuto y fechas futuras", () => {
  assert.equal(notificationText(ev(ago(10_000)), now), "ana pagó hace un momento");
  assert.equal(notificationText(ev(new Date(now.getTime() + 5000)), now), "ana pagó hace un momento");
});
test("usa la hora actual por defecto", () => {
  const txt = notificationText({ user: "ana", action: "pagó", at: new Date(Date.now() - 2 * H) });
  assert.equal(txt, "ana pagó hace 2 horas");
});
