# GLOSSARY.md format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** When several words exist for the same concept, choose the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences at most. Define what the term is, not what it does.
- **Include only terms specific to this project's context.** General programming concepts, such as timeouts, error types and utility patterns, do not belong, even if the project uses them often. Before you add a term, ask whether the concept is unique to this context.
- **Group terms under subheadings** when natural clusters appear. If all terms belong to one area, a flat list is fine.

## One context or several

**One context (most repositories).** One `GLOSSARY.md` at the repository root.

**Several contexts.** A `GLOSSARY-MAP.md` at the repository root lists the contexts, where each one is, and how they relate:

```md
# Glossary Map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/GLOSSARY.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

Find the structure that applies:

- If `GLOSSARY-MAP.md` exists, read it to find the contexts.
- If only a root `GLOSSARY.md` exists, the repository has one context.
- If neither exists, create a root `GLOSSARY.md` when the first term is resolved.

When the repository has several contexts, infer which one the current topic belongs to. If that is unclear, ask.
