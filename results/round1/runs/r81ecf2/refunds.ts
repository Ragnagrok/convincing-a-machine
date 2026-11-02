// Computes the refund for a cancelled order.

/** Millisecond timestamp (e.g. `Date.now()` or `date.getTime()`). */
export type EpochMs = number;

/** Refund policy attached to an order. */
export interface RefundPolicy {
  /** Percentage (0-100) withheld as a fee when cancelling after the grace window. */
  lateFeePct: number;
}

/** A line item in an order. */
export interface OrderItem {
  /** Unit price in cents. */
  priceCents: number;
  quantity: number;
  /** Items already shipped are not refundable. */
  shipped: boolean;
}

/** An order that may be cancelled and refunded. */
export interface Order {
  /** When the order was paid, in epoch milliseconds. */
  paidAt: EpochMs;
  items: OrderItem[];
  policy: RefundPolicy;
}

/** Result of refunding a cancelled order. */
export interface RefundResult {
  /** Amount returned to the customer, in cents. */
  amountCents: number;
  /** Fee withheld from the refund, in cents. */
  fee: number;
}

/** Computes the refund for a cancelled order. */
export function refund(order: Order, cancelledAt: EpochMs): RefundResult {
  const hours = (cancelledAt - order.paidAt) / 3_600_000;
  const items = order.items.filter((i) => !i.shipped);
  const amount = items.reduce((sum, i) => sum + i.priceCents * i.quantity, 0);
  if (hours <= 24) return { amountCents: amount, fee: 0 };
  const fee = Math.round((amount * order.policy.lateFeePct) / 100);
  return { amountCents: amount - fee, fee };
}

/** Sums the refunded amounts (in cents) of a list of refund results. */
export function totalRefunded(refunds: readonly RefundResult[]): number {
  return refunds.reduce((sum, r) => sum + r.amountCents, 0);
}
