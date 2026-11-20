# Deep Modules

Design deep modules: much behavior behind a small interface, placed at a clean seam, testable through that interface. Callers get leverage. Maintainers get locality.

## Vocabulary

Use these terms exactly. Do not substitute "component", "service", "API" or "boundary".

- **Module**: anything with an interface and an implementation. The term applies at every scale: a function, a class, a package, or a slice that spans tiers. _Avoid_: unit, component, service.
- **Interface**: everything a caller must know to use the module correctly. This includes the type signature, invariants, ordering constraints, error modes, required configuration and performance characteristics. _Avoid_: API, signature.
- **Implementation**: the code inside a module.
- **Depth**: leverage at the interface. It is the amount of behavior a caller or a test can exercise for each unit of interface they must learn. A module is deep when much behavior sits behind a small interface. A module is shallow when the interface is nearly as complex as the implementation.
- **Seam** (Michael Feathers): a place where you can alter behavior without an edit in that place. It is the location where a module's interface lives. _Avoid_: boundary.
- **Adapter**: a concrete thing that satisfies an interface at a seam. The term names the role, not the contents.
- **Leverage**: what callers get from depth. One implementation pays back across many call sites and tests.
- **Locality**: what maintainers get from depth. Change, bugs, knowledge and verification concentrate in one place.

For the symptoms of a shallow or leaking design, read the [design red flags](../../../architect/references/design-red-flags.md).

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can contain small, swappable parts. Those parts are not part of the interface. A module can have internal seams, used by its own tests, and the external seam at its interface.
- **The deletion test.** Imagine that you delete the module. If the complexity disappears, the module only passed calls through. If the complexity reappears across many callers, the module earned its place.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test past the interface, the module probably has the wrong shape.
- **One adapter means a hypothetical seam. Two adapters mean a real one.** Do not add a seam unless something varies across it. This is the [Ponytail](../../../ponytail/SKILL.md) rule for seams: no abstraction that nobody asked for.
- **A deepening deletes.** A reshape that only adds a layer is not a deepening. It must delete code, branches or invalid states.

When you design an interface, ask three questions. Can I reduce the number of methods? Can I simplify the parameters? Can I hide more complexity inside?

## Design for testability

1. Accept dependencies. Do not create them inside the module.
2. Return results. Do not produce side effects where a return value can carry the result.
3. Keep the interface small. Fewer methods need fewer tests. Fewer parameters need less test setup.

## Deepen a cluster of shallow modules

Classify the dependencies of the cluster. The category decides how you test the deepened module across its seam.

1. **In-process**: pure computation and in-memory state, no I/O. Merge the modules and test through the new interface. No adapter is necessary.
2. **Local-substitutable**: a dependency with a local test stand-in, such as an in-memory database or filesystem. Test the deepened module with the stand-in. The seam is internal.
3. **Remote but owned**: your own services across a network. Define a port at the seam. The deep module owns the logic, and the transport is an injected adapter. Tests use an in-memory adapter. Production uses the network adapter.
4. **True external**: a third-party service that you do not control. The deepened module takes the dependency as an injected port. Tests supply a mock adapter.

Replace tests, do not layer them. Write new tests at the deepened module's interface. Delete the old unit tests on the shallow modules when the new tests cover their behavior. A test that must change when the implementation changes tests past the interface.

## Rejected framings

- **Depth as the ratio of implementation lines to interface lines** (Ousterhout). This rewards a padded implementation. Use depth as leverage.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods.** This is too narrow. The interface includes every fact a caller must know.
- **"Boundary".** Domain-driven design already uses it for the bounded context. Say seam or interface.

To compare alternative interfaces for one module, use [architect](../../../architect/SKILL.md) or [arena](../../../arena/SKILL.md). Give each runner a different constraint: the smallest interface, the most flexible interface, the simplest common case, and ports and adapters.

This entry adapts the `codebase-design` skill from mattpocock/skills.
