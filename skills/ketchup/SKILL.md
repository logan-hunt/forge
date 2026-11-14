---
name: ketchup
description: Summarize what changed in this chat and the decisions still waiting on the user. Use for /ketchup or a catch-up request.
disable-model-invocation: false
---

# Ketchup

Catch the user up from their last human message before this request. Notifications and delegate results do not reset that point.

Keep the turn read-only. Use the conversation, returned work and relevant current PR/check state. Do not change code, launch jobs or post messages to make the summary more complete.

Explain the outcomes in plain words. Distinguish completed, running, failed and unverified work. Correct any stale status you discover. Include links and technical details when they help the user decide or act.

List every decision still waiting on the user, including earlier unanswered ones. Give the relevant item, your recommendation, supporting evidence, tradeoffs and material risk. Say when a needed fact is unknown. Do not invent decisions or present work you can do yourself as a user action.

Keep the recap proportionate to what changed. Show existing screenshots or a small diagram when they make a visible change or dependency easier to understand. A short text answer is enough when no picture helps.

If nothing changed and no decision is pending, say so and stop. Otherwise name any remaining work you can continue. Follow the adopter's writing style.
