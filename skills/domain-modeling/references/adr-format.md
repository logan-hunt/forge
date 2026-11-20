# ADR format

ADRs are in `docs/adr/` and use sequential numbers: `0001-slug.md`, `0002-slug.md`, and so on.

Create the `docs/adr/` directory only when the first ADR is necessary.

## Template

```md
# {Short title of the decision}

{1-3 sentences: the context, what we decided, and why.}
```

An ADR can be a single paragraph. Its value is the record that a decision was made, and why. Sections add no value by themselves.

## Optional sections

Include these only when they help a future reader. Most ADRs do not need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`). Use it when the team revisits decisions.
- **Considered Options**. Use it only when the rejected alternatives are worth a record.
- **Consequences**. Use it only when the decision has downstream effects that are not obvious.

## Numbering

Scan `docs/adr/` for the highest existing number and add one.

## When to offer an ADR

All three conditions must be true:

1. **Hard to reverse.** A later change of mind has a meaningful cost.
2. **Surprising without context.** A future reader will look at the code and ask why the team did it this way.
3. **The result of a real trade-off.** Real alternatives existed, and you chose one for specific reasons.

A decision that is easy to reverse needs no record, because you can reverse it. A decision that surprises nobody needs no explanation. A decision with no real alternative has nothing to record.

### What qualifies

- **Architectural shape.** "We use a monorepo." "The write model is event-sourced, and the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate through domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Record only the choices that would take a quarter to replace, not every library.
- **Boundary and scope decisions.** "The Customer context owns customer data. Other contexts reference it by ID only." An explicit "no" is as valuable as a "yes".
- **Deliberate deviations from the obvious path.** "We use manual SQL and no ORM because X." Record anything where a reasonable reader would assume the opposite. The record stops the next engineer from "fixing" a deliberate choice.
- **Constraints that the code does not show.** "We cannot use AWS because of compliance requirements." "Response times must stay under 200ms because of the partner API contract."
- **Rejected alternatives, when the rejection is not obvious.** If you considered GraphQL and chose REST for subtle reasons, record it. Without the record, someone will suggest GraphQL again in six months.
