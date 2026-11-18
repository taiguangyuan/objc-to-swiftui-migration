---
name: objc-to-swiftui-migration
display_name: Objective-C 转 SwiftUI 迁移
display_name_en: Objective-C to SwiftUI Migration
description: Migrate legacy iOS projects written in Objective-C, including .h/.m, XIB, and Storyboard files, into native Swift and SwiftUI. Use when the user asks to migrate, port, rewrite, or modernize an existing UIKit/Objective-C app or screen into SwiftUI. Runs a mandatory pre-flight requirements interrogation (grill-me gate) before any work, then performs project inventory, Interface Builder XML analysis, dependency and behavior mapping, staged implementation, build validation, and visual/functional parity checks. The target is native SwiftUI; do not wrap whole legacy screens in UIKit representables.
description_zh: 把 Objective-C + UIKit + XIB/Storyboard 老项目增量迁移为原生 SwiftUI：动工前先用 grill-me 式需求盘问锁定范围与关键决策，再盘点分析、经确认后逐个切片实现，并做构建、测试与视觉/功能一致性校验。
description_en: "Incrementally migrate legacy Objective-C/UIKit apps (XIB and Storyboard included) to native SwiftUI: run a mandatory grill-me requirements gate first, then inventory and plan, implement one approved vertical slice at a time, and verify with builds, tests and parity checks."
version: 1.0.1
---

# Objective-C / UIKit to Native SwiftUI Migration

## Mission

Migrate an existing iOS application or selected feature from Objective-C + UIKit + XIB + Storyboard to Swift + native SwiftUI while preserving externally observable behavior and visual intent.

**Default target:** native SwiftUI views and navigation. UIKit is not the target UI implementation.

**Non-goals:** mechanical syntax translation, blind XML-to-view conversion, wholesale replacement without understanding dependencies, or claiming parity without running checks.

## Hard rules

**Rule 16 — the pre-flight interrogation gate — precedes every other rule.** No
analysis deliverable, no scope decision, and no source edit may begin until the
grill-me gate described below is CLEARED. The per-batch human-approval gate is
necessary but not sufficient: it approves a *batch*, whereas the interrogation
gate approves the *request itself*.

1. Never start by rewriting files. First inventory the project and produce a migration plan.
2. Treat `.h/.m`, `.xib`, `.storyboard`, asset catalogs, plist/configuration, routing, and tests as one connected system.
3. Parse XIB and Storyboard as XML. Reconstruct the actual hierarchy from `document` / `objects` / `subviews`, not from source order alone.
4. Model constraints relative to their actual `firstItem` and `secondItem`, attributes, multiplier, constant, priority, and safe-area/layout-guide anchors. Never assume screen coordinates when the constraint is parent-relative.
5. Trace every IBOutlet, IBAction, segue, reuse identifier, custom class, module, storyboard identifier, initial controller, navigation relationship, and dependency injection path.
6. Separate business behavior from UIKit lifecycle and rendering. Preserve business rules; redesign UI state using SwiftUI state/data flow.
7. Prefer native SwiftUI: `VStack`, `HStack`, `ZStack`, `Grid`, `LazyVGrid`, `ScrollView`, `List`, `NavigationStack`, `TabView`, `sheet`, `popover`, `alert`, `confirmationDialog`, `@State`, `@Binding`, `@Observable` / `ObservableObject`, and `@Environment`. For reactive state and async work, follow the dedicated policy below.
8. Do not use `UIViewRepresentable` or `UIViewControllerRepresentable` to wrap an entire legacy screen, controller, or custom view hierarchy. A narrow bridge is allowed only for a system capability with no reasonable SwiftUI equivalent; document the limitation and isolate the bridge.
9. Do not invent missing behavior, constraints, API contracts, validation rules, or design values. Mark unknowns and ask only for information that blocks safe implementation.
10. Keep old and new implementations separate during migration. Do not delete legacy files until parity checks pass and the user approves removal.
11. Preserve project conventions where useful, but do not carry UIKit architecture into SwiftUI merely for familiarity.
12. Build and test after each migration slice. Report actual command results; never claim a build or test passed unless it was run successfully.
13. **Never introduce RxSwift (or any third-party reactive framework) by default.** Use Apple's native observation, state and concurrency stack instead. This is a hard technical constraint with the same priority as the rules above; see the dedicated section below for the deployment-target rules, forbidden shortcuts, and the only exception path.
14. **Never copy hard-coded `frame` / coordinate values from Objective-C into SwiftUI.** Translate the layout intent they encode into native SwiftUI layout. See the "Layout and gesture parity constraints" section below.
15. **Gestures must preserve the original operation logic exactly.** Treat every legacy gesture/control event and its full interaction semantics as part of the feature contract, and verify each path before calling a slice complete. See the "Layout and gesture parity constraints" section below.
16. **Run the pre-flight requirements interrogation before any work.** No analysis deliverable and no source edit may be produced until every decision branch of the grill-me gate is resolved and the gate is marked CLEARED. See the dedicated section below and `references/requirements-interrogation.md`.


