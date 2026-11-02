// Computes the refund for a cancelled order.

/** Refund policy attached to an order. */
export interface RefundPolicy {
  /** Percentage (0-100) withheld as a fee when cancelled after the grace window. */
  lateFeePct: number;
}

/** A single line item in an order. */
export interface OrderItem {
  /** Unit price in cents. */
  priceCents: number;
  quantity: number;
  /** Shipped items are not refundable. */
  shipped: boolean;
}

/** An order that may be cancelled and refunded. */
export interface Order {
  /** Payment timestamp in milliseconds since the epoch. */
  paidAt: number;
  items: readonly OrderItem[];
  policy: RefundPolicy;
}

/** Outcome of a refund computation. */
export interface RefundResult {
  /** Amount returned to the customer, in cents. */
  amountCents: number;
  /** Fee withheld, in cents. */
  fee: number;
}

const MS_PER_HOUR = 3_600_000;
const FULL_REFUND_WINDOW_HOURS = 24;

export function refund(order: Order, cancelledAt: number): RefundResult {
  const hours = (cancelledAt - order.paidAt) / MS_PER_HOUR;
  const items = order.items.filter((i) => !i.shipped);
  const amount = items.reduce((sum, i) => sum + i.priceCents * i.quantity, 0);
  if (hours <= FULL_REFUND_WINDOW_HOURS) return { amountCents: amount, fee: 0 };
  const fee = Math.round((amount * order.policy.lateFeePct) / 100);
  return { amountCents: amount - fee, fee };
}

export function totalRefunded(refunds: readonly RefundResult[]): number {
  return refunds.reduce((sum, r) => sum + r.amountCents, 0);
}
