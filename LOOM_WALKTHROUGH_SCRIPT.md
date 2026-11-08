# Loom Video Presentation Script

**Author:** Subrata Ghosh  
**Role:** Automation & QA Developer Candidate  
**Target Video Duration:** 3 – 4 Minutes  
**Tools Needed:** Loom (or screen recorder), Browser with tabs open (GitHub Repo, PDF Report, n8n Canvas/Screenshots, Live Conduit app).

---

## 🎬 Pre-Recording Checklist & Tab Setup
Before hitting record on Loom, open these tabs in your browser in order:
1. **Tab 1:** GitHub Repository / Project root (`README.md`).
2. **Tab 2:** `Task1_QA_Report_Subrata_Ghosh.pdf` (opened in browser PDF viewer, showing Bug Table & RCA).
3. **Tab 3:** Live Conduit Web App (`https://conduit.bondaracademy.com/editor`).
4. **Tab 4:** `screenshots/task2_workflow_canvas.png` and `screenshots/task2_execution_output.png`.
5. **Tab 5:** `screenshots/bonus_uptime_monitor_canvas.png`.

---

## 🎙️ Spoken Script & Screen Transitions

### Section 1: Introduction & Context (0:00 – 0:35)
**Screen to Show:** *Tab 1 (GitHub Repo README / Camera bubble in corner)*

> *"Hi everyone, my name is Subrata Ghosh, and this is my walkthrough for the Automation & QA Developer assessment.*  
>  
> *In this project, I tackled two core objectives:*  
> *First, conducting a thorough QA and architectural audit of an AI-assisted, 'vibe-coded' web application that users reported felt broken, including a deep root-cause analysis.*  
> *Second, building production-ready n8n automation workflows with multi-API enrichment, robust error handling, and a bonus uptime monitor with anti-flap retry logic.*  
>  
> *Let’s dive right into Task 1."*

---

### Section 2: Task 1 — Web App QA & Root Cause Analysis (0:35 – 1:45)
**Screen to Show:** *Tab 2 (`Task1_QA_Report_Subrata_Ghosh.pdf` & Tab 3 live app)*

> *"For Task 1, I exercised the full user journey on the RealWorld Conduit web app—sign-up, authentication, article creation with markdown, editing, deletion, settings, and logout.*  
>  
> *I documented 6 significant issues in the standard bug table, categorized by severity:*  
> 1. *First, a high-severity **state desynchronization bug** where client-side navigation between routes causes the top navigation bar to completely vanish, stranding logged-in users.*  
> 2. *Second, an **instant, destructive article deletion** that executes on a single click without any confirmation modal or undo grace period.*  
> 3. *Third, **stale validation error messages** that stay frozen on screen even while the user is actively entering valid text.*  
> 4. *Fourth, a **settings form initialization bug** where fields load completely blank instead of pre-populating with user data, risking profile overwrites.*  
> 5. *And fifth, a security concern with **raw JWT tokens stored in plain-text localStorage** rather than secure httpOnly cookies.*  
>  
> *For the Root-Cause Analysis, I focused on the disappearing navigation header. In Angular's reactive architecture, the `HeaderComponent` subscribes to a `currentUser$` observable. Because this stream wasn't configured with replay buffering (`shareReplay(1)`), when child routes activate, the local component re-renders before user state resolves, evaluating `*ngIf="currentUser"` to falsy.  
> To fix this in production, we pipe the observable through `shareReplay({ bufferSize: 1, refCount: false })`, utilize Angular’s declarative `async` pipe in the template, attach route resolvers, and guard against regressions with Playwright E2E tests."*

---

### Section 3: Task 2 — n8n Morning Brief API Integration (1:45 – 2:50)
**Screen to Show:** *Tab 4 (`screenshots/task2_workflow_canvas.png` and `task2_execution_output.png`)*

> *"Moving on to Task 2, I designed an automated 'Morning Brief' workflow in n8n for our engineering and QA team.*  
>  
> *Here is the architecture:*  
> • *It supports dual triggers: a **Schedule Trigger** running hourly for automated production briefs, and a **Webhook Trigger** for on-demand execution.*  
> • *For the first API call, it queries the **GitHub REST Search API** for trending automation repositories with over 1,000 stars.*  
> • *The **Code node** cleans, normalizes, and filters the top 5 projects—formatting star numbers (like 209.8k) and extracting the #1 ranked project.*  
> • *For the second API call, it dynamically enriches the #1 repository by hitting the **GitHub Commits API** to fetch its latest commit SHA, message, author, and timestamp.*  
> • *An **IF node** evaluates a 50,000-star threshold. If met, it formats an eye-catching **Mega-Tier Spotlight Digest**; otherwise, it produces a standard morning digest.*  
> • *Finally, the digest is posted to our Discord or Slack webhook.*  
>  
> *Crucially, it **never crashes silently**: HTTP nodes have `continueOnFail: true`, validation IF nodes route failed searches to an `API 1 Error Fallback Logger`, and a dedicated `Global Error Trigger` captures unhandled exceptions with execution IDs and node stack traces."*

---

### Section 4: Bonus Task — Uptime Sentinel with Retry Logic (2:50 – 3:35)
**Screen to Show:** *Tab 5 (`screenshots/bonus_uptime_monitor_canvas.png`)*

> *"I also completed the Bonus Task by building an **Uptime Sentinel** that pings our Conduit web application every 5 minutes.*  
>  
> *Here are the key engineering features:*  
> 1. *It tracks **response-time latency in milliseconds**. If response time exceeds 1,500ms, it flags a performance degradation warning.*  
> 2. *I implemented **smart retry logic**: if the initial health ping fails or returns non-200, the workflow does not immediately sound the alarm. It pauses for 3 seconds via a Wait node and dispatches a second verification ping.*  
> 3. *If the second attempt also fails, it posts a **Critical Outage Alert** to the operations channel with HTTP status codes and timestamps.*  
> 4. *If it recovers on retry, it logs a **Transient Flap Warning**, preventing false-positive pager fatigue.*  
> 5. *Healthy pings feed directly into a daily summary metrics accumulator."*

---

### Section 5: Conclusion (3:35 – 3:55)
**Screen to Show:** *Tab 1 (GitHub Repo)*

> *"All deliverables are committed to this repository:*  
> • *The full PDF QA report with annotated screenshots,*  
> • *Both exported n8n workflow JSON files ready for immediate import,*  
> • *And complete technical documentation in the README.*  
>  
> *Thank you for your time and review, and I look forward to discussing my technical approach in the follow-up interview!"*

---

## 💡 Quick Tips for Recording
- Keep your camera bubble in the lower-left or lower-right corner.
- Speak with natural enthusiasm and confidence.
- Use your mouse cursor to point to specific nodes on the canvas and rows in the bug table as you speak.
- If you stumble, pause for 2 seconds and re-say the sentence—Loom lets you trim easily!

