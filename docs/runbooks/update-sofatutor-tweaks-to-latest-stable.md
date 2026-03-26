# Runbook Moved

This workflow now lives as a Copilot skill and agent so it can be executed directly from chat instead of maintained as a long static runbook.

## Use The Skill

- Slash command: `/update-sofatutor-tweaks`
- Source: `.github/skills/update-sofatutor-tweaks/SKILL.md`

The skill contains the end-to-end procedure, conflict heuristics, verification steps, a release notes template, and a quick reference shell script.

## Use The Agent

- Agent: `sofatutor-stable-update`
- Source: `.github/agents/sofatutor-stable-update.agent.md`

Use the agent when you want Copilot to drive the workflow interactively, including repo validation, branch creation, merge handling, test execution, tagging, and release preparation.

## Skill Resources

- `.github/skills/update-sofatutor-tweaks/release-notes-template.md`
- `.github/skills/update-sofatutor-tweaks/quick-reference.sh`

## Notes

- The skill is now the source of truth for this procedure.
- The agent points back to the skill so the workflow stays defined in one place.
