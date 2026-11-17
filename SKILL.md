---
name: objc-to-swiftui-migration
description: Migrate legacy iOS projects written in Objective-C, including .h/.m, XIB, and Storyboard files, into native Swift and SwiftUI. Use when the user asks to migrate, port, rewrite, or modernize an existing UIKit/Objective-C app or screen into SwiftUI. Performs project inventory, Interface Builder XML analysis, dependency and behavior mapping, staged implementation, build validation, and visual/functional parity checks. The target is native SwiftUI; do not wrap whole legacy screens in UIKit representables.
---

# Objective-C / UIKit to Native SwiftUI Migration

## Mission

Migrate an existing iOS application or selected feature from Objective-C + UIKit + XIB + Storyboard to Swift + native SwiftUI while preserving externally observable behavior and visual intent.

**Default target:** native SwiftUI views and navigation. UIKit is not the target UI implementation.

**Non-goals:** mechanical syntax translation, blind XML-to-view conversion, wholesale replacement without understanding dependencies, or claiming parity without running checks.

## Hard rules

1. Never start by rewriting files. First inventory the project and produce a migration plan.
2. Treat `.h/.m`, `.xib`, `.storyboard`, asset catalogs, plist/configuration, routing, and tests as one connected system.
3. Parse XIB and Storyboard as XML. Reconstruct the actual hierarchy from `document` / `objects` / `subviews`, not from source order alone.
4. Model constraints relative to their actual `firstItem` and `secondItem`, attributes, multiplier, constant, priority, and safe-area/layout-guide anchors. Never assume screen coordinates when the constraint is parent-relative.
5. Trace every IBOutlet, IBAction, segue, reuse identifier, custom class, module, storyboard identifier, initial controller, navigation relationship, and dependency injection path.
6. Separate business behavior from UIKit lifecycle and rendering. Preserve business rules; redesign UI state using SwiftUI state/data flow.
7. Prefer native SwiftUI: `VStack`, `HStack`, `ZStack`, `Grid`, `LazyVGrid`, `ScrollView`, `List`, `NavigationStack`, `TabView`, `sheet`, `popover`, `alert`, `confirmationDialog`, `@State`, `@Binding`, `@Observable` / `ObservableObject`, and `@Environment`.
8. Do not use `UIViewRepresentable` or `UIViewControllerRepresentable` to wrap an entire legacy screen, controller, or custom view hierarchy. A narrow bridge is allowed only for a system capability with no reasonable SwiftUI equivalent; document the limitation and isolate the bridge.
9. Do not invent missing behavior, constraints, API contracts, validation rules, or design values. Mark unknowns and ask only for information that blocks safe implementation.
10. Keep old and new implementations separate during migration. Do not delete legacy files until parity checks pass and the user approves removal.
11. Preserve project conventions where useful, but do not carry UIKit architecture into SwiftUI merely for familiarity.
12. Build and test after each migration slice. Report actual command results; never claim a build or test passed unless it was run successfully.


## Mandatory incremental migration and human approval gate

This section has higher priority than convenience, speed, or an agent's judgment that adjacent work would be helpful.

### Core rule

**Never migrate the whole project in one pass. Never expand an approved batch without explicit user approval.**

The default unit of work is one small, independently verifiable vertical slice:
- one screen, one reusable component, or one tightly coupled sub-feature;
- only the source files, assets, tests, and routing files strictly required for that slice;
- prefer the smallest representative slice for the first implementation.

Do not interpret "migrate this project" or "continue" as approval to modify every related file.

### Batch 0 — Analysis only

Before the first code edit:
1. Inventory and analyze the project.
2. Recommend a migration order.
3. Select one small first batch and explain why it is representative and low-risk.
4. List the exact files proposed for modification, creation, deletion, or renaming.
5. List expected behavior, dependencies, tests, risks, and acceptance criteria.
6. Wait for the user's approval before editing.

No source-code edits are allowed in Batch 0. Analysis reports may be created only when the user has authorized report generation or the workflow requires them.

### Batch 1 — First limited implementation

After approval:
1. Treat the approved file list and scope as a strict allowlist.
2. Implement only the first approved slice.
3. Do not opportunistically refactor, rename, reformat, or modernize unrelated code.
4. Do not modify shared infrastructure, app-wide navigation, project settings, deployment targets, signing, dependencies, or unrelated assets unless explicitly included in the approved batch.
5. If a newly discovered dependency requires out-of-scope changes, stop and explain the dependency. Propose a revised file list and wait for approval.
6. Do not delete or disable the legacy implementation.

