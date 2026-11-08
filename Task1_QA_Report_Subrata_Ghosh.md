# Task 1 — Web App QA & Debug Report

**Candidate Name:** Subrata Ghosh  
**Target Application:** RealWorld Conduit Web App (`https://conduit.bondaracademy.com`)  
**Assessment Date:** November 8, 2026  
**Role:** Automation & QA Developer  

---

## 1. Executive Summary & Context

As part of the Automation & QA Developer assessment, we conducted an end-to-end quality and architectural audit of an AI-assisted ("vibe-coded") web application. Non-technical users reported that the application "feels broken." 

Our investigative mandate was to exercise all primary user journeys:
- User registration and account creation
- User authentication and login persistence
- Content creation (Markdown article editor and tag parsing)
- Content editing and slug handling
- Content deletion and resource teardown
- User settings, profile updates, and session termination (logout)

### Summary of Findings
While the application fulfills baseline happy-path scenarios when navigated in a rigid sequence, it suffers from critical architectural oversights common to AI-generated codebases:
1. **Unstable Asynchronous State Management:** Router events desynchronize from user authentication observables, dropping UI navigation elements upon internal transitions.
2. **Missing Defensive Confirmation Guards:** High-consequence destructive operations (e.g., article deletion) execute on a single click without confirmation modals or undo mechanisms.
3. **Reactive Form Lifecycle Desynchronization:** Input error arrays are statically tied to HTTP rejection responses and do not clear on input revision.
4. **Form Initialization Race Conditions:** Asynchronous profile endpoints fail to patch reactive form controls before initial render.
5. **Insecure Credential Storage:** Long-lived JWT tokens reside in plain-text `localStorage` without XSS mitigations.
6. **Accessibility & Semantic HTML Gaps:** Input controls lack WAI-ARIA labels, unique element identifiers, and autocomplete attributes.

---

## 2. Bug Report Table (Section 5 Template)

| # | Title / Summary | Steps to Reproduce | Expected vs Actual | Severity | Suspected Cause |
|---|---|---|---|---|---|
| **1** | **Disappearing Navigation Header & Desynchronized Auth State**<br>User session links vanish during client-side SPA routing transitions. | 1. Log in or register an account.<br>2. Confirm logged-in header shows "Home", "New Article", "Settings", and username.<br>3. Navigate to `/editor`, publish/edit an article, or visit `/profile/:user`.<br>4. Inspect the top header. | **Expected:** Top navbar consistently displays authenticated navigation links across all internal routes.<br><br>**Actual:** Navigation controls vanish entirely; only the raw "conduit" brand text remains. User is stranded with no way to navigate without a browser hard refresh. | **High** | The `currentUser$` BehaviorSubject in `UserService` is not shared with replay (`shareReplay(1)`) or is unsubscribed on route activation, causing `*ngIf="currentUser"` to evaluate falsy. |
| **2** | **Immediate Irreversible Content Deletion Without Confirmation**<br>Accidental single click permanently purges user articles without recovery. | 1. Log in and publish an article.<br>2. Open the article page (`/article/:slug`).<br>3. Click the red "Delete Article" button. | **Expected:** A confirmation dialog/modal prompts: *"Are you sure you want to delete this article?"* before destructive action.<br><br>**Actual:** Article is permanently deleted via `DELETE /api/articles/:slug` immediately on click with zero confirmation prompt and no undo grace period. | **High** | Click handler directly invokes `ArticlesService.destroy()` without any `window.confirm()` or modal interception. |
| **3** | **Stale Validation Error Banner Persisting on Input Correction**<br>Error messages remain frozen on screen while user is actively entering valid text. | 1. Navigate to New Article (`/editor`).<br>2. Click "Publish Article" with empty fields to trigger a 422 error ("title can't be blank").<br>3. Click into "Article Title" and type a valid title. | **Expected:** The validation error banner clears immediately when the user modifies or focuses the invalid input field.<br><br>**Actual:** "title can't be blank" remains visibly rendered above the form even while the user actively types a valid title, misinforming the user. | **Medium** | Component error state is bound only to HTTP rejection responses and does not subscribe to form control `valueChanges` to clear errors upon user input. |
| **4** | **Settings Form Profile Pre-Population Failure (Blank Form)**<br>Form controls load blank, risking accidental profile data overwrites. | 1. Log in with an established user account.<br>2. Navigate to Settings (`/settings`).<br>3. Inspect the "Username" and "Email" fields. | **Expected:** Settings form fields are pre-populated with the user's current username, email, bio, and image URL.<br><br>**Actual:** Username and Email fields are completely blank (`""`). Submitting an update to Bio sends empty fields to the API, risking data loss/overwrite. | **Medium** | Reactive form is initialized with blank default strings synchronously before the asynchronous user profile API response resolves, omitting `patchValue()`. |
| **5** | **Insecure Storage of Plain-Text JWT in `localStorage`**<br>Authentication token exposed to client-side script execution and XSS. | 1. Authenticate via login or register.<br>2. Open browser DevTools Console.<br>3. Execute `window.localStorage.getItem('jwtToken')`. | **Expected:** Authentication session tokens should be stored in secure, `httpOnly`, `SameSite=Strict` cookies inaccessible to JavaScript.<br><br>**Actual:** Long-lived JWT token is stored in unencrypted `localStorage`, vulnerable to theft by any injected XSS script or compromised dependency. | **High** | Client-side architectural shortcut relying on browser `localStorage` instead of server-managed secure session cookies. |
| **6** | **Accessibility & DOM Non-Compliance: Missing Input Labels & Attributes**<br>Blocks screen readers and breaks password manager auto-fill. | 1. Open `/login` or `/register`.<br>2. Inspect form DOM inputs in Elements tab & Console. | **Expected:** Every input features accessible `<label>` tags, unique `id`/`name` attributes, and `autocomplete` hints.<br><br>**Actual:** Inputs lack labels, IDs, and autocomplete attributes, generating DOM console warnings and blocking assistive technologies. | **Medium** | Minimalist UI template styling omitting WAI-ARIA and semantic HTML standards during rapid prototyping. |

