# Automation & QA Developer — Take-Home Assessment

**Candidate:** Subrata Ghosh  
**Target App Tested:** RealWorld Conduit (`https://conduit.bondaracademy.com/`)  

---

## Overview
This repository contains my submission for the Automation & QA Developer take-home assessment:
1. **Task 1 — Web App QA & Debug Report**: Full QA audit and root-cause analysis on the RealWorld Conduit app (`Task1_QA_Report_Subrata_Ghosh.pdf`).
2. **Task 2 — n8n API Integration Workflow**: Daily morning brief workflow watching trending automation repos, enriching with commit details, conditional thresholding, and error handling (`Task2_Workflow_Subrata_Ghosh.json`).
3. **Bonus Task — Conduit Uptime Monitor**: 5-minute health check monitor with response-time tracking and retry logic (`Bonus_UptimeMonitor_Subrata_Ghosh.json`).

---

## Repository Structure

```text
├── Task1_QA_Report_Subrata_Ghosh.pdf       # QA Bug Report and Root-Cause Analysis (PDF)
├── Task2_Workflow_Subrata_Ghosh.json       # Task 2 n8n Workflow export
├── Bonus_UptimeMonitor_Subrata_Ghosh.json  # Bonus Task n8n Uptime Monitor export
├── README.md                               # Project documentation & setup notes
└── screenshots/                            # Evidence captures & workflow diagrams
    ├── bug_disappearing_navbar.png         # Issue #1: Nav links vanish on internal route transition
    ├── bug_stale_validation.png            # Issue #3: Stale error banner on form edit
    ├── bug_blank_settings.png              # Issue #4: Settings form fields load blank
    ├── article_view_with_delete_action.png # Issue #2: Instant deletion without confirmation
    ├── task2_workflow_canvas.png           # Task 2 n8n workflow canvas
    ├── task2_execution_output.png          # Task 2 successful execution output data
    └── bonus_uptime_monitor_canvas.png     # Bonus Task uptime monitor canvas
```

---

## Task 1: Web App QA & Debug Report
I ran exploratory and edge-case testing against the live RealWorld Conduit web application across all core user flows:
- Sign-up & Login
- New Article creation (markdown rendering, tag input)
- Article view & editing
- Article deletion
- User Profile & Settings updates
- Logout

I documented 6 key issues in the report according to the assessment template:
1. **Disappearing Navigation Header & Desynchronized Auth State (High)**: During internal client-side routing (e.g. going to `/editor` or user profile), the navbar loses the authenticated navigation links (`Home`, `New Article`, `Settings`, profile username) and only shows the brand text until a hard browser refresh.
2. **Immediate Irreversible Article Deletion (High)**: Clicking "Delete Article" deletes the article instantly via `DELETE /api/articles/:slug` with no confirmation dialog or undo option.
3. **Stale Validation Error Banner (Medium)**: When submitting an empty article form, the error banner ("title can't be blank") remains stuck on screen even after the user starts typing a valid title.
4. **Settings Form Pre-Population Failure (Medium)**: Navigating to `/settings` opens a form with blank Username and Email fields rather than pre-populating with existing user data.
5. **Plain-Text JWT in `localStorage` (High / Security)**: Auth token is stored directly in browser `localStorage` where any XSS vulnerability can access it, instead of using secure `httpOnly` cookies.
6. **Missing Form Labels & Autocomplete Attributes (Medium / Accessibility)**: Form inputs lack `<label>` tags, unique IDs, and autocomplete hints, triggering browser console warnings and blocking assistive screen readers.

The PDF report [`Task1_QA_Report_Subrata_Ghosh.pdf`](./Task1_QA_Report_Subrata_Ghosh.pdf) includes the bug table, full steps to reproduce, screenshots, and an in-depth root-cause analysis on the disappearing navbar issue with suggested Angular fixes (`shareReplay(1)`, async pipe, route resolvers).

---

## Task 2: n8n API Integration Workflow (Morning Brief)
File: [`Task2_Workflow_Subrata_Ghosh.json`](./Task2_Workflow_Subrata_Ghosh.json)

- **Triggers**: Schedule trigger running hourly, plus a Webhook trigger (`POST /trigger-morning-brief`) for on-demand runs.
- **First API Call**: GitHub REST Search API (`GET https://api.github.com/search/repositories?q=topic:automation+stars:>1000&sort=stars&order=desc&per_page=10`) to find trending automation projects.
- **Transformation (Code node)**:
  - Sorts the repos by star count and keeps the top 5.
  - Normalizes numbers into readable format (e.g. `209.8k` stars).
  - Isolates the #1 ranked repo for secondary enrichment.
- **Second API Call (Enrichment)**: Calls GitHub Commits API (`GET https://api.github.com/repos/:owner/:repo/commits?per_page=1`) on the #1 repo to pull latest commit SHA, commit message, author, and timestamp.
- **Conditional Threshold (IF node)**: Checks if the top repo has `>= 50,000` stars:
  - **True**: Formats a "Mega-Tier" alert spotlight highlighting breakthrough projects.
  - **False**: Formats a standard morning brief digest.
- **Output**: Sends the formatted markdown message to a webhook (compatible with Discord, Slack, or generic webhook receivers).
- **Error Handling**:
  - `continueOnFail: true` on HTTP Request nodes so unexpected status codes do not crash the workflow.
  - IF node checks if items were returned; if the API call fails or returns empty data, it routes to an `API 1 Error Fallback Logger` node that formats an alert and notifies the team.
  - Added a global `Error Trigger` node to catch any unhandled workflow-level failures.
  - Uses environment variables (`$env.NOTIFICATION_WEBHOOK_URL`) instead of hardcoding webhook URLs.

---

## Bonus Task: Conduit Web App Uptime Monitor
File: [`Bonus_UptimeMonitor_Subrata_Ghosh.json`](./Bonus_UptimeMonitor_Subrata_Ghosh.json)

- **Schedule**: Pings `https://conduit-api.bondaracademy.com/api/articles?limit=1` every 5 minutes.
- **Latency Tracking**: Calculates duration in milliseconds between request start and response. Flags performance degradation if response time exceeds `1500ms`.
- **Retry Logic (Anti-Flap)**:
  - If the initial ping fails or returns non-200, the workflow does not immediately sound a critical alert.
  - It pauses for 3 seconds using a Wait node and fires a second verification ping.
  - If the second attempt also fails, it posts a **Critical Outage Alert** with HTTP status codes and timestamps.
  - If the second attempt succeeds, it logs a **Transient Flap Warning**, preventing false-alarm pager fatigue.
- **Daily Summary**: Normal pings are routed to a metric logger node to record uptime stats.

---

## How to Import into n8n
1. Open your n8n workspace.
2. In the top-right menu, select **Import from File**.
3. Choose `Task2_Workflow_Subrata_Ghosh.json` or `Bonus_UptimeMonitor_Subrata_Ghosh.json`.
4. Click **Test workflow** to run with live data.
