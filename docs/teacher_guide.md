# Kairo Teacher Guide

## Lesson overview
Kairo is a tiny educational language-model lab for demonstrating next-token prediction.

## Safeguarding (lightweight, teacher-led)
Kairo includes lightweight guardrails only. It is not full moderation. Teachers should supervise prompts, datasets, and outputs at all times.

## Dataset checklist
- Use school-appropriate text only.
- Do not include personal data (emails, phone numbers, addresses).
- Avoid harmful or distressing themes.
- Avoid content you do not have permission to reuse.
- Start with `data/samples/` when possible.

## Prompting rules for pupils
- Use kind, respectful prompts.
- Avoid requests about harm, weapons, or illegal activity.
- Do not paste personal information.
- Ask a teacher before trying unusual prompts.

## Teacher review workflow
1. Teacher selects or approves dataset text.
2. Teacher runs training and checks warnings.
3. Pupils submit prompts; teacher monitors output.
4. If output is unsuitable, stop and discuss why.
5. Adjust dataset/prompting rules and retry.

## How to respond to unsuitable outputs
- Pause the activity.
- Remind students that Kairo predicts tokens and can be wrong/unsafe.
- Remove unsafe dataset text and retry with safer samples.
- Re-enable safe filtering if it was disabled.

## Suggested classroom rules
- "No personal data in prompts or datasets."
- "Use only teacher-approved text."
- "Tell a teacher immediately if output seems unsafe."
- "Kairo is a learning tool, not a trusted authority."