The first batch should be deliberately small. If a screen depends on a shared component, migrate only the minimum needed to demonstrate the approach; otherwise use a narrowly scoped adapter-free SwiftUI implementation and leave the shared component for a separately approved batch.

### Mandatory checkpoint after every batch

After implementation:
1. Run the available build and targeted tests.
2. Review `git diff` and `git status`.
3. Compare behavior and layout against the baseline where evidence is available.
4. Update the migration ledger and validation report.
5. Report exact files changed, actual command results, unresolved issues, and deviations from the approved scope.
6. Present the next proposed batch separately.

Then **STOP**. Do not begin the next batch until the user explicitly approves it.

### What counts as approval

Approval must be an unambiguous user response referring to the current batch, for example:
- "OK，继续下一批"
- "这一批通过，继续"
- "确认，按这个范围修改"

A request for explanation, a question, silence, or a general statement such as "看起来不错" is not approval to expand the scope.

Approval of one batch does not authorize later batches. Each new batch requires its own approval.

### If the batch fails acceptance

- Do not move to the next batch.
- Fix only defects within the current approved scope.
- If the fix requires touching files outside the allowlist, stop and request approval for the additional files.
- Re-run the relevant build/tests and update the report.
- Ask the user to re-check the corrected batch.

### Batch sizing and scope changes

- Default: one screen or one reusable component per batch.
- A batch may include tightly coupled files such as a View, its state model, a focused service interface, and tests, but explain why they belong together.
- Do not set an arbitrary file-count limit when a screen genuinely requires multiple files; instead keep the functional scope narrow and make every file's purpose explicit.
- Any scope expansion, additional screen, broad refactor, dependency upgrade, or project-setting change requires separate approval.

### Required checkpoint response

Use this format after each batch:

```text
Batch N — [feature / screen]

Approved scope:
- ...

Changed files:
- ...

Build and tests:
- [command] — [actual result]

Parity review:
- Visual:
- Behavior:
- Navigation:
- Accessibility:

Known gaps:
- ...

Out-of-scope findings (not changed):
- ...

Proposed Batch N+1:
- Goal:
- Exact files:
- Why this is the next smallest safe slice:

Status: WAITING FOR USER APPROVAL
```

Do not append implementation for Batch N+1 to the same response or continue editing while waiting.

## Workflow

### Phase 0 — Establish scope and baseline

- Determine repository root, Xcode project/workspace, scheme, target, deployment target, Swift version, package/dependency manager, app entry point, and selected migration scope.
- Ask for the target screen/feature only if the user has not specified a scope and the repository is too large to migrate safely in one pass.
- Inspect current build settings and tests.
- Capture baseline screenshots or request them if visual parity is required and no runnable baseline exists.
- Do not change deployment target or project settings without approval.

Deliver: `migration/00-baseline.md`.

### Phase 1 — Project inventory

Run:

```bash
python3 scripts/inventory_project.py /path/to/project --out migration/inventory
```

Inventory:
- Objective-C / Swift source files.
- XIB / Storyboard files.
- asset catalogs and image/font resources.
- app and scene entry points.
- project targets, schemes, build settings where discoverable.
- references between source and Interface Builder files where discoverable.

Then inspect relevant files and dependencies. The inventory script is a locator, not a complete semantic analyzer.

Deliver:
- `migration/inventory/project-inventory.json`
- `migration/inventory/project-inventory.md`
- `migration/01-scope-and-dependencies.md`

### Phase 2 — Interface Builder analysis

Run:

```bash
python3 scripts/parse_interface_builder.py path/to/View.xib --out migration/ib
python3 scripts/parse_interface_builder.py path/to/Main.storyboard --out migration/ib
```

For every relevant XIB / Storyboard:
- identify root object and all nested objects;
- reconstruct view/controller containment;
- extract class, module, id, custom class, reuse identifier, storyboard identifier;
- extract constraints and layout guides;
- extract outlets, actions, segues, relationships, connections;
- note intrinsic content size, content hugging/compression resistance, stack-view settings, safe areas, scroll content/layout guides, priorities, and ambiguous/missing references;
- map constraints to SwiftUI layout semantics.

Validate parser output against Xcode Interface Builder and source code. XML alone cannot reveal runtime-created views, conditional constraints, custom drawing, or all intrinsic sizing behavior.

Deliver:
- `migration/ib/<file>.json`
- `migration/02-interface-builder-analysis.md`
- a view-tree diagram or indented tree in the report.

### Phase 3 — Objective-C behavior and architecture analysis

