#!/usr/bin/env python3
"""Extract a structural report from XIB / Storyboard XML. Read-only."""
import argparse, json, re
from pathlib import Path
import xml.etree.ElementTree as ET

def clean_tag(tag):
    return tag.split("}")[-1]

def attrs(el):
    return {k: v for k, v in el.attrib.items()}

def descendants(el, tag):
    return [x for x in el.iter() if clean_tag(x.tag) == tag]

def object_record(el, parent_id=None):
    tag = clean_tag(el.tag)
    a = attrs(el)
    oid = a.get("id")
    record = {
        "id": oid, "xml_tag": tag, "class": a.get("customClass") or a.get("class"),
        "module": a.get("customModule"), "reuse_identifier": a.get("reuseIdentifier"),
        "storyboard_identifier": a.get("storyboardIdentifier"),
        "parent_id": parent_id, "attributes": a, "children": [], "constraints": [],
        "connections": [], "resources": []
    }
    for child in list(el):
        ctag = clean_tag(child.tag)
        if ctag in {"subviews", "viewControllers", "tableViewCells", "collectionViewCells", "objects"}:
            for nested in list(child):
                if clean_tag(nested.tag) not in {"placeholder"}:
                    record["children"].append(object_record(nested, oid))
        elif ctag == "constraints":
            for c in list(child):
                if clean_tag(c.tag) == "constraint":
                    record["constraints"].append(attrs(c))
        elif ctag == "connections":
            for c in list(child):
                record["connections"].append({"kind": clean_tag(c.tag), **attrs(c)})
        elif ctag == "resources":
            for r in list(child):
                record["resources"].append({"kind": clean_tag(r.tag), **attrs(r)})
    return record

def flatten(nodes):
    for n in nodes:
        yield n
        yield from flatten(n.get("children", []))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("file")
    p.add_argument("--out", default="migration/ib")
    args = p.parse_args()
    path = Path(args.file)
    root = ET.parse(path).getroot()
    root_attrs = attrs(root)
    # XIBs commonly have a root-level <objects>; Storyboards place an <objects>
    # collection inside each <scene>. Preserve scene boundaries instead of
    # treating the storyboard as a single flat object list.
    scene_records = []
    scenes_el = next((x for x in list(root) if clean_tag(x.tag) == "scenes"), None)
    if scenes_el is not None:
        for scene in list(scenes_el):
            scene_objects = next((x for x in list(scene) if clean_tag(x.tag) == "objects"), None)
            scene_nodes = []
            if scene_objects is not None:
                for child in list(scene_objects):
                    if clean_tag(child.tag) != "placeholder":
                        scene_nodes.append(object_record(child))
            scene_records.append({"scene_attributes": attrs(scene), "objects": scene_nodes})
        nodes = [n for scene in scene_records for n in scene["objects"]]
    else:
        objects_el = next((x for x in list(root) if clean_tag(x.tag) == "objects"), None)
        nodes = []
        if objects_el is not None:
            for child in list(objects_el):
                if clean_tag(child.tag) != "placeholder":
                    nodes.append(object_record(child))
    all_nodes = list(flatten(nodes))
    constraints = []
    connections = []
    for n in all_nodes:
        for c in n["constraints"]:
            constraints.append({"owner_id": n["id"], **c})
        for c in n["connections"]:
            connections.append({"owner_id": n["id"], **c})
    result = {
        "file": str(path),
        "document": root_attrs,
        "top_level_objects": nodes,
        "scenes": scene_records,
        "object_count": len(all_nodes),
        "constraints": constraints,
        "connections": connections,
        "object_index": {n["id"]: {"class": n["class"], "xml_tag": n["xml_tag"],
                                  "parent_id": n["parent_id"]} for n in all_nodes if n["id"]},
        "limitations": [
            "This is a structural XML extractor, not a full Interface Builder or Auto Layout solver.",
            "Some nested object relationships, layout guides, variations, size classes, trait collections and document-specific constructs may require manual inspection.",
            "It cannot detect runtime-created views, code-activated constraints, custom drawing, or actual intrinsic content sizes.",
            "Verify extracted hierarchy and connections against Xcode and the Objective-C source before implementation."
        ]
    }
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / (path.stem + ".json")
    dest.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Objects: {len(all_nodes)}; constraints: {len(constraints)}; connections: {len(connections)}")
    print(f"Wrote {dest}")

if __name__ == "__main__":
    main()
