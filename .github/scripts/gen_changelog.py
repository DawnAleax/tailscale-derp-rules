import yaml

def load(p):
    try:
        return yaml.safe_load(open(p)) or {}
    except:
        return {}

old = load("old.yaml")
new = load("tailscale_derp.yaml")

# =========================
# 只用 HostName 做主键（核心优化）
# =========================
def index(d):
    m = {}
    for r in d.get("Regions", {}).values():
        for n in r.get("Nodes", []):
            h = n.get("HostName")
            if h:
                m[h] = n
    return m

old_m = index(old)
new_m = index(new)

old_h = set(old_m)
new_h = set(new_m)

added = new_h - old_h
removed = old_h - new_h
common = old_h & new_h

changed = []
for h in common:
    o = old_m[h]
    n = new_m[h]
    if (o.get("IPv4"), o.get("IPv6")) != (n.get("IPv4"), n.get("IPv6")):
        changed.append(h)

def fmt(hosts, m):
    return "\n".join(
        f"- {h} | {m[h].get('IPv4')} | {m[h].get('IPv6')}"
        for h in sorted(hosts)
    ) or "- None"

summary = {
    "added": len(added),
    "removed": len(removed),
    "changed": len(changed),
    "total": len(new_h),
}

with open("CHANGELOG.md", "w") as f:
    f.write("# DERP Update\n\n")
    f.write("## Summary\n")
    f.write(f"- Added: {summary['added']}\n")
    f.write(f"- Removed: {summary['removed']}\n")
    f.write(f"- IP Changed: {summary['changed']}\n")
    f.write(f"- Total: {summary['total']}\n\n")

    f.write("## Added\n")
    f.write(fmt(added, new_m) + "\n\n")

    f.write("## Removed\n")
    f.write(fmt(removed, old_m) + "\n\n")

    f.write("## IP Changed\n")
    f.write(fmt(changed, new_m) + "\n")

with open("release_body.txt", "w") as f:
    f.write("DERP Update\n\n")
    f.write("## Summary\n")
    f.write(f"- Added: {summary['added']}\n")
    f.write(f"- Removed: {summary['removed']}\n")
    f.write(f"- IP Changed: {summary['changed']}\n")
    f.write(f"- Total: {summary['total']}\n")
