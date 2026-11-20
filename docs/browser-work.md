# Browser work

Follow the active host's required browser route. Otherwise use an available browser or the project's existing automation according to the task. Reuse project-owned sign-in and verification instructions rather than assuming a particular application or authentication service.

Preserve existing profiles and session ownership. Never terminate another task's session to clear a lock. Use authenticated sessions when available. Request sign-in through the host's supported mechanism when needed. Never ask for passwords in conversation or print credentials, cookies or session tokens.

Keep actions within task authorization. Restore test preferences or data when appropriate, and close task-created tabs and processes unless the user needs them. Inspect failures, retry when useful and try another available route when permitted. Report concrete blockers rather than claiming verification.

Use the host's visualization tools for inline reports. Browser automation and report rendering are separate capabilities. Do not start a server just to display a standalone report.
