export async function operation({ orderId, sku, quantity }, stock) {
  if (typeof orderId !== 'string' || !orderId.trim() ||
      typeof sku !== 'string' || !sku.trim() || !Number.isSafeInteger(quantity) || quantity <= 0) {
    throw new TypeError('Expected orderId, sku and a positive integer quantity')
  }
  return stock({ orderId: orderId.trim(), sku: sku.trim().toUpperCase(), quantity })
}
