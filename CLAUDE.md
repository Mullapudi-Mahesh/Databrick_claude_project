# Databricks Claude Multi-Agent Pipeline

This project implements a 3-agent development pipeline:
**User describes project → Jira tickets → Databricks implementation → GitHub PR**

## How to Run

```bash
bash pipeline.sh
```

Or open this project in Claude Code and describe your project — Claude will orchestrate all three agents automatically.

## Agent Pipeline

| Agent | Instruction File | Role |
|-------|-----------------|------|
| Jira PM Agent | `.claude/agents/jira_agent.md` | Breaks project description into Jira tickets |
| Databricks Agent | `.claude/agents/databricks_agent.md` | Reads tickets, writes implementation code |
| GitHub Agent | `.claude/agents/github_agent.md` | Creates branch, commits, pushes, opens PR |

## Authentication (no keys needed)

| Service | How to authenticate |
|---------|-------------------|
| **Jira** | Atlassian MCP — already connected in Claude Code settings |
| **GitHub** | Run `gh auth login` once in your terminal |
| **Databricks** | Run `databricks configure` once (optional — code written locally if skipped) |

## Project Config

- Jira project: **Claude_project** (key: `CP`)
- Jira site: `mahesh172003.atlassian.net`
- Jira cloudId: `7ce5f23f-915c-4c60-a8c1-fc8fa6ef5ed6`

## Orchestration Instructions (read this when user describes a project)

When the user provides a project description, follow this pipeline in order:

1. **Spawn the Jira PM Agent** — pass the project description, get back created ticket keys
2. **Spawn the Databricks Implementation Agent** — pass the ticket keys, get back list of implemented files
3. **Spawn the GitHub Release Agent** — pass the ticket keys + file list, get back PR URL
4. **Show the user the PR URL** and ask them to review and validate before merging

Do not skip steps. Do not proceed to the next agent until the current one is complete.

## Pipeline State Files

Intermediate state is stored in `.pipeline/` (gitignored):
- `project_description.txt` — saved project description
- `ticket_keys.txt` — comma-separated Jira ticket keys (e.g. `CP-5,CP-6`)
- `implemented_files.txt` — one file path per line
- `pr_url.txt` — final GitHub PR URL
