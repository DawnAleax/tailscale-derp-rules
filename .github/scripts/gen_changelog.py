import yaml

def load(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except:
        return {}

old = load("old.yaml")
new = load("tailscale_derp.yaml")

def extract(d):
    m = {}
    for r in d.get("Regions", {}).values():
        for n in r.get("Nodes", []):
            m[n["HostName"]] = {
                "ipv4": n.get("IPv4"),
                "ipv6": n.get("IPv6")
            }
    return m

old_map = extract(old)
new_map = extract(new)

added = []
removed = []
updated = []

for k in new_map:
    if k not in old_map:
        added.append((k, new_map[k]["ipv4"], new_map[k]["ipv6"]))
    else:
        if new_map[k] != old_map[k]:
            updated.append((k, old_map[k], new_map[k]))

for k in old_map:
    if k not in new_map:
        removed.append((k, old_map[k]["ipv4"], old_map[k]["ipv6"]))

def fmt_added(items):
    return "\n".join([f"- {a} | {b} | {c}" for a,b,c in items]) or "- None"

def fmt_removed(items):
    return "\n".join([f"- {a} | {b} | {c}" for a,b,c in items]) or "- None"

def fmt_updated(items):
    if not items:
        return "- None"
    out = []
    for host, oldv, newv in items:
        out.append(
            f"- {host} | {oldv['ipv4']}→{newv['ipv4']} | {oldv['ipv6']}→{newv['ipv6']}"
        )
    return "\n".join(out)

summary = {
    "added": len(added),
    "removed": len(removed),
    "updated": len(updated),
    "total": len(new_map)
}

with open("CHANGELOG.md", "w", encoding="utf-8") as f:
    f.write("# DERP Change Log\n\n")

    f.write("## 📊 Summary\n")
    f.write(f"- Added: {summary['added']}\n")
    f.write(f"- Removed: {summary['removed']}\n")
    f.write(f"- Updated: {summary['updated']}\n")
    f.write(f"- Total nodes: {summary['total']}\n\n")

    f.write("## ➕ Added\n")
    f.write(fmt_added(added))
    f.write("\n\n")

    f.write("## ➖ Removed\n")
    f.write(fmt_removed(removed))
    f.write("\n\n")

    f.write("## 🔁 Updated (IP changed)\n")
    f.write(fmt_updated(updated))
    f.write("\n")
