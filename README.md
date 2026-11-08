# Automation & QA Developer — Take-Home Skills Assessment

**Author / Candidate:** Subrata Ghosh  
**Target Web Application:** RealWorld Conduit Web App (`https://conduit.bondaracademy.com/`) & API (`https://conduit-api.bondaracademy.com/api`)  
**Public GitHub Repository:** [https://github.com/Subrata0Ghosh/automation-qa-assessment](https://github.com/Subrata0Ghosh/automation-qa-assessment)  
**Assessment Date:** November 8, 2026  

---

## 📋 Table of Contents
1. [Overview & Project Structure](#overview--project-structure)
2. [Task 1 — Web App QA & Debug Report](#task-1--web-app-qa--debug-report)
3. [Task 2 — n8n API Integration Workflow](#task-2--n8n-api-integration-workflow)
4. [Bonus Task — Web App Uptime Monitor](#bonus-task--web-app-uptime-monitor)
5. [Loom Video Presentation Script](#loom-video-presentation-script)
6. [Import & Execution Guide for Reviewers](#import--execution-guide-for-reviewers)

---

## 1. Overview & Project Structure

This repository contains the complete deliverables for the **Automation & QA Developer Skills Assessment**, addressing:
- End-to-end exploratory and automated QA of a "vibe-coded" AI-assisted web application.
- Production-grade n8n integration workflow with scheduling, webhook triggers, multi-stage API consumption, data enrichment, dynamic thresholding, notification dispatching, and failure guards.
- Bonus Uptime Sentinel workflow combining QA health-checking with automated retry logic, latency measurement, and incident alerting.

```text
automation-qa/
├── Task1_QA_Report_Subrata_Ghosh.pdf      # Official Task 1 PDF deliverable (executive styling)
├── Task1_QA_Report_Subrata_Ghosh.md       # Markdown version of Bug Report & Root Cause Analysis
├── Task2_Workflow_Subrata_Ghosh.json      # Official Task 2 n8n Workflow JSON (Download ready)
├── Bonus_UptimeMonitor_Subrata_Ghosh.json # Official Bonus Task n8n Workflow JSON
├── README.md                              # Complete assessment documentation & API architecture
├── LOOM_WALKTHROUGH_SCRIPT.md             # Rehearsed Loom video presentation guide with cues
├── generate_report_html.py                # Automation script compiling report HTML
├── render_n8n_screenshots.py              # Visual engine rendering canvas & execution views
└── screenshots/                           # High-resolution photographic evidence & workflow captures
    ├── bug_disappearing_navbar.png        # Task 1: SPA state desynchronization
    ├── bug_stale_validation.png           # Task 1: Persistent stale error banner
    ├── bug_blank_settings.png             # Task 1: Form pre-population failure
    ├── article_view_with_delete_action.png# Task 1: Unprotected destructive deletion
    ├── task2_workflow_canvas.png          # Task 2: n8n workflow canvas
    ├── task2_execution_output.png         # Task 2: Successful execution & JSON inspector
    └── bonus_uptime_monitor_canvas.png    # Bonus: Uptime monitor canvas with retry loop
```

---

## 2. Task 1 — Web App QA & Debug Report

### Investigation Context
We tested the live RealWorld Conduit web application deployed at `https://conduit.bondaracademy.com/` (backed by `https://conduit-api.bondaracademy.com/api`). Our testing exercised the critical user paths: user registration, session authentication, content authoring (markdown and tags), article editing, article deletion, profile updates, and logout.

### Bug Report Summary (Section 5 Template)
A total of **6 critical issues** were identified:

| # | Title / Summary | Steps to Reproduce | Expected vs Actual | Severity | Suspected Cause |
|---|---|---|---|---|---|
| **1** | **Disappearing Navigation Header & Desynchronized Auth State** | 1. Log in or register.<br>2. Confirm logged-in header displays.<br>3. Navigate to `/editor`, edit an article, or visit `/profile/:user`.<br>4. Inspect the top header. | **Expected:** Navbar consistently retains user navigation links across all SPA routes.<br><br>**Actual:** Navigation links disappear completely; only raw "conduit" brand text displays. User is stranded without navigation controls until a browser refresh. | **High** | The `currentUser$` BehaviorSubject in `UserService` is not multicasted with replay (`shareReplay(1)`) or is unsubscribed on route activation, causing `*ngIf="currentUser"` to evaluate falsy. |
| **2** | **Immediate Irreversible Content Deletion Without Confirmation** | 1. Publish an article.<br>2. Open article view (`/article/:slug`).<br>3. Click the red "Delete Article" button. | **Expected:** A confirmation dialog/modal prompts: *"Are you sure you want to delete this article?"* before destructive action.<br><br>**Actual:** Article is permanently deleted via `DELETE /api/articles/:slug` on a single click with zero confirmation prompt and no undo grace period. | **High** | Click handler directly invokes `ArticlesService.destroy()` without any `window.confirm()` or modal interception. |
| **3** | **Stale Validation Error Banner Persisting on Input Correction** | 1. Navigate to `/editor`.<br>2. Click "Publish Article" with empty fields to trigger a 422 error ("title can't be blank").<br>3. Click into "Article Title" and type a valid title. | **Expected:** Validation error banner clears immediately when the user modifies or focuses the invalid input field.<br><br>**Actual:** "title can't be blank" remains visibly rendered above the form even while the user actively types a valid title, misinforming the user. | **Medium** | Component error state is bound only to HTTP rejection responses and does not subscribe to form control `valueChanges` to clear errors upon user input. |
| **4** | **Settings Form Profile Pre-Population Failure (Blank Form)** | 1. Log in with an established user account.<br>2. Navigate to Settings (`/settings`).<br>3. Inspect the "Username" and "Email" fields. | **Expected:** Settings form fields are pre-populated with the user's current username, email, bio, and image URL.<br><br>**Actual:** Username and Email fields are completely blank (`""`). Submitting an update to Bio sends empty fields to the API, risking data loss/overwrite. | **Medium** | Reactive form is initialized with blank default strings synchronously before the asynchronous user profile API response resolves, omitting `patchValue()`. |
| **5** | **Insecure Storage of Plain-Text JWT in `localStorage`** | 1. Authenticate via login or register.<br>2. Open browser DevTools Console.<br>3. Execute `window.localStorage.getItem('jwtToken')`. | **Expected:** Authentication session tokens should be stored in secure, `httpOnly`, `SameSite=Strict` cookies inaccessible to JavaScript.<br><br>**Actual:** Long-lived JWT token is stored in unencrypted `localStorage`, vulnerable to theft by any injected XSS script or compromised dependency. | **High** | Client-side architectural shortcut relying on browser `localStorage` instead of server-managed secure session cookies. |
| **6** | **Accessibility & DOM Non-Compliance: Missing Input Labels & Attributes** | 1. Open `/login` or `/register`.<br>2. Inspect form DOM inputs in Elements tab & Console. | **Expected:** Every input features accessible `<label>` tags, unique `id`/`name` attributes, and `autocomplete` hints.<br><br>**Actual:** Inputs lack labels, IDs, and autocomplete attributes, generating DOM console warnings and blocking assistive technologies. | **Medium** | Minimalist UI template styling omitting WAI-ARIA and semantic HTML standards during rapid prototyping. |

### Root-Cause Analysis (Issue #1: Disappearing Navigation Header)
- **What is Happening:** When navigating between internal routes in the SPA (e.g. from the feed to an article editor or user profile), the header links vanish, leaving only the brand text.
- **Why it Happens:** The `HeaderComponent` binds navigation items via `*ngIf="currentUser"` linked to `UserService.currentUser$`. Because the observable stream lacked replay buffering (`shareReplay(1)`), component re-renders during child route activation evaluate before the user session object is re-emitted, dropping the template DOM nodes.
- **How to Fix:**
  1. Pipe `currentUser$` through `shareReplay({ bufferSize: 1, refCount: false })`.
  2. Use Angular's declarative `async` pipe in the template (`*ngIf="currentUser$ | async as user; else guestNav"`).
  3. Attach an Angular route resolver (`UserResolver`) on protected routes.
  4. Implement automated Playwright regression tests asserting navbar persistence across route hops.

*Full details and visual evidence are documented in [Task1_QA_Report_Subrata_Ghosh.pdf](./Task1_QA_Report_Subrata_Ghosh.pdf).*

---

## 3. Task 2 — n8n API Integration Workflow

**Deliverable File:** [`Task2_Workflow_Subrata_Ghosh.json`](./Task2_Workflow_Subrata_Ghosh.json)  
**Canvas Screenshot:** [`screenshots/task2_workflow_canvas.png`](./screenshots/task2_workflow_canvas.png)  
**Execution Screenshot:** [`screenshots/task2_execution_output.png`](./screenshots/task2_execution_output.png)

```
[Schedule Trigger (1h)] ──┐
                          ├──► [Fetch Trending Repos (GitHub)] ──► [Check API Success (IF)]
[Webhook Trigger (POST)] ─┘                                            │
                                           ┌───────────────────────────┴───────────────────────────┐
                                      (True Branch)                                          (False Branch)
                                           │                                                       │
                           [Transform & Filter Top 5]                                   [API 1 Error Fallback]
                                           │                                                       │
                       [Enrich #1 Repo (Commit API)]                                    [Dispatch Error Alert]
                                           │
                              [Merge Enriched Data]
                                           │
                         [Conditional Star Threshold]
                         (Threshold: stars >= 50,000)
                                           │
                   ┌───────────────────────┴───────────────────────┐
              (True Branch)                                  (False Branch)
                   │                                               │
        [Format Mega-Tier Brief]                        [Format Standard Brief]
                   │                                               │
                   └───────────────────────┬───────────────────────┘
                                           ▼
                            [Send Notification Digest]
                          (Discord / Slack / Telegram)
```

### 1. APIs Used & Rationale
1. **Primary Ingestion API: GitHub REST API Search (`/search/repositories`)**  
   - **Endpoint:** `GET https://api.github.com/search/repositories?q=topic:automation+stars:>1000&sort=stars&order=desc&per_page=10`
   - **Why:** Directly matches the Automation & QA Developer domain by querying the ecosystem's highest-impact automation tools (e.g. `n8n`, `dify`, `orca`, `playwright`). Highly reliable, rich metadata, and adheres to standard pagination and caching headers.
2. **Enrichment API: GitHub Commits API (`/repos/:owner/:repo/commits`)**  
   - **Endpoint:** `GET https://api.github.com/repos/{{ $json.top_repo.full_name }}/commits?per_page=1`
   - **Why:** Enriches the #1 ranked project with real-time velocity metrics: latest commit SHA, commit author, commit timestamp, and release activity.

### 2. Transformation Logic (`Transform & Filter Top 5` & `Merge Data`)
- **Sanitization & Sorting:** Verifies response integrity, sorts items strictly by star count, and extracts the top 5 projects.
- **Data Normalization:** Formats numbers into human-readable notation (e.g., `209.8k` stars), handles null descriptions gracefully, and normalizes repository fields.
- **Enrichment Merging:** Merges the secondary commit payload with the primary dataset without losing array elements.
- **Dynamic Thresholding:** Routes through an IF node checking `{{ $json.top_repo.stars >= 50000 }}`. If met, it formats an eye-catching **Mega-Tier High Velocity Radar** spotlight; otherwise, it formats a **Standard Daily Brief**.

### 3. Error Handling Architecture (No Silent Crashes)
1. **Node-Level Error Containment:** HTTP Request nodes have `continueOnFail: true`, preventing unhandled 4xx/5xx responses from halting execution.
2. **Conditional Validation (`Check API Success`):** If GitHub API returns rate-limiting (403), network timeouts, or empty datasets, the flow routes to the `API 1 Error Fallback Logger`. This formats a structured incident notice and alerts the operations channel.
3. **Global Workflow Watchdog (`Global Error Trigger`):** An independent `n8n-nodes-base.errorTrigger` node captures any unforeseen edge cases across the runtime, formatting execution IDs and stack traces for engineering triage.
4. **Credential Security:** All secrets reference n8n's Credential Store or environment variables (`$env.NOTIFICATION_WEBHOOK_URL`), ensuring zero hard-coded secrets.

---

## 4. Bonus Task — Web App Uptime Monitor

**Deliverable File:** [`Bonus_UptimeMonitor_Subrata_Ghosh.json`](./Bonus_UptimeMonitor_Subrata_Ghosh.json)  
**Canvas Screenshot:** [`screenshots/bonus_uptime_monitor_canvas.png`](./screenshots/bonus_uptime_monitor_canvas.png)

### Architecture Highlights
- **Cadence:** Schedule Trigger running every 5 minutes (`*/5 * * * *`).
- **Target Inspected:** RealWorld Conduit API (`https://conduit-api.bondaracademy.com/api/articles?limit=1`).
- **Response-Time Tracking:** Records `start_time` and calculates elapsed duration in milliseconds. Flags performance degradation if latency exceeds `1500ms`.
- **Anti-Flap Retry Logic (Bonus Points):** If the initial ping returns non-200 or times out, the workflow **pauses for 3 seconds** via a Wait node and dispatches a **second verification ping**.
  - If the second ping also fails &rarr; fires a **CRITICAL OUTAGE ALERT**.
  - If the second ping succeeds &rarr; logs a **Transient Flap Warning** rather than triggering false-positive pager alarms.
- **Daily Summary Accumulator:** Logs successful checks to an ongoing metrics ledger for daily availability reporting.

---

## 5. Loom Video Presentation Script

We have prepared a turnkey walkthrough script in [`LOOM_WALKTHROUGH_SCRIPT.md`](./LOOM_WALKTHROUGH_SCRIPT.md) formatted with exact timestamps, talking points, and screen transitions to make recording a 3-minute video effortless.

---

## 6. Import & Execution Guide for Reviewers

### Importing Workflows into n8n
1. Open your n8n instance (Cloud or self-hosted).
2. Go to **Workflows** &rarr; click the **⋮** menu in the top right &rarr; select **Import from File**.
3. Select `Task2_Workflow_Subrata_Ghosh.json` or `Bonus_UptimeMonitor_Subrata_Ghosh.json`.
4. (Optional) Set an environment variable or edit the webhook node URL to point to your Discord/Slack channel.
5. Click **Test workflow** &bull; all nodes will execute in real-time with live GitHub and Conduit API data!
