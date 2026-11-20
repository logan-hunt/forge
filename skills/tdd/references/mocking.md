# When to mock

The examples use TypeScript. The rules apply in every language.

Mock at **system boundaries** only:

- External APIs, such as payment and email
- Databases, sometimes. Prefer a test database.
- Time and randomness
- The file system, sometimes

Do not mock:

- Your own classes and modules
- Internal collaborators
- Anything you control

## Design for mockability

At system boundaries, design interfaces that are easy to mock:

**1. Use dependency injection**

Pass external dependencies in. Do not create them inside the function:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. Prefer SDK-style interfaces over generic fetchers**

Create one specific function for each external operation. Do not use one generic function with conditional logic:

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach gives you:

- Mocks that each return one specific shape
- No conditional logic in the test setup
- A clear view of which endpoints a test uses
- Type safety for each endpoint
