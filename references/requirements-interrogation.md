# Pre-flight requirements interrogation (grill-me gate)

This reference defines the mandatory interrogation that must happen **before** any
analysis deliverable or source edit. It adapts the `grill-me` method — relentless,
branch-by-branch interviewing — to the specific decisions of an Objective-C /
UIKit to native SwiftUI migration.

Core purpose: eliminate "blind start" failures. A migration is expensive to redo.
Ambiguity about scope, deployment target, reactive stack, parity standard, or
gesture semantics must be resolved up front, not discovered halfway through a slice.

## Non-negotiable method

1. **One question at a time.** For every question:
   1. Give your recommended answer first, with a one-line reason.
   2. Ask the question.
   3. Wait for the user's response before moving to the next question.
2. **Do not ask what you can find yourself.** If the answer is discoverable from
   the repository — source files, Xcode project settings, `Info.plist`, existing
   docs, or a Read/Grep of the code — answer it yourself and state the evidence.
   Only ask the user about intent, priority, constraint, or trade-off.
3. **List the decision branches first.** Open the session by naming the 3–6
   top-level branches you see (from the catalog below), then start with the most
   foundational one. Later branches usually depend on earlier ones.
4. **Walk each branch to completion** before moving on. Inside a branch, resolve
   sub-decisions in dependency order.
5. **An "it depends" answer is not resolved.** Reduce it to the condition that
   decides it, resolve that condition, then return to the original question.
   Do not carry an open "it depends" into Batch 0.
6. **No files are edited during interrogation.** The only permitted output is the
   interrogation record (see "Record and handoff" below), written after the
   session concludes.
7. **The session ends** only when every branch is resolved and no open
   "it depends" remains. Close with a one-paragraph summary of the key decisions.

## Decision branch catalog

Use this as a checklist, not a rigid script. Skip any question already answered by
repository evidence or by an earlier answer, and say that you are skipping it.

### Branch A — Scope and objective (start here; other branches depend on it)

- A1. Which screens/features are in scope, and which are explicitly out of scope?
  - Recommended answer: the smallest representative screen first; name everything else as out.
  - Self-check from repo: source tree, storyboard/XIB list, existing `migration/` reports.
  - Resolved when: an explicit in-scope list and an explicit out-of-scope list exist.
- A2. What is the first vertical slice, and why that one?
  - Recommended answer: one screen with the fewest shared dependencies; lowest-risk, representative.
  - Resolved when: one named slice plus a low-risk rationale is agreed.
- A3. What does "done" mean for this slice?
  - Recommended answer: build passes, behavior + gesture matrix green, baseline compared, legacy untouched.
  - Resolved when: measurable acceptance criteria are written down.
- A4. What is the legacy implementation's fate after cutover?
  - Recommended answer: keep it during migration; remove only after parity plus explicit approval (Hard rule 10).
  - Resolved when: the user states keep / switch-then-remove-later / remove-now; removal always needs separate approval.

### Branch B — Platform baseline

- B1. What is the actual minimum deployment target?
  - Self-check: project file, `Info.plist`, `PROJECT`/`TARGET` build settings. Do not guess and do not raise it just to use `@Observable`.
  - Resolved when: a concrete iOS version is confirmed and the state stack is derived from it.
- B2. Which form factors, orientations and size classes must be supported (iPhone only? iPad? split view? landscape)?
  - Resolved when: a device/orientation matrix is stated.
- B3. Are Dynamic Type, VoiceOver, localization/RTL, and dark mode required?
  - Resolved when: each is marked required or not-required; parity checks are scoped accordingly.
- B4. Which project settings are strictly off-limits (signing, bundle id, endpoints, deployment target, dependencies)?
  - Recommended answer: all of them are off-limits unless explicitly added to an approved batch.
  - Resolved when: the user confirms the off-limits list.

### Branch C — State, reactive technology and concurrency

