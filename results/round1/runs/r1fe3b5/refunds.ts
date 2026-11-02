// Computes the refund for a cancelled order.

/** Epoch milliseconds. */
export type Timestamp = number;

export interface Item {
  /** Unit price in cents. */
  priceCents: number;
  quantity: number;
  /** Shipped items are not refundable. */
  shipped: boolean;
}

export interface RefundPolicy {
  /** Percentage of the refundable amount charged as a late fee. */
  lateFeePct: number;
}

export interface Order {
  paidAt: Timestamp;
  items: readonly Item[];
  policy: RefundPolicy;
}

export interface RefundResult {
  /** Amount to return to the customer, in cents. */
  amountCents: number;
  /** Late fee withheld, in cents. */
  fee: number;
}

export function refund(order: Order, cancelledAt: Timestamp): RefundResult {
  const hours = (cancelledAt - order.paidAt) / 3_600_000;
  const items = order.items.filter((i) => !i.shipped);
  const amount = items.reduce((sum, i) => sum + i.priceCents * i.quantity, 0);
  if (hours <= 24) return { amountCents: amount, fee: 0 };
  const fee = Math.round((amount * order.policy.lateFeePct) / 100);
  return { amountCents: amount - fee, fee };
}

export function totalRefunded(refunds: readonly RefundResult[]): number {
  return refunds.reduce((sum, r) => sum + r.amountCents, 0);
}
