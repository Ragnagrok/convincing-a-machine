import * as o from './orig.mjs';
import * as n from './new.mjs';
const H = 3_600_000;
const cases = [];
for (const hrs of [0, 5, 24, 24.5, 100]) for (const pct of [0, 10, 33]) for (const ship of [false, true]) {
  const order = { paidAt: 1_000_000_000, items: [{ priceCents: 1999, quantity: 3, shipped: ship }, { priceCents: 250, quantity: 2, shipped: false }], policy: { lateFeePct: pct } };
  cases.push([order, order.paidAt + hrs * H]);
}
let bad = 0;
for (const [ord, t] of cases) if (JSON.stringify(o.refund(ord, t)) !== JSON.stringify(n.refund(ord, t))) bad++;
const rs = [{ amountCents: 5, fee: 1 }, { amountCents: 7, fee: 0 }];
console.log('cases', cases.length, 'mismatches', bad, 'total', n.totalRefunded(rs) === o.totalRefunded(rs));
