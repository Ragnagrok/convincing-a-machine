// Computes the refund for a cancelled order.

/** Monetary amount in cents (integer). */
export type Cents = number;

/** Timestamp in milliseconds since the Unix epoch (same as `Date#getTime()`). */
export type EpochMs = number;

export interface OrderItem {
  readonly priceCents: Cents;
  readonly quantity: number;
  /** Shipped items are not refundable. */
  readonly shipped: boolean;
}

export interface RefundPolicy {
  /** Percentage (0-100) withheld as a fee when cancelling after the free window. */
  readonly lateFeePct: number;
}

export interface Order {
  readonly paidAt: EpochMs;
  readonly items: readonly OrderItem[];
  readonly policy: RefundPolicy;
}

export interface RefundResult {
  readonly amountCents: Cents;
  readonly fee: Cents;
}

export function refund(order: Order, cancelledAt: EpochMs): RefundResult {
  const hours = (cancelledAt - order.paidAt) / 3_600_000;
  const items = order.items.filter((i) => !i.shipped);
  const amount = items.reduce((sum, i) => sum + i.priceCents * i.quantity, 0);
  if (hours <= 24) return { amountCents: amount, fee: 0 };
  const fee = Math.round((amount * order.policy.lateFeePct) / 100);
  return { amountCents: amount - fee, fee };
}

export function totalRefunded(refunds: readonly RefundResult[]): Cents {
  return refunds.reduce((sum, r) => sum + r.amountCents, 0);
}
