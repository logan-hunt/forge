---
name: teach
description: Teach the user a new skill or concept over several sessions, with the current directory as a stateful teaching workspace. Use for /teach. To explain how code works, use how.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

# Teach

The user asked you to teach them something. This request has state: the user intends to learn the topic over several sessions. To explain how code works one time, use [how](../how/SKILL.md).

## Teaching workspace

Treat the current directory as a teaching workspace. Workspace paths such as `./lessons/` resolve from the directory where the user ran `/teach`. Only the format links resolve from this skill's folder. If the current directory is a code repository, ask the user where the workspace goes before you write.

These files hold the state of the user's learning:

- `MISSION.md`: the reason the user is interested in the topic. Ground all teaching in it. Use [mission-format.md](references/mission-format.md).
- `./reference/*.html`: reference materials. They are the compressed learnings from the lessons: cheat sheets, reference algorithms, syntax, glossaries. Design them for quick reference and for print.
- `RESOURCES.md`: the resources that ground your teaching. Use [resources-format.md](references/resources-format.md).
- `./learning-records/*.md`: records of what the user learned. They are the teaching equivalent of ADRs: non-obvious lessons and key insights that steer later sessions. Use them to calculate the zone of proximal development. Name them `0001-<dash-case-name>.md`, with a number that increments. Use [learning-record-format.md](references/learning-record-format.md).
- `./lessons/*.html`: the lessons. A **lesson** is one self-contained HTML file that teaches one tightly scoped thing tied to the mission. It is the primary unit of teaching.
- `./assets/*`: reusable components shared across lessons. See [Assets](#assets).
- `GLOSSARY.md`: the canonical terms for the topic. Use [glossary-format.md](references/glossary-format.md).
- `NOTES.md`: a scratchpad for the user's preferences and your working notes.

## Philosophy

To learn at a deep level, the user needs three things:

- **Knowledge**, from high-quality, high-trust resources
- **Skills**, acquired through relevant interactive lessons that you design from the knowledge
- **Wisdom**, which comes from interaction with other learners and practitioners

Until `RESOURCES.md` is well populated, focus on high-quality resources that help the user acquire knowledge. Never trust your parametric knowledge.

Some topics need more skills than knowledge. Theoretical physics is more knowledge-based. Yoga is more skills-based.

### Fluency and storage strength

Separate two types of learning:

- **Fluency strength**: retrieval of knowledge in the moment
- **Storage strength**: retention of knowledge in the long term

Fluency can give the user a false sense of mastery. Storage strength is the real goal. Design lessons that build long-term retention through desirable difficulty:

- Retrieval practice: recall from memory
- Spacing: practice distributed over time
- Interleaving: different but related topics mixed in practice (for skills practice only)

## Lessons

A lesson is the main thing you produce. Each lesson is one self-contained HTML file in `./lessons/`, named `0001-<dash-case-name>.html` with a number that increments.

A lesson has clean, readable typography and layout, because the user returns to it for review. Think Tufte.

Keep the lesson short, so that the user can complete it quickly. Working memory is small. Give the user one tangible win to build on. Tie the lesson directly to the mission, and keep it in the user's zone of proximal development.

- Open the lesson file for the user with a CLI command if possible.
- Link each lesson to other lessons and reference documents with HTML anchors.
- Recommend one primary source in each lesson: the most trustworthy resource you found on the topic.
- Remind the user in each lesson to ask you follow-up questions. You are their teacher.

## Assets

Lessons are built from reusable **components** in `./assets/`: stylesheets, quiz widgets, simulators, diagram helpers, and anything else a second lesson can reuse.

Reuse is the default. Before you write a lesson, read `./assets/` and build from the components there. When a lesson needs something new and reusable, write it as a component in `./assets/` and link to it. Never inline code that a later lesson would duplicate.

A shared stylesheet is the first component of every workspace. Every lesson links it, so that the lessons look like one course.

## The mission

Tie every lesson to the mission: the reason the user wants to learn the topic.

If the mission is unclear, or `MISSION.md` is empty, your first job is to ask the user why they want to learn this. Without the mission, the lessons are too abstract, and you cannot judge what the user needs next.

Missions change as the user develops skills and knowledge. Confirm with the user before you change the mission. Then update `MISSION.md` and add a learning record for the change.

## Zone of proximal development

In each lesson, challenge the user "just enough".

The user can name the exact thing they want to learn. If they do not, find their zone of proximal development:

1. Read their learning records.
2. Decide what to teach from their mission.
3. Teach the most relevant thing that fits.

## Knowledge

Design each lesson around a skill the user will learn. Include only the knowledge that the skill requires. Teach the knowledge first. Then have the user practice the skill in an interactive feedback loop.

Take knowledge from trusted resources, and track them in `RESOURCES.md`. Cite an external resource for every claim in a lesson.

For knowledge acquisition, difficulty is the enemy. It uses working memory that the user needs for understanding.

## Skills

Knowledge is about acquisition. Skills are about durability and flexibility.

For skill acquisition, difficulty is the tool. Effortful retrieval builds storage strength. Teach skills through interactive lessons:

- Quizzes and light in-browser tasks
- Lessons that guide the user through a list of real-world steps

Base each one on a **feedback loop** that tells the user how they performed. Make the loop as tight as possible: immediate feedback, automatic where possible.

In a quiz, give every answer the same number of words, and the same number of characters if possible. Vary the position of the correct answer across questions. Give no clue through format or order.

## Wisdom

Wisdom comes from real-world interaction: the user tests their skills outside the learning environment.

When a question appears to need wisdom, attempt an answer, but direct the user to a **community**. A community is a place, online or offline, where the user can test their skills. Examples are a forum, a subreddit, a class and a local interest group.

Find high-reputation communities the user can join. If the user does not want to join a community, respect that.

## Reference documents

While you create lessons, also create reference documents. A user rarely returns to a lesson. They return to a reference document. Make it the compressed essence of the lesson, in a format for quick reference.

Some topics suit reference well:

- Syntax and code snippets for programming
- Algorithms and flowcharts for processes
- Exercises and routines for fitness
- Glossaries for any topic with its own terms

A glossary is an essential reference. After you create one, follow it in every lesson.

## `NOTES.md`

The user sometimes states how they want to be taught, or things to remember. Record those preferences in `NOTES.md` and read it when you design a lesson.
