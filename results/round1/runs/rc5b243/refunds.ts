// Computes the refund for a cancelled order.

/** Timestamps are epoch milliseconds. */
export type EpochMs = number;

/** Refund policy attached to an order. `lateFeePct` is a percentage (0-100). */
export interface RefundPolicy {
  lateFeePct: number;
}

/** A line item in an order. `priceCents` is the unit price. */
export interface OrderItem {
  shipped: boolean;
  priceCents: number;
  quantity: number;
}

export interface Order {
  paidAt: EpochMs;
  items: OrderItem[];
  policy: RefundPolicy;
}

/** Result of `refund`: the amount to return and the late fee withheld. */
export interface RefundResult {
  amountCents: number;
  fee: number;
}

const MS_PER_HOUR = 3_600_000;
const REFUND_WINDOW_HOURS = 24;

export function refund(order: Order, cancelledAt: EpochMs): RefundResult {
  const hours = (cancelledAt - order.paidAt) / MS_PER_HOUR;
  const items = order.items.filter((i) => !i.shipped);
  const amount = items.reduce((sum, i) => sum + i.priceCents * i.quantity, 0);
  if (hours <= REFUND_WINDOW_HOURS) return { amountCents: amount, fee: 0 };
  const fee = Math.round((amount * order.policy.lateFeePct) / 100);
  return { amountCents: amount - fee, fee };
}

export function totalRefunded(refunds: RefundResult[]): number {
  return refunds.reduce((sum, r) => sum + r.amountCents, 0);
}
