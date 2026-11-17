# objc-to-swiftui-migration

A Codex Skill package for migrating Objective-C + UIKit + XIB + Storyboard projects to native Swift + SwiftUI.

## Install

Copy this folder into your Codex skills directory, for example:

```text
~/.codex/skills/objc-to-swiftui-migration/
```

If your Codex installation uses a different skills discovery path, use that installation's documented path. Restart/reload Codex if required.

## Use

In a Codex session opened at the iOS repository, ask:

> Use objc-to-swiftui-migration to analyze this project. Do not modify source files yet. Inventory the project, analyze the selected screen's Objective-C, XIB and Storyboard relationships, and produce the migration reports.

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
