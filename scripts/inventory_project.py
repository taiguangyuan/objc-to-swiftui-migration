#!/usr/bin/env python3
"""Create a lightweight inventory of an iOS project. No project files are modified."""
import argparse, json
from pathlib import Path

SOURCE_EXTS = {".h", ".m", ".mm", ".c", ".cc", ".cpp", ".swift"}
IB_EXTS = {".xib", ".storyboard"}
RESOURCE_EXTS = {".xcassets", ".imageset", ".colorset", ".xcconfig", ".plist"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("root", help="Project or repository directory")
    p.add_argument("--out", default="migration/inventory")
    args = p.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.out).resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")
    out.mkdir(parents=True, exist_ok=True)

    sources, ib, projects, resources = [], [], [], []
    excluded = {".git", "Pods", "Carthage", "DerivedData", "build", ".build"}
    for path in root.rglob("*"):
        if any(part in excluded for part in path.parts):
            continue
        if not path.is_file():
            if path.name.endswith(".xcassets") or path.name.endswith(".imageset") or path.name.endswith(".colorset"):
                resources.append(str(path.relative_to(root)))
            continue
        rel = str(path.relative_to(root))
        if path.suffix.lower() in SOURCE_EXTS:
            sources.append(rel)
        elif path.suffix.lower() in IB_EXTS:
            ib.append(rel)
        elif path.name.endswith((".xcodeproj", ".xcworkspace")):
            projects.append(rel)
        elif path.suffix.lower() in {".plist", ".xcconfig"}:
            resources.append(rel)

    result = {
        "root": str(root),
        "source_files": sorted(sources),
        "interface_builder_files": sorted(ib),
        "project_files": sorted(projects),
        "configuration_and_resources": sorted(resources),
        "counts": {"source": len(sources), "interface_builder": len(ib),
                   "projects": len(projects), "configuration_and_resources": len(resources)},
        "limitations": [
            "This is a filesystem inventory, not a complete Xcode project graph.",
            "It does not resolve target membership, build phases, Swift/Objective-C symbols, or runtime-created views.",
            "Pods, Carthage, DerivedData, .git and build output are excluded by default."
        ]
    }
    (out / "project-inventory.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    lines = [f"# Project inventory: {root}", "", "## Counts",
             *[f"- {k}: {v}" for k, v in result["counts"].items()], "",
             "## Interface Builder files", *[f"- `{x}`" for x in sorted(ib)], "",
             "## Source files", *[f"- `{x}`" for x in sorted(sources)], "",
             "## Projects / workspaces", *[f"- `{x}`" for x in sorted(projects)], "",
             "## Notes", *[f"- {x}" for x in result["limitations"]]]
    (out / "project-inventory.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote inventory to {out}")

if __name__ == "__main__":
    main()
