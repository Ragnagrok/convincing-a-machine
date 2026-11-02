// Computes the refund for a cancelled order.
export function refund(order, cancelledAt) {
  const hours = (cancelledAt - order.paidAt) / 3_600_000;
  const items = order.items.filter((i) => !i.shipped);
  const amount = items.reduce((sum, i) => sum + i.priceCents * i.quantity, 0);
  if (hours <= 24) return { amountCents: amount, fee: 0 };
  const fee = Math.round(amount * order.policy.lateFeePct / 100);
  return { amountCents: amount - fee, fee };
}

export function totalRefunded(refunds) {
  return refunds.reduce((sum, r) => sum + r.amountCents, 0);
}
