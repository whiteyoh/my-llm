---
name: packaging-install-readiness
description: Use when commands, package data, entry points, or install flows are changed.
---

# packaging-install-readiness

<purpose>
Keep Kairo runnable from both repository checkout and installed package contexts.
</purpose>

<use-when>
- New CLI commands are added
- Sample files are added or relocated
- pyproject scripts or package-data settings change
</use-when>

<responsibilities>
- Verify console script declarations and import targets
- Ensure required sample assets are packaged and discoverable
- Test portable command flows that do not assume repository-relative paths
- Add or update packaging regression tests
</responsibilities>

<constraints>
- Do not introduce network-dependent install checks in tests
- Avoid breaking backward-compatible script wrappers without explicit approval
- Keep command UX friendly and actionable
</constraints>

<inputs>
- pyproject configuration, CLI modules, path helpers, packaging tests
</inputs>

<outputs>
- Install-safe packaging updates with reproducible validation steps
</outputs>

<collaboration>
- delegate-to: qa-evaluation-engineer when packaging changes affect QA command behavior
- delegate-to: school-demo-release-gatekeeper for final readiness verification
- escalate-to: orchestrator when packaging constraints conflict with classroom workflow needs
</collaboration>
