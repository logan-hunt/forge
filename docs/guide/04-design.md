# Design

Architect grounds the subsystem, sketches contracts and compares structural alternatives. Arena runs competing candidates and synthesizes the strongest coherent design. Interrogate tries to break the design or implementation with executable evidence. Use their full skills when invoked.

Max defaults to this stronger design exploration for cross-boundary work. Standard reaches for it when ownership, concurrency, persistence or an unfamiliar contract makes the decision consequential. Existing clear patterns can be followed without manufacturing alternatives.

Model the domain before scattering flags and branches. Preserve external users, stored formats and independent deployments when changing APIs. A coordinated internal migration can remove old callers and APIs together; that permission does not extend to external contracts.
