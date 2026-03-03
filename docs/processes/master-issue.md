# Master Issue

_(stub)_

## Overview
How to coordinate large initiatives using Master Issues in the Cimeika ecosystem.

## What Is a Master Issue?
A Master Issue is a tracking issue that groups related sub-tasks for a large feature, epic, or initiative.

## Structure
```markdown
## Goal
<High-level description of the initiative>

## Sub-tasks
- [ ] #<issue-number> — <description>
- [ ] #<issue-number> — <description>

## Definition of Done
<Criteria that must be met to close this Master Issue>
```

## Rules
- Each sub-task must be a separate issue with its own PR.
- The Master Issue is closed only when all sub-tasks are completed and verified.
- Reference the Master Issue in every related PR description.
