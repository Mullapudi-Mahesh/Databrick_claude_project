#!/usr/bin/env bash
# Multi-Agent Development Pipeline
# Usage: bash pipeline.sh
# Requires: claude CLI, gh CLI (gh auth login), databricks CLI (optional)

set -euo pipefail

# ── Colours ──────────────────────────────────────────────────────────────────
BLUE='\033[0;34m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

banner()  { echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; echo -e "${BLUE}  $1${NC}"; echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"; }
step()    { echo -e "\n${GREEN}▶ [Agent $1]${NC} $2\n"; }
success() { echo -e "${GREEN}✓ $1${NC}"; }
warn()    { echo -e "${YELLOW}⚠ $1${NC}"; }
fail()    { echo -e "${RED}✗ $1${NC}"; exit 1; }

# ── Preflight checks ─────────────────────────────────────────────────────────
command -v claude &>/dev/null || fail "claude CLI not found. Install Claude Code first."
command -v git    &>/dev/null || fail "git not found."
command -v gh     &>/dev/null || warn "gh CLI not found — GitHub agent will fail. Run: gh auth login"

mkdir -p .pipeline

# ── Step 0: Get project description ──────────────────────────────────────────
banner "MULTI-AGENT DEVELOPMENT PIPELINE"
echo -e "  Jira PM Agent  →  Databricks Implementation Agent  →  GitHub Release Agent\n"

PROJECT_DESC=""

if [ -f ".pipeline/project_description.txt" ] && [ -s ".pipeline/project_description.txt" ]; then
    echo -e "${YELLOW}Saved project description found:${NC}"
    echo "────────────────────────────────────────"
    cat .pipeline/project_description.txt
    echo ""
    echo "────────────────────────────────────────"
    read -rp "Use this description? (y/n): " USE_SAVED
    if [[ "$USE_SAVED" =~ ^[Yy]$ ]]; then
        PROJECT_DESC=$(cat .pipeline/project_description.txt)
    fi
fi

if [ -z "$PROJECT_DESC" ]; then
    echo -e "${YELLOW}Describe your project in detail.${NC}"
    echo "Include: what to build, data sources, transformations, outputs, requirements."
    echo "(Press Ctrl+D when done)"
    echo "────────────────────────────────────────"
    PROJECT_DESC=$(cat)
    echo "$PROJECT_DESC" > .pipeline/project_description.txt
fi

[ -z "$PROJECT_DESC" ] && fail "No project description provided."
success "Project description saved."

# ── Agent 1: Jira PM Agent ───────────────────────────────────────────────────
step "1" "Jira PM Agent — Creating tickets in Claude_project (CP)"

JIRA_PROMPT=$(cat <<EOF
Read the instruction file at .claude/agents/jira_agent.md and follow every instruction in it exactly.

Project description to analyse and create Jira tickets for:
---
$PROJECT_DESC
---

After creating all tickets, write the ticket keys (comma-separated) to .pipeline/ticket_keys.txt
EOF
)

claude -p "$JIRA_PROMPT"

TICKET_KEYS=$(cat .pipeline/ticket_keys.txt 2>/dev/null || echo "")
[ -z "$TICKET_KEYS" ] && fail "No ticket keys written to .pipeline/ticket_keys.txt. Check Agent 1 output."

success "Tickets created: $TICKET_KEYS"
echo -e "${YELLOW}View board: https://mahesh172003.atlassian.net/jira/software/projects/CP/boards${NC}"

echo ""
read -rp "Press Enter to continue to implementation... "

# ── Agent 2: Databricks Implementation Agent ─────────────────────────────────
step "2" "Databricks Implementation Agent — Implementing tasks"

DEV_PROMPT=$(cat <<EOF
Read the instruction file at .claude/agents/databricks_agent.md and follow every instruction in it exactly.

Jira tickets to implement (read each one from Jira before coding): $TICKET_KEYS

After writing all implementation files, save the file paths to .pipeline/implemented_files.txt
EOF
)

claude -p "$DEV_PROMPT"

IMPL_FILES=$(cat .pipeline/implemented_files.txt 2>/dev/null | tr '\n' ',' | sed 's/,$//' || echo "")

if [ -z "$IMPL_FILES" ]; then
    # Fallback: pick up any unstaged changes
    IMPL_FILES=$(git diff --name-only 2>/dev/null | tr '\n' ',' | sed 's/,$//' || echo "")
    warn "No .pipeline/implemented_files.txt found — using git diff: $IMPL_FILES"
fi

success "Implementation complete. Files: $IMPL_FILES"

echo ""
read -rp "Press Enter to create GitHub branch and PR... "

# ── Agent 3: GitHub Release Agent ────────────────────────────────────────────
step "3" "GitHub Release Agent — Branch → Commit → Push → PR"

GH_PROMPT=$(cat <<EOF
Read the instruction file at .claude/agents/github_agent.md and follow every instruction in it exactly.

Jira tickets: $TICKET_KEYS
Implemented files (also in .pipeline/implemented_files.txt): $IMPL_FILES

After creating the pull request, write the PR URL to .pipeline/pr_url.txt
EOF
)

claude -p "$GH_PROMPT"

PR_URL=$(cat .pipeline/pr_url.txt 2>/dev/null || echo "(check GitHub for PR)")

# ── Done ─────────────────────────────────────────────────────────────────────
banner "PIPELINE COMPLETE"
echo -e "  ${GREEN}Jira tickets:${NC}  $TICKET_KEYS"
echo -e "  ${GREEN}Files written:${NC} $IMPL_FILES"
echo -e "  ${GREEN}Pull Request:${NC}  $PR_URL"
echo ""
echo -e "${YELLOW}Please open the PR, review the changes, and validate before merging.${NC}"
echo ""