## Pre-flight grill-me gate — interrogate before any work

This section has the highest priority in the workflow: it runs before Batch 0,
before Phase 0, and before any file is created or edited.

### Purpose

Prevent blind implementation. A migration is expensive to redo, so ambiguity about
scope, deployment target, reactive stack, parity standard, or gesture semantics
must be resolved up front — not discovered halfway through a slice.

### How to run the gate

1. Read `references/requirements-interrogation.md` in full before opening the session.
2. Open by listing the 3–6 top-level decision branches you see, name the most
   foundational one (Scope), and say why you are starting there.
3. Walk one branch at a time. For each question: give your recommended answer with
   a one-line reason, ask, then **stop and wait** for the user's response.
4. Answer factual questions yourself from the repository (Read/Grep, project
   settings, existing reports); only ask about intent, priority, and trade-offs.
5. Treat "it depends" as unresolved: find the deciding condition, resolve it, then
   return to the question. Do not carry an open "it depends" forward.
6. Skip questions already answered by evidence or by an earlier answer, and say so.
7. When all branches are resolved, close with a one-paragraph decision summary and
   declare the gate **CLEARED**.

### The six branches

- **A — Scope and objective:** in/out scope, first slice, definition of done, legacy fate.
- **B — Platform baseline:** deployment target, device/orientation matrix, accessibility/localization, off-limits settings.
- **C — State, reactive technology and concurrency:** state stack derived from the real target, RAC/RxSwift mapping, any genuine exception.
- **D — Visual, layout and gesture parity:** parity standard, frame-intent translation, gesture matrix, navigation model.
- **E — Dependencies and shared infrastructure:** slice boundary around shared code, third-party dependency stance.
- **F — Validation and delivery cadence:** build/test commands, who verifies on device, report location, per-batch approval acknowledgment.

### Gate output and handoff

Write `migration/00-preflight-interrogation.md` from
`templates/00-preflight-interrogation.md`, present the decision summary, and only
then start Batch 0 / Phase 0 — never in the same turn as the questions. If a
blocking question is declined, the gate remains **OPEN**: produce no analysis
deliverables and edit no source; state exactly which branch is blocked and why.


## Reactive technology constraint — native Apple stack first, no RxSwift by default

This section has the same priority as the Hard rules. It applies to every migration slice and must not be traded away for convenience or familiarity with the legacy reactive code.

**Default rule:** do not add RxSwift / RxCocoa, ReactiveObjC / RAC, or any other third-party reactive framework to the migrated SwiftUI code. Apple's native tools are the default and sufficient choice for the overwhelming majority of UI state, data flow and async work. Do not carry a dependency over merely because the legacy Objective-C code used one.

### Deployment-target rules

- **iOS 17+:** prefer `@Observable`, `@State`, `@Environment`, `@Bindable` (and `@Binding` for child views).
- **iOS 16 and below:** use `ObservableObject`, `@Published`, `@StateObject` as required by the project's compatibility target.
- Pick the stack from the project's **actual minimum deployment target**, not from personal preference. Do not raise the deployment target solely to use `@Observable` without approval.

### Async work

- Use **Swift Concurrency** (`async`/`await`, `Task`, `task(id:)`, `.task`, actors, `AsyncSequence`, structured cancellation) for networking, timers, and other asynchronous work.
- Do not introduce a reactive framework only to express async sequences, debounce, throttling or cancellation when a native API can do it cleanly.

### Forbidden shortcuts

- **No Subject for simple state changes.** Do not model plain state or user events with `PassthroughSubject` / `CurrentValueSubject` (or RxSwift `Subject` / `Relay`) when `@State`, `@Binding`, `@Observable` / `ObservableObject` or a plain method suffices.
- **No hand-rolled RACCommand imitation.** Do not build a custom reactive command/action framework to mimic `RACCommand`. Express an action as a Swift method (or closure) plus explicit state such as `isRunning`, `error`, and result, driven by Swift Concurrency and observed natively.
- **No reactive wrapper layer** whose only purpose is to reproduce the old framework's shapes (signals, relays, schedulers, dispose bags) inside SwiftUI.

### The only exception

