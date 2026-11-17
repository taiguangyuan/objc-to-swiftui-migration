# Cross-tool compatibility: Codex and TRAE

This package uses the portable Agent Skills structure: a folder containing `SKILL.md`, optional Markdown references, scripts, and templates.

## Codex

Install the complete folder into the Skills directory supported by the installed Codex version, commonly:

```text
~/.codex/skills/objc-to-swiftui-migration/
```

## TRAE

Two supported approaches:

### Import ZIP

Use TRAE Settings → Skills & Commands → Skills → Create / Import local Skill, then upload the ZIP containing this folder. Confirm the imported Skill is enabled.

### Project-local installation

Place the folder at:

```text
YourProject/.trae/skills/objc-to-swiftui-migration/
```

TRAE documentation also describes `.agents/skills/` as an interoperable Agent Skills directory. Enable that directory in TRAE settings before relying on discovery:

```text
YourProject/.agents/skills/objc-to-swiftui-migration/
```

For TRAE CN, the documented global path is commonly:

```text
~/.trae-cn/skills/objc-to-swiftui-migration/
```

For international TRAE builds, use the global path documented by that installed build or import through the UI. Paths can vary by product edition and version.

## Portability boundaries

Portable:
- `SKILL.md` YAML frontmatter and Markdown instructions;
- Markdown files in `references/`;
- templates and sample reports;
- standard Python scripts using the Python standard library.

Environment-dependent:
- whether the IDE automatically discovers a folder or requires import/refresh;
- terminal and filesystem permissions;
- Python availability and invocation path;
- Xcode installation, simulator availability, and `xcodebuild`;
- screenshot capture and visual-diff tools;
- agent context retention and how reliably it pauses for approval.

The Skill's approval gate is an instruction-level workflow, not a cryptographic or operating-system permission boundary. For stronger protection, use Git commits/branches, review diffs, restrict write permissions where practical, and do not grant unattended execution permissions for destructive commands.

## Recommended shared project layout

```text
YouriOSProject/
├── .agents/
│   └── skills/
│       └── objc-to-swiftui-migration/
│           ├── SKILL.md
│           ├── references/
│           ├── scripts/
│           └── templates/
└── migration/
```

Use one canonical copy in the repository. Avoid maintaining independent Codex and TRAE copies that can drift. If a tool requires a different installation location, copy or import the same versioned package rather than editing its rules separately.
