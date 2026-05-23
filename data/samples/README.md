# Sample Training Text Guide

This folder contains text files used to train Kairo in different styles.

Use this guide before training so learners understand what the model is about to
learn and why that matters for comparison.

## `space_adventure.txt`

Intro:
Story-style space narrative with calm descriptive language.

Insight:
Use this as a baseline dataset for neutral narrative output. It is ideal for the
"before retrain" run.

## `pirate_dialogue.txt`

Intro:
Dialogue-heavy pirate voice with expressive vocabulary and rhythm.

Insight:
Use this as a contrast dataset after baseline training to demonstrate obvious
style transfer.

## `robot_helper.txt`

Intro:
Instructional helper-style text focused on practical assistance.

Insight:
Useful for testing a task-oriented tone and comparing factual/helpful phrasing
against creative narrative corpora.

## `nature_notes.txt`

Intro:
Observation-style writing about natural scenes and patterns.

Insight:
Good for showing how descriptive, grounded language influences output stability
and tone.

## `short_poems.txt`

Intro:
Compact poetic lines with rhythm and imagery.

Insight:
Useful for demonstrating brief, stylized output patterns and repetition effects
common in tiny models.

## `sci_fi_micro_story.txt`

Intro:
Short science-fiction micro fiction with compressed narrative beats.

Insight:
Useful for comparing concise storytelling behavior with longer narrative files.

## `qa_space_facts.jsonl`

Intro:
Structured question-answer examples in JSONL format.

Insight:
This is for QA corpus building with `kairo-build-qa-corpus`, not direct training
as plain text.
