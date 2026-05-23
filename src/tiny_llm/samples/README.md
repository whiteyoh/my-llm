# Bundled Sample Training Text Guide

This folder mirrors sample training files packaged with `tiny-llm` installs.

The training intent for each sample matches the repository guide at
`data/samples/README.md`.

## `space_adventure.txt`

Intro:
Neutral space narrative.

Insight:
Recommended baseline corpus for before/after retrain lessons.

## `pirate_dialogue.txt`

Intro:
Pirate dialogue and stylized speech.

Insight:
Recommended contrast corpus for visible style shift after retraining.

## `robot_helper.txt`

Intro:
Task-assistant style instructional text.

Insight:
Useful for comparing helpful/task-oriented tone against story datasets.

## `nature_notes.txt`

Intro:
Nature observation writing.

Insight:
Useful for descriptive tone comparisons and calmer output patterns.

## `short_poems.txt`

Intro:
Compact poetic lines.

Insight:
Useful for rhythm and repetition pattern demonstrations.

## `sci_fi_micro_story.txt`

Intro:
Short science-fiction micro stories.

Insight:
Useful for concise narrative behavior experiments.

## `qa_space_facts.jsonl`

Intro:
Structured QA records.

Insight:
Use with `kairo-build-qa-corpus`; do not train directly as plain text.
