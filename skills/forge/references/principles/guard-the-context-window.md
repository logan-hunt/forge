# Guard the Context Window

When large reads or parallel investigations fill the context window, delegate the bulk reading when the active mode permits it. Keep the findings and source locations in the main thread.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
