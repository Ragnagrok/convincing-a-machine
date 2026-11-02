// Computes the refund for a cancelled order.
//
// Money is always integer cents. Timestamps are epoch milliseconds.

const MS_PER_HOUR = 3_600_000;
const FREE_CANCEL_WINDOW_HOURS = 24;

export type Cents = number;

export interface OrderItem {
  readonly sku: string;
  readonly priceCents: Cents;
  readonly quantity: number;
  readonly shipped: boolean;
}

export interface RefundPolicy {
  /** Percentage of the refundable amount withheld when cancelling after the free window. */
  readonly lateFeePct: number;
}

export interface Order {
  readonly id: string;
  /** Epoch milliseconds at which the order was paid. */
  readonly paidAt: number;
  readonly items: readonly OrderItem[];
  readonly policy: RefundPolicy;
}

export interface RefundResult {
  readonly amountCents: Cents;
  readonly fee: Cents;
}

export function refund(order: Order, cancelledAt: number): RefundResult {
  const hours = (cancelledAt - order.paidAt) / MS_PER_HOUR;
  const items = order.items.filter((i) => !i.shipped);
  const amount = items.reduce<Cents>((sum, i) => sum + i.priceCents * i.quantity, 0);
  if (hours <= FREE_CANCEL_WINDOW_HOURS) return { amountCents: amount, fee: 0 };
  const fee = Math.round((amount * order.policy.lateFeePct) / 100);
  return { amountCents: amount - fee, fee };
}

export function totalRefunded(refunds: readonly RefundResult[]): Cents {
  return refunds.reduce<Cents>((sum, r) => sum + r.amountCents, 0);
}