Introducing a third-party reactive library is allowed **only** when the native stack genuinely cannot meet the requirement gracefully. To take this path, all of the following must hold:

1. Identify the concrete requirement and explain precisely why the native alternatives above cannot satisfy it.
2. Document the justification in `migration/04-swiftui-design.md` before implementation.
3. Get explicit user approval for the new dependency and for any deployment-target or project-setting change it requires.
4. Keep the dependency isolated behind a narrow interface and record where it is used; do not let it become the app-wide architecture.

If the justification cannot be written concretely, do not add the dependency.

### Official references

- [Managing model data in your app](https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app) — Apple
- [Observation framework](https://developer.apple.com/documentation/observation) — Apple
- [Migrating from the Observable Object protocol to the Observable macro](https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro) — Apple


## Layout and gesture parity constraints

This section has the same priority as the Hard rules. Both constraints apply to every migration slice.

### Hard-coded frames — translate intent, never copy coordinates

Legacy Objective-C code frequently sets `frame` / `bounds` / `center` directly, computes rects in `layoutSubviews`, or positions subviews with literal coordinates. Do not carry those numbers into SwiftUI.

**Forbidden:**
- copying `CGRect(x:y:width:height:)` values into `.frame(width:height:)`, `.offset(x:y:)`, or `.position(x:y:)`;
- reproducing device-screen-sized constants from the legacy code;
- using `GeometryReader` plus manual arithmetic to reimplement UIKit frame layout when a layout container expresses the same intent.

**Required:**
1. Record what the frame code is actually doing: relative alignment, proportional sizing, fixed intrinsic size, spacing, safe-area inset, scroll content size, overlay/z-order, or animation target.
2. Rebuild that intent with native SwiftUI tools: `HStack` / `VStack` / `ZStack`, `Spacer`, `padding`, `frame(maxWidth:minWidth:alignment:)`, `aspectRatio`, `alignmentGuide`, `safeAreaInset`, and `GeometryReader` only when genuinely geometry-dependent. Use the `Layout` protocol for custom layout that containers cannot express.
3. Verify at multiple device sizes, orientations, and Dynamic Type sizes. The layout must adapt as the design intends, not merely match one screenshot.
4. If an absolute size is genuinely part of the design (for example a fixed-size icon or a coordinate-based canvas), document why, keep the constants centralized, and call it out in `migration/04-swiftui-design.md`.

### Gestures — preserve the original operation logic exactly

Legacy gesture behavior is part of the feature contract. "It looks the same" is not enough; the operation logic must remain identical, including event phases, thresholds, cancellation, and interaction with other gestures.

Before implementation, build a gesture matrix in `migration/03-behavior-map.md` with one row per recognizer or control event, covering:
- recognizer type and configuration: `UITapGestureRecognizer` (`numberOfTapsRequired`, `numberOfTouchesRequired`), `UILongPressGestureRecognizer` (`minimumPressDuration`, `allowableMovement`), `UIPanGestureRecognizer`, `UISwipeGestureRecognizer` (`direction`), `UIPinchGestureRecognizer`, `UIRotationGestureRecognizer`, custom `UIGestureRecognizer` subclasses, and raw `touchesBegan/Moved/Ended/Cancelled`;
- control events: `UIControl.Event` cases such as `.touchUpInside`, `.touchDown`, `.valueChanged`, plus target-action on custom controls;
- the exact action at every phase (`began` / `changed` / `ended` / `cancelled`), including state rollback when a gesture fails or is cancelled;
- dependencies and competition: `requireGestureRecognizer(toFail:)`, `gestureRecognizer(_:shouldRecognizeSimultaneouslyWith:)`, `gestureRecognizerShouldBegin`, `cancelsTouchesInView`, `delaysTouchesBegan` / `delaysTouchesEnded`, parent/child and scroll-view interaction, and hit-test overrides;
- thresholds and derived values: distance, velocity, direction, scale, rotation, plus haptic feedback and analytics triggered by the gesture.

Map to native SwiftUI gestures:
- `.onTapGesture(count:)`, `.onLongPressGesture(minimumDuration:maximumDistance:perform:onPressingChanged:)`, `DragGesture(minimumDistance:)`, `MagnifyGesture`, `RotateGesture`, `SpatialTapGesture`, `.gesture` / `.highPriorityGesture` / `.simultaneousGesture`, with explicit `.onChanged` / `.onEnded` state handling;
- reproduce custom hit areas with `.contentShape(...)` and `allowsHitTesting` when the legacy code used an oversized tappable region or a custom `hitTest`;
- if a native gesture cannot reproduce a custom recognizer exactly, document the concrete gap and propose a narrowly scoped bridge under the Hard rules. Do not ship a behavioral difference without explicit user approval.

**Verification is mandatory:** exercise every gesture path on device or simulator, including multi-touch, rapid repeated taps, long-press cancellation, drag interrupted by scrolling, combined pinch/rotate, and background/foreground during an active gesture. Record results in `migration/06-validation-report.md`. Do not mark a slice complete if any gesture path differs from the baseline.


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

Entry condition: the grill-me pre-flight gate is CLEARED. Use
`migration/00-preflight-interrogation.md` as the agreed input for scope and
constraints.

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

### Phase -1 — Pre-flight interrogation (grill-me gate)

Run the interrogation gate defined above and produce
`migration/00-preflight-interrogation.md`. Do not enter Phase 0 or Batch 0 until
the gate is CLEARED.

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
- target-action, delegate/data source, notifications, KVO, timers;
- gestures: recognizer type, configuration, event phases, thresholds, dependencies and cancellation (see the "Layout and gesture parity constraints" section);
- hard-coded `frame` / `bounds` / `center` assignments, `layoutSubviews` math, and other manual geometry;
- RAC / ReactiveObjC chains and command lifecycles (map their behavior to native state and Swift Concurrency; never port the reactive framework — see the "Reactive technology constraint" section);
- networking, persistence, caches, analytics, permissions, file access;
- navigation and presentation;
- threading and cancellation;
- error, empty, loading, retry, and offline states.

Build a behavior matrix:

| Legacy element | Current responsibility | SwiftUI destination | State / event | Verification |
|---|---|---|---|---|

Do not mechanically convert `viewDidLoad` into `onAppear`. Identify whether work is one-time initialization, view visibility work, state reaction, task, or resource lifecycle.

Include a separate gesture matrix covering every recognizer/control event and its full interaction semantics, and record the layout intent behind every hard-coded frame. Do not reduce a gesture to "tap -> action" if the original code has phases, thresholds, recognizer dependencies, or cancellation behavior.

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
- minimum OS compatibility strategy;
- reactive technology choice by deployment target, and any exception justification;
- how each hard-coded legacy frame is expressed as native SwiftUI layout;
- gesture mapping, including trigger conditions, event phases, interaction priorities and cancellation.

Default architecture:
- `Feature/Views`: small composable SwiftUI views;
- `Feature/ViewModels` or `Feature/State`: presentation state and user intents;
- `Domain`: business models and use cases where justified;
- `Data`: API/repository implementations;
- `Navigation`: typed routes and presentation coordination;
- `DesignSystem`: reusable tokens and components.

Use the simplest architecture that fits the existing app. Do not create a ViewModel for every trivial view. Keep business logic out of `body`. Apply the "Reactive technology constraint" section: prefer `@Observable` / `@State` / `@Environment` / `@Bindable` on iOS 17+, use `ObservableObject` / `@Published` / `@StateObject` on lower deployment targets, use Swift Concurrency for async work, and do not introduce RxSwift / RAC by default. If a third-party reactive dependency is proposed, record the concrete justification and approval in `migration/04-swiftui-design.md` before implementation.

Deliver: `migration/04-swiftui-design.md`.

### Phase 5 — Implement in vertical slices

For each screen/feature:
1. Create Swift models and service interfaces.
2. Port business rules and data handling.
3. Implement state transitions and async tasks with the native stack (no RxSwift by default).
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
- **Layout:** hierarchy, alignment, sizing, scrolling, safe areas, keyboard behavior, Dynamic Type and orientation are checked; no copied hard-coded frames remain without documented justification.
- **Gestures:** every mapped recognizer/control event is exercised with its original phases, thresholds, multi-touch behavior, failure/cancellation paths, and interaction with scrolling and other gestures.
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
├── 00-preflight-interrogation.md
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
5. Native reactive/state/concurrency stack used, by deployment target.
6. Third-party reactive dependencies, if any, with the approved exception and justification.
7. UIKit bridges, if any, with justification.
8. Hard-coded frame translations and any documented absolute-size exceptions.
9. Gesture parity verification results, including any differences and approvals.
10. Build/test commands and actual results.
11. Visual/functional differences still open.
12. Legacy files safe to remove vs. retained.
13. Next recommended slice.

## Safety and repository hygiene

- Inspect `git status` before editing; never overwrite unrelated user changes.
- Make focused changes; avoid broad formatting or unrelated refactors.
- Do not modify signing, provisioning, bundle identifiers, entitlements, production endpoints, secrets, or deployment target without approval.
- Do not delete legacy files or assets before explicit approval.
- If build/test execution is unavailable, state that validation is unverified.
