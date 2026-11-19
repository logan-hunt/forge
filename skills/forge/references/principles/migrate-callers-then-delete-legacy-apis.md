# Migrate Callers Then Delete Legacy APIs

When all consumers can move together, migrate every caller to the new API and delete the old API in the same change. Preserve compatibility for external callers and persisted data.

- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative
