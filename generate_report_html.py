import os
import base64
from pathlib import Path

def encode_image(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

img_navbar = encode_image("screenshots/bug_disappearing_navbar.png")
img_validation = encode_image("screenshots/bug_stale_validation.png")
img_settings = encode_image("screenshots/bug_blank_settings.png")
img_delete = encode_image("screenshots/article_view_with_delete_action.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Task 1 — Web App QA & Debug Report</title>
<style>
  @page {{
    size: A4;
    margin: 14mm 16mm 14mm 16mm;
    @bottom-right {{
      content: counter(page);
    }}
  }}
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.5;
    font-size: 13px;
    margin: 0;
    padding: 0;
  }}
  .header {{
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 12px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .header h1 {{
    margin: 0 0 4px 0;
    font-size: 22px;
    color: #0f172a;
    font-weight: 700;
  }}
  .header .subtitle {{
    font-size: 13px;
    color: #64748b;
    margin: 0;
  }}
  .meta-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 20px;
  }}
  .meta-item .label {{
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 2px;
  }}
  .meta-item .val {{
    font-size: 12px;
    color: #0f172a;
    font-weight: 600;
  }}
  h2 {{
    font-size: 15px;
    color: #0f172a;
    border-left: 3px solid #3b82f6;
    padding-left: 8px;
    margin: 20px 0 10px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  p {{
    margin: 0 0 10px 0;
    color: #334155;
  }}
  .summary-card {{
    background-color: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 6px;
    padding: 12px 14px;
    margin-bottom: 18px;
  }}
  .summary-card p {{
    margin: 0;
    font-size: 12.5px;
    color: #1e40af;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 22px;
    font-size: 11px;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 600;
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}
  .badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 9.5px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }}
  .badge-critical {{ background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }}
  .badge-high {{ background-color: #ffedd5; color: #9a3412; border: 1px solid #fed7aa; }}
  .badge-medium {{ background-color: #fef9c3; color: #854d0e; border: 1px solid #fef08a; }}
  .badge-low {{ background-color: #e0f2fe; color: #075985; border: 1px solid #bae6fd; }}

  .rca-container {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 14px 16px;
    margin-bottom: 20px;
  }}
  .rca-subheading {{
    font-weight: 700;
    color: #0f172a;
    margin: 8px 0 4px 0;
    font-size: 12px;
  }}
  .code-block {{
    background-color: #1e293b;
    color: #f8fafc;
    padding: 10px 12px;
    border-radius: 4px;
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 10.5px;
    margin: 8px 0;
    overflow-x: auto;
  }}

  .evidence-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 10px;
    page-break-inside: avoid;
  }}
  .evidence-box {{
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    overflow: hidden;
    background: #f8fafc;
  }}
  .evidence-box img {{
    width: 100%;
    height: auto;
    display: block;
    border-bottom: 1px solid #e2e8f0;
  }}
  .evidence-caption {{
    padding: 6px 10px;
    font-size: 10.5px;
    color: #475569;
    font-weight: 500;
  }}
  .page-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>QA & Web App Debugging Assessment Report</h1>
    <div class="subtitle">Comprehensive Quality Audit & Root-Cause Analysis for AI-Assisted ("Vibe-Coded") Web Applications</div>
  </div>
  <div style="text-align: right;">
    <div style="font-weight: 700; color: #0f172a;">Task 1 Deliverable</div>
    <div style="font-size: 11px; color: #64748b;">Role: Automation & QA Developer</div>
  </div>
</div>

<div class="meta-grid">
  <div class="meta-item">
    <div class="label">Candidate Name</div>
    <div class="val">Subrata Ghosh</div>
  </div>
  <div class="meta-item">
    <div class="label">Target Application</div>
    <div class="val">RealWorld Conduit Live Web App</div>
  </div>
  <div class="meta-item">
    <div class="label">Date of Assessment</div>
    <div class="val">November 8, 2026</div>
  </div>
  <div class="meta-item">
    <div class="label">App URL / Endpoint</div>
    <div class="val">conduit.bondaracademy.com</div>
  </div>
</div>

<h2>1. Executive Summary & Investigation Context</h2>
<div class="summary-card">
  <p><strong>Scenario:</strong> Handed a web application built using AI-assisted ("vibe coding") techniques that users reported as "feeling broken". Our objective was to thoroughly exercise the core user journeys (Sign-up, Authentication, Content Creation, Markdown Editor, Edit Article, Delete Article, Profile Settings, and Logout), identify high-impact functional, architectural, security, and UX defects, and present a rigorous Root Cause Analysis (RCA) with production remediation steps.</p>
</div>
<p>
  AI-assisted vibe-coded applications often achieve visually compelling mockups rapidly but frequently omit defensive programming paradigms: asynchronous state management synchronization, reactive form cleanup, destructive action confirmation guards, secure session handling, and accessibility attributes. During this audit, <strong>6 distinct issues</strong> were identified, documented, and classified.
</p>

<h2>2. Comprehensive Bug Report Table (Section 5 Template)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 4%;">#</th>
      <th style="width: 20%;">Title / Summary</th>
      <th style="width: 25%;">Steps to Reproduce</th>
      <th style="width: 26%;">Expected vs Actual</th>
      <th style="width: 10%;">Severity</th>
      <th style="width: 15%;">Suspected Cause</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1</strong></td>
      <td><strong>Disappearing Navigation Header & Desynchronized Auth State</strong><br><small>User session links vanish during SPA transitions.</small></td>
      <td>1. Log in or register an account.<br>2. Confirm logged-in navbar (Home, New Article, Settings, Profile).<br>3. Navigate to <code>/editor</code>, edit an article, or go to <code>/profile/:user</code>.<br>4. Inspect the top header.</td>
      <td><strong>Expected:</strong> Navbar consistently retains user navigation links across all SPA routes.<br><br><strong>Actual:</strong> Header links disappear completely; only the raw "conduit" brand text displays. User is stranded without navigation controls until a browser refresh.</td>
      <td><span class="badge badge-high">High</span></td>
      <td>Unicast or un-replayed <code>currentUser$</code> BehaviorSubject in <code>UserService</code> drops state upon child router activation; <code>*ngIf="currentUser"</code> evaluates falsy.</td>
    </tr>
    <tr>
      <td><strong>2</strong></td>
      <td><strong>Immediate Irreversible Content Deletion Without Confirmation</strong><br><small>Accidental single-click deletes user articles permanently.</small></td>
      <td>1. Publish an article.<br>2. Open article view (<code>/article/:slug</code>).<br>3. Click the red "Delete Article" button.</td>
      <td><strong>Expected:</strong> A confirmation modal or <code>window.confirm()</code> warning asks the user to confirm before permanent deletion.<br><br><strong>Actual:</strong> Article is immediately destroyed via <code>DELETE /api/articles/:slug</code> on a single click with zero prompt and no undo grace period.</td>
      <td><span class="badge badge-high">High</span></td>
      <td>Click handler invokes <code>ArticlesService.destroy()</code> directly without intercepting user confirmation or dispatching a confirmation dialog.</td>
    </tr>
    <tr>
      <td><strong>3</strong></td>
      <td><strong>Stale Validation Error Banner Persisting on Input Correction</strong><br><small>Error messages remain frozen while user is actively typing.</small></td>
      <td>1. Go to New Article (<code>/editor</code>).<br>2. Click "Publish Article" with empty fields to trigger 422 error banner ("title can't be blank").<br>3. Focus into "Article Title" and type a valid title.</td>
      <td><strong>Expected:</strong> Error banner clears immediately upon input change or field focus.<br><br><strong>Actual:</strong> "title can't be blank" remains visibly rendered above the form even while the user actively types a valid title, misinforming the user.</td>
      <td><span class="badge badge-medium">Medium</span></td>
      <td>Component error state is bound only to HTTP rejection responses and does not subscribe to form control <code>valueChanges</code> to clear errors upon user input.</td>
    </tr>
    <tr>
      <td><strong>4</strong></td>
      <td><strong>Settings Form Profile Pre-Population Failure (Blank Form)</strong><br><small>Form fields load empty, risking profile data overwrite.</small></td>
      <td>1. Log in with an established user profile.<br>2. Navigate to Settings (<code>/settings</code>).<br>3. Inspect the Username and Email input fields.</td>
      <td><strong>Expected:</strong> Settings form inputs are populated with the active user's existing profile data.<br><br><strong>Actual:</strong> Form inputs are completely blank. Submitting edits to Bio sends empty fields to the API, risking data loss/overwrite.</td>
      <td><span class="badge badge-medium">Medium</span></td>
      <td>Reactive form is initialized with blank default strings synchronously before the asynchronous user profile API response resolves, omitting <code>patchValue()</code>.</td>
    </tr>
    <tr>
      <td><strong>5</strong></td>
      <td><strong>Insecure Storage of Plain-Text JWT in <code>localStorage</code></strong><br><small>Auth token vulnerable to exfiltration via XSS.</small></td>
      <td>1. Sign in or register.<br>2. Open DevTools Console.<br>3. Run <code>window.localStorage.getItem('jwtToken')</code>.</td>
      <td><strong>Expected:</strong> Authentication session credentials should be stored in secure, <code>httpOnly</code>, <code>SameSite=Strict</code> cookies.<br><br><strong>Actual:</strong> Long-lived JWT token is stored in unencrypted <code>localStorage</code>, vulnerable to extraction by any injected script or XSS flaw.</td>
      <td><span class="badge badge-high">High</span></td>
      <td>Client-side architectural shortcut relying on browser <code>localStorage</code> instead of server-managed secure session cookies.</td>
    </tr>
    <tr>
      <td><strong>6</strong></td>
      <td><strong>Accessibility & DOM Non-Compliance: Missing Input Labels & Attributes</strong><br><small>Blocks screen readers and breaks password managers.</small></td>
      <td>1. Open <code>/login</code> or <code>/register</code>.<br>2. Inspect form DOM inputs in Elements tab & Console.</td>
      <td><strong>Expected:</strong> Inputs feature accessible <code>&lt;label&gt;</code> tags, unique <code>id</code>/<code>name</code> attributes, and <code>autocomplete</code> hints.<br><br><strong>Actual:</strong> Inputs lack labels, IDs, and autocomplete attributes, generating DOM console warnings and blocking assistive technologies.</td>
      <td><span class="badge badge-medium">Medium</span></td>
      <td>Minimalist UI template styling omitting WAI-ARIA and semantic HTML standards during rapid prototyping.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h2>3. In-Depth Root-Cause Analysis (Issue #1: Disappearing Navigation Header)</h2>
<div class="rca-container">
  <div class="rca-subheading">1. What is Happening?</div>
  <p>
    When an authenticated user navigates between routes inside the Single Page Application (e.g. from the home feed to the article editor, an existing article, or the user profile page), the top navigation header abruptly loses its authenticated elements ("Home", "New Article", "Settings", and user profile avatar), rendering only the raw brand link "conduit". The user is left in a broken visual state with no access to core navigation links until they execute a full browser hard refresh.
  </p>

  <div class="rca-subheading">2. Why is it Happening?</div>
  <p>
    This defect is caused by an architectural desynchronization between Angular's reactive authentication state and the component router lifecycle. The <code>HeaderComponent</code> binds its navigation elements via an <code>*ngIf="currentUser"</code> directive backed by a local property populated through a manual subscription to <code>UserService.currentUser$</code>. When internal client-side navigation occurs, child routes trigger without invoking the root application bootstrap sequence. Because the underlying observable in <code>UserService</code> was implemented as a cold or un-replayed subject rather than a multicasted replay stream, late-subscribing or re-rendering components fail to receive the cached user session object. Consequently, the user object evaluates to <code>undefined</code>/<code>null</code>, and the template removes the navigation elements from the DOM.
  </p>

  <div class="rca-subheading">3. How Would You Fix It? (Production Remediation)</div>
  <p>
    To resolve this permanently and build resilience into the application, implement the following four-phase fix:
  </p>
  <ul>
    <li>
      <strong>Replay Authentication State:</strong> In <code>UserService</code>, ensure the <code>currentUser$</code> stream uses a <code>BehaviorSubject</code> or is piped through <code>shareReplay({{ bufferSize: 1, refCount: false }})</code>. This guarantees that any component subscribing at any point in the router lifecycle immediately receives the current user object:
      <div class="code-block">
// user.service.ts
private currentUserSubject = new BehaviorSubject&lt;User | null&gt;(this.getStoredUser());
public currentUser$ = this.currentUserSubject.asObservable().pipe(distinctUntilChanged(), shareReplay(1));
      </div>
    </li>
    <li>
      <strong>Use Declarative Async Pipe in Header Template:</strong> Eliminate manual subscription management inside <code>HeaderComponent</code> and leverage Angular's <code>async</code> pipe, which automatically handles subscription lifecycles, change detection, and template unwrapping:
      <div class="code-block">
&lt;!-- header.component.html --&gt;
&lt;ng-container *ngIf="currentUser$ | async as user; else guestNav"&gt;
  &lt;ul class="nav navbar-nav pull-xs-right"&gt;
    &lt;li class="nav-item"&gt;&lt;a class="nav-link" routerLink="/"&gt;Home&lt;/a&gt;&lt;/li&gt;
    &lt;li class="nav-item"&gt;&lt;a class="nav-link" routerLink="/editor"&gt;New Article&lt;/a&gt;&lt;/li&gt;
    &lt;li class="nav-item"&gt;&lt;a class="nav-link" routerLink="/settings"&gt;Settings&lt;/a&gt;&lt;/li&gt;
    &lt;li class="nav-item"&gt;&lt;a class="nav-link" [routerLink]="['/profile', user.username]"&gt;{{ user.username }}&lt;/a&gt;&lt;/li&gt;
  &lt;/ul&gt;
&lt;/ng-container&gt;
      </div>
    </li>
    <li>
      <strong>Implement Route Session Resolver:</strong> Add an Angular <code>UserResolver</code> to protected and dependent routes to verify session validity and pre-fetch the authenticated user profile before routing completes.
    </li>
    <li>
      <strong>Automated Regression Suite:</strong> Add automated Playwright end-to-end tests verifying navbar state persistence across sequential route hops (<code>/</code> &rarr; <code>/editor</code> &rarr; <code>/article/:slug</code> &rarr; <code>/settings</code> &rarr; <code>/profile</code>).
    </li>
  </ul>
</div>

<h2>4. Photographic Bug Evidence & UI Inspection</h2>
<div class="evidence-grid">
  <div class="evidence-box">
    <img src="{img_navbar}" alt="Disappearing Navbar Bug">
    <div class="evidence-caption"><strong>Figure 1 (Issue #1):</strong> State Desynchronization on <code>/editor</code> &mdash; Logged-in navigation controls vanish completely from header.</div>
  </div>
  <div class="evidence-box">
    <img src="{img_validation}" alt="Stale Validation Banner">
    <div class="evidence-caption"><strong>Figure 2 (Issue #3):</strong> Stale Validation Error &mdash; "title can't be blank" persists on screen while user actively enters title.</div>
  </div>
  <div class="evidence-box">
    <img src="{img_settings}" alt="Blank Settings Form">
    <div class="evidence-caption"><strong>Figure 3 (Issue #4):</strong> Settings Form Blanking &mdash; Form inputs fail to pre-populate with existing username and email.</div>
  </div>
  <div class="evidence-box">
    <img src="{img_delete}" alt="Instant Delete Action">
    <div class="evidence-caption"><strong>Figure 4 (Issue #2):</strong> Destructive Deletion &mdash; "Delete Article" button executes immediate permanent purge with zero confirmation.</div>
  </div>
</div>

<div style="margin-top: 24px; padding-top: 10px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8;">
  <span>Automation & QA Developer Skills Assessment &bull; Task 1</span>
  <span>Author: Subrata Ghosh &bull; Certified QA Report</span>
</div>

</body>
</html>
"""

with open("Task1_QA_Report_Subrata_Ghosh.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated Task1_QA_Report_Subrata_Ghosh.html successfully.")

