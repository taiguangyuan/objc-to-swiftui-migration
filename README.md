# objc-to-swiftui-migration

A WorkBuddy / Codex / TRAE compatible Skill package for migrating Objective-C + UIKit + XIB + Storyboard projects to native Swift + SwiftUI.

## Install

Copy this folder into your Codex skills directory, for example:

```text
~/.codex/skills/objc-to-swiftui-migration/
```

If your Codex installation uses a different skills discovery path, use that installation's documented path. Restart/reload Codex if required.

## Use

In a Codex session opened at the iOS repository, ask:

> Use objc-to-swiftui-migration. Start with the pre-flight requirements interrogation: ask me one question at a time about scope, deployment target and parity, and do not analyze or modify source files until the gate is CLEARED. Then inventory the project and produce the migration reports.

Then migrate one vertical slice at a time:

> Continue with the Login feature. Implement the native SwiftUI version according to the approved analysis. Do not remove the legacy implementation. Build and test it, then update the validation report.

## Scripts

```bash
python3 scripts/inventory_project.py /path/to/repository --out migration/inventory
python3 scripts/parse_interface_builder.py /path/to/View.xib --out migration/ib
python3 scripts/parse_interface_builder.py /path/to/Main.storyboard --out migration/ib
```

Scripts are read-only and use Python's standard library. Their output must be verified against Xcode and source code; they are not complete semantic parsers.

## Important

This Skill provides workflow rules and lightweight analysis scripts. It does not guarantee automatic full-project migration. Build, simulator, visual comparison and behavioral verification still require the actual project, Xcode toolchain, test fixtures and review.

**Reactive constraint:** RxSwift / RAC and other third-party reactive frameworks are not introduced by default. Use Apple's native observation, state and concurrency stack (`@Observable` / `@State` / `@Environment` / `@Bindable` on iOS 17+, `ObservableObject` / `@Published` / `@StateObject` below iOS 17, Swift Concurrency for async work). Third-party reactive dependencies require documented justification and user approval. See the "Reactive technology constraint" section in `SKILL.md`.

**Layout and gesture constraints:** Hard-coded Objective-C `frame` coordinates are never copied into SwiftUI — translate the layout intent into native containers and modifiers. Gestures must preserve the original operation logic exactly (event phases, thresholds, cancellation, interaction with other gestures) and be verified on device/simulator before completion. See "Layout and gesture parity constraints" in `SKILL.md`.


## Pre-flight requirements interrogation (grill-me gate)

Before any analysis or code edit, the Skill runs a mandatory interrogation to
prevent a blind start:

1. List the decision branches: scope, platform baseline, reactive/state stack, parity, dependencies, delivery cadence.
2. Ask one question at a time, giving a recommended answer first; stop and wait for each response.
3. Self-answer from the repository whatever can be discovered there; ask only about intent, priority and trade-offs.
4. Resolve every branch and every "it depends"; record the decisions in `migration/00-preflight-interrogation.md`.
5. Declare the gate CLEARED — only then may Batch 0 begin. A blocked gate means no analysis deliverables and no source edits.

This avoids assuming the deployment target, reactive stack or scope and then
having to redo a slice. See `references/requirements-interrogation.md` for the
full question catalog.

## Incremental approval gate

The Skill now enforces one small migration batch at a time:
1. Analyze first; no source edits.
2. Propose the first slice and exact file allowlist.
3. Wait for approval.
4. Implement only that slice.
5. Build, test, inspect the diff and report.
6. Stop and wait for explicit approval before the next slice.

Approval of one batch does not authorize later batches. See the mandatory rules in `SKILL.md`.

## Use in TRAE

TRAE supports the `SKILL.md` Agent Skills format. You can import the ZIP from Settings → Skills & Commands, or install the folder in `.trae/skills/` / an enabled `.agents/skills/` directory. See `CROSS-TOOL-COMPATIBILITY.md` for details and environment caveats.

## Upload to the WorkBuddy developer platform

`SKILL.md` frontmatter includes the fields required by the WorkBuddy skill upload validator: `name`, `version`, `display_name`, `display_name_en`, `description`, `description_zh`, and `description_en`. Zip the folder with `SKILL.md` at the package root (the archive should contain `objc-to-swiftui-migration/SKILL.md`), and exclude local artifacts such as `.DS_Store`, `__pycache__`, and `.workbuddy/` from the archive.