For each selected feature, inspect:
- public headers and implementation;
- inheritance and category extensions;
- properties, ivars, initialization paths;
- `viewDidLoad`, `viewWillAppear`, `viewDidAppear`, layout callbacks and teardown;
- target-action, delegate/data source, notifications, KVO, timers, gestures;
- RAC / ReactiveObjC chains and command lifecycles;
- networking, persistence, caches, analytics, permissions, file access;
- navigation and presentation;
- threading and cancellation;
- error, empty, loading, retry, and offline states.

Build a behavior matrix:

| Legacy element | Current responsibility | SwiftUI destination | State / event | Verification |
|---|---|---|---|---|

Do not mechanically convert `viewDidLoad` into `onAppear`. Identify whether work is one-time initialization, view visibility work, state reaction, task, or resource lifecycle.

Deliver: `migration/03-behavior-map.md`.

### Phase 4 — SwiftUI design

Before coding, define:
- feature/module boundaries;
- view composition tree;
- state ownership and data flow;
- models and service protocols;
- navigation routes and presentation state;
- async work and cancellation;
- accessibility identifiers and labels;
- design tokens, typography, spacing, colors, assets;
- minimum OS compatibility strategy.

Default architecture:
- `Feature/Views`: small composable SwiftUI views;
- `Feature/ViewModels` or `Feature/State`: presentation state and user intents;
- `Domain`: business models and use cases where justified;
- `Data`: API/repository implementations;
- `Navigation`: typed routes and presentation coordination;
- `DesignSystem`: reusable tokens and components.

Use the simplest architecture that fits the existing app. Do not create a ViewModel for every trivial view. Prefer `@Observable` on supported deployment targets; otherwise use `ObservableObject` / `@StateObject` as appropriate. Keep business logic out of `body`.

Deliver: `migration/04-swiftui-design.md`.

### Phase 5 — Implement in vertical slices

For each screen/feature:
1. Create Swift models and service interfaces.
2. Port business rules and data handling.
3. Implement state transitions and async tasks.
4. Build the SwiftUI hierarchy from the verified view tree.
5. Recreate navigation and presentations.
6. Reuse assets and fonts; preserve image rendering modes and content modes.
7. Add accessibility and stable identifiers.
8. Add unit/UI tests.
9. Build and compare with baseline.
10. Update the migration ledger.

Keep the old route available until the new route is verified. Avoid running both implementations' side effects simultaneously.

### Phase 6 — Validation gates

A migration slice is complete only when all applicable gates pass:

- **Build:** selected target and scheme compile.
- **Behavior:** every mapped action, state, validation, navigation and error path is covered.
- **Layout:** hierarchy, alignment, sizing, scrolling, safe areas, keyboard behavior, Dynamic Type and orientation are checked.
- **Visual:** screenshots compared at the same device, OS, size, content and state.
- **Accessibility:** VoiceOver labels, traits, order, focus and Dynamic Type checked.
- **Lifecycle:** repeated navigation, dismissal, background/foreground and task cancellation checked.
- **Performance:** scrolling, large lists, image loading and repeated state updates checked.
- **Regression:** existing tests and critical flows pass.

Record failures and unresolved differences. Do not label a slice “complete” while critical parity gaps remain.

### Phase 7 — Cutover and cleanup

Only after user approval:
- switch routing / app entry to the SwiftUI implementation;
- remove obsolete storyboard/XIB references from build settings and project;
- remove dead Objective-C UI code and unused resources;
- retain required Objective-C interoperability only if non-UI legacy libraries still require it;
- run a clean build and regression suite;
- update documentation.

## Required deliverables

For each migration scope, maintain:

```text
migration/
├── 00-baseline.md
├── 01-scope-and-dependencies.md
├── 02-interface-builder-analysis.md
├── 03-behavior-map.md
├── 04-swiftui-design.md
├── 05-implementation-log.md
├── 06-validation-report.md
├── inventory/
└── ib/
```

Also update `templates/migration-ledger.csv` or an equivalent table with status per screen and legacy file.

## Completion report format

1. Scope migrated.
2. Legacy files analyzed.
3. New Swift files created/changed.
4. Behavior mapping summary.
5. UIKit bridges, if any, with justification.
6. Build/test commands and actual results.
7. Visual/functional differences still open.
8. Legacy files safe to remove vs. retained.
9. Next recommended slice.

## Safety and repository hygiene

- Inspect `git status` before editing; never overwrite unrelated user changes.
- Make focused changes; avoid broad formatting or unrelated refactors.
- Do not modify signing, provisioning, bundle identifiers, entitlements, production endpoints, secrets, or deployment target without approval.
- Do not delete legacy files or assets before explicit approval.
- If build/test execution is unavailable, state that validation is unverified.