- C1. Confirm the state stack implied by B1: `@Observable`/`@State`/`@Bindable` on iOS 17+,
  or `ObservableObject`/`@Published`/`@StateObject` below that.
  - Resolved when: the stack is chosen from the real deployment target, not preference.
- C2. How is the legacy RAC / ReactiveObjC / RxSwift usage to be treated?
  - Recommended answer: do not port the framework; map each chain to native state + Swift Concurrency per the reactive constraint section.
  - Resolved when: the user accepts the native mapping, or supplies a concrete exception case.
- C3. Any async work that genuinely cannot be expressed with Swift Concurrency?
  - If yes, this is a candidate for the documented exception — record the concrete requirement before proposing a dependency.
  - Resolved when: either no exception is needed, or the exception justification and approval path are agreed.

### Branch D — Visual, layout and gesture parity

- D1. What is the parity standard: pixel-perfect match to captured baselines, or faithful design intent at multiple sizes?
  - Recommended answer: design intent at multiple sizes/orientations/Dynamic Type; pixel comparison at the captured baseline state.
  - Resolved when: the standard is stated and baseline screenshots exist or the user agrees to provide them.
- D2. How are hard-coded Objective-C frames to be handled?
  - Recommended answer: translate the layout intent into native containers; never copy coordinates (Hard rule 14).
  - Resolved when: the user confirms no coordinate-copying; any genuine absolute-size exceptions are flagged for documentation.
- D3. Is any legacy gesture interaction too subtle to infer from code (custom hit area, multi-touch, recognizer dependency, cancellation)?
  - Recommended answer: build the full gesture matrix and verify every path on device/simulator (Hard rule 15).
  - Resolved when: gesture paths are enumerated and the verification environment is available.
- D4. Which navigation and presentation model must be reproduced (routes, deep links, modal stack, tab structure)?
  - Resolved when: the navigation map is agreed and typed routes are planned if appropriate.

### Branch E — Dependencies and shared infrastructure

- E1. Does the first slice depend on shared components, networking, persistence or analytics that are outside the slice?
  - Recommended answer: migrate the minimum needed for the slice; leave shared components for a separately approved batch.
  - Resolved when: the dependency boundary is drawn and any out-of-scope dependencies are named.
- E2. Are any new third-party dependencies acceptable?
  - Recommended answer: none; native stack first. Any addition follows the documented exception + explicit approval.
  - Resolved when: the dependency stance is confirmed.

### Branch F — Validation and delivery cadence

- F1. What build/test commands are available, and will the user run device/simulator verification?
  - Self-check: scheme, test targets, `xcodebuild` availability.
  - Resolved when: the concrete validation commands and who runs them are stated.
- F2. Where should reports and the ledger live (default: `migration/`)?
  - Resolved when: the output path is confirmed.
- F3. Confirm the approval cadence: one slice at a time, STOP after each, explicit approval required for the next.
  - Recommended answer: yes — this is a Hard rule and not negotiable.
  - Resolved when: the user acknowledges the per-batch gate.

## Record and handoff

After all branches are resolved, write `migration/00-preflight-interrogation.md`
using `templates/00-preflight-interrogation.md`, then:

1. Present the one-paragraph decision summary.
2. State that the interrogation gate is **CLEARED**.
3. Only then proceed to Batch 0 / Phase 0 analysis — and never in the same turn as
   the questions themselves.

If the user declines to answer a blocking question, the gate stays **OPEN**: do
not produce analysis deliverables or edit source. State exactly which branch is
blocked and why it blocks safe implementation.

## Anti-patterns this gate exists to prevent

- Assuming the deployment target, reactive stack, or scope instead of confirming it.
- Starting to "explore and see what needs changing" before the scope branch is resolved.
- Treating silence or a vague "sounds fine" as a resolved answer.
- Asking the user for facts that are sitting in the project file or source code.
- Dumping all questions at once instead of walking one branch at a time.