---

## 3. In-Depth Root-Cause Analysis (Issue #1: Disappearing Navigation Header)

### 1. What is Happening?
When an authenticated user navigates between routes inside the Single Page Application (such as moving from the home feed to an article editor, an existing article, or the user profile page), the top navigation header abruptly loses its authenticated elements ("Home", "New Article", "Settings", and user profile avatar), rendering only the raw brand link "conduit". The user is left in a broken visual state with no access to core navigation links until they execute a full browser hard refresh.

### 2. Why is it Happening?
This defect is caused by an architectural desynchronization between Angular's reactive authentication state and the component router lifecycle. The `HeaderComponent` binds its navigation elements via an `*ngIf="currentUser"` directive backed by a local property populated through a manual subscription to `UserService.currentUser$`. When internal client-side navigation occurs, child routes trigger without invoking the root application bootstrap sequence. Because the underlying observable in `UserService` was implemented as a cold or un-replayed subject rather than a multicasted replay stream, late-subscribing or re-rendering components fail to receive the cached user session object. Consequently, the user object evaluates to `undefined`/`null`, and the template removes the navigation elements from the DOM.

### 3. How Would You Fix It? (Production Remediation)
To resolve this permanently and build resilience into the application, implement the following four-phase fix:

1. **Replay Authentication State:**  
   In `UserService`, ensure the `currentUser$` stream uses a `BehaviorSubject` or is piped through `shareReplay({ bufferSize: 1, refCount: false })`. This guarantees that any component subscribing at any point in the router lifecycle immediately receives the current user object:
   ```typescript
   // user.service.ts
   private currentUserSubject = new BehaviorSubject<User | null>(this.getStoredUser());
   public currentUser$ = this.currentUserSubject.asObservable().pipe(
     distinctUntilChanged(),
     shareReplay({ bufferSize: 1, refCount: false })
   );
   ```

2. **Use Declarative Async Pipe in Header Template:**  
   Eliminate manual subscription management inside `HeaderComponent` and leverage Angular's `async` pipe, which automatically handles subscription lifecycles, change detection, and template unwrapping:
   ```html
   <!-- header.component.html -->
   <ng-container *ngIf="currentUser$ | async as user; else guestNav">
     <ul class="nav navbar-nav pull-xs-right">
       <li class="nav-item"><a class="nav-link" routerLink="/">Home</a></li>
       <li class="nav-item"><a class="nav-link" routerLink="/editor">New Article</a></li>
       <li class="nav-item"><a class="nav-link" routerLink="/settings">Settings</a></li>
       <li class="nav-item">
         <a class="nav-link" [routerLink]="['/profile', user.username]">{{ user.username }}</a>
       </li>
     </ul>
   </ng-container>
   ```

3. **Implement Route Session Resolver:**  
   Add an Angular `UserResolver` (`ResolveFn`) to protected and dependent routes to verify session validity and pre-fetch the authenticated user profile before routing completes.

4. **Automated Regression Suite:**  
   Add automated Playwright end-to-end tests verifying navbar state persistence across sequential route hops:
   ```typescript
   test('Navbar maintains authenticated links across all route transitions', async ({ page }) => {
     await loginUser(page, 'qa_tester_subrata@example.com', 'TestingPass123!');
     await expect(page.locator('nav')).toContainText('qa_tester_subrata');
     
     await page.goto('/editor');
     await expect(page.locator('nav')).toContainText('qa_tester_subrata');
     
     await page.goto('/settings');
     await expect(page.locator('nav')).toContainText('qa_tester_subrata');
   });
   ```

---

## 4. Visual Inspection & Photographic Bug Evidence

- **Figure 1:** `screenshots/bug_disappearing_navbar.png` &mdash; State Desynchronization on `/editor` where header links disappear.
- **Figure 2:** `screenshots/bug_stale_validation.png` &mdash; Stale Validation Error where "title can't be blank" persists on input change.
- **Figure 3:** `screenshots/bug_blank_settings.png` &mdash; Settings Form Blanking where Username and Email fields load empty.
- **Figure 4:** `screenshots/article_view_with_delete_action.png` &mdash; Destructive Deletion button executing immediate purge with zero confirmation.

