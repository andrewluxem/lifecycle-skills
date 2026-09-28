---
name: program-template
description: >-
  Authoring scaffold for a new Lifecycle-Programs blueprint, not a program
  itself. Use when adding a new lifecycle program skill to this plugin (for
  example browse-abandon, sunset, or birthday), so the new skill starts with the
  required section order, evidence labels, touch framework, holdout recipe, and
  kill condition already in place instead of improvised.
license: MIT
---

# Program Template

This is the skeleton every program in this plugin is built from. Copy the whole
folder to `skills/<your-program-slug>/`, rename `name:` in the frontmatter to
match the folder, and replace every guidance block below with real content. Read
`PROGRAM-CONVENTIONS.md` first. If you can't fill a section honestly, the program
isn't ready, and I'd rather you say so than ship a section of filler.

> Delete every `> Guidance:` block before you merge. A program with guidance
> text still in it is a draft.

## When to use this skill

> Guidance: List 4–6 trigger phrases a real operator would say ("our welcome
> flow isn't converting," "build me a cart abandon program"). Then name the
> leak zone(s) this program fixes: activation / early-life / mid-life /
> resurrection. Then say what it is NOT for and which sibling skill owns that.
> Always include the routing rule: if the leak is unknown, send the user to
> `retention-diagnosis` first and refuse to design in the dark.

## What I need before I start

> Guidance: Split into **Required** and **Optional**. Required inputs are the
> ones without which the program is a guess (the trigger event you can actually
> detect, consent status, AOV or margin if an incentive is on the table). Then
> say exactly what you can still produce with partial inputs, and that every
> missing number becomes `[Assumption]`.

## The thesis

> Guidance: One or two paragraphs. What do most teams get wrong about this
> program, and what does this one do instead? Take a position. "I think" and "I
> worry" are allowed and encouraged. End with the sacrifice: what this program
> deliberately does NOT do.

## Program blueprint

### Objective and audience

> Guidance: The one business outcome, the entry audience, and the leak zone it
> treats.

### Message architecture

> Guidance: A table with one row per touch and these columns: #, Purpose,
> Timing + rationale, Channel, Job, Proof element, CTA, Anti-goal. Frameworks,
> never finished copy.

| # | Purpose | Timing + rationale | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |

### Splits and personalization

> Guidance: Every split must earn its place with a reason. Name the default
> path, then the branches. Personalization that doesn't change a decision is
> decoration; cut it.

### Exits and suppression

> Guidance: Every exit condition, where the person goes next, and which other
> programs are suppressed while they're in this one. The most common bug in any
> program lives here.

### Content blocks

> Guidance: Reusable modules (dynamic product block, review snippet, guarantee
> strip) and the data each one needs.

## Platform build mapping

> Guidance: Describe the build in primitives only: trigger, filter, split, wait,
> exit. One short list. Point to `references/platform-build.md` for Braze,
> Klaviyo, Iterable, and SFMC specifics.

## QA

> Guidance: The five checks that catch the most expensive errors for this
> program, in the order you'd run them. Full list in
> `references/qa-checklist.md`. This skill never sends; it tells a human what to
> verify before they do.

## Measurement

> Guidance: Four things, all in the SKILL.md:
> - **Primary KPI** and its window.
> - **Guardrails** (unsubscribe, complaint, margin, cannibalization).
> - **Holdout recipe**: size, randomization unit, duration, what the control
>   receives.
> - **Kill condition**: "If treated doesn't beat holdout on X by Y within Z
>   weeks, we stop and do W." Specific, dated, and stated here, not in a
>   reference file.

## Field notes

> Guidance: Optional. Only the author's real operator experience, labeled
> `[Fact — author's record]`. Never client or employer specifics. Delete the
> section if you have nothing true to say.

## Worked example

> Guidance: Three to six lines summarizing the fictional brief in
> `examples/example-brief.md` and the one decision it illustrates best. Invented
> brand, labeled numbers.
