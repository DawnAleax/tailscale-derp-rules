import yaml

def load(p):
    try:
        return yaml.safe_load(open(p)) or {}
    except:
        return {}

old = load("old.yaml")
new = load("tailscale_derp.yaml")

def index(d):
    m = {}
    for r in d.get("Regions", {}).values():
        for n in r.get("Nodes", []):
            host = n.get("HostName")
            if host:
                m[host] = n
    return m

old_map = index(old)
new_map = index(new)

old_set = set(old_map)
new_set = set(new_map)

added = new_set - old_set
removed = old_set - new_set

changed = []
for h in old_set & new_set:
    if (old_map[h].get("IPv4"), old_map[h].get("IPv6")) != \
       (new_map[h].get("IPv4"), new_map[h].get("IPv6")):
        changed.append(h)

def fmt(keys, m):
    if not keys:
        return "- None"
    return "\n".join(
        f"- {k} | {m[k].get('IPv4')} | {m[k].get('IPv6')}"
        for k in sorted(keys)
    )

summary = {
    "added": len(added),
    "removed": len(removed),
    "changed": len(changed),
    "total": len(new_set),
}

with open("CHANGELOG.md", "w") as f:
    f.write("# DERP Update\n\n")
    f.write("## Summary\n")
    f.write(f"- Added: {summary['added']}\n")
    f.write(f"- Removed: {summary['removed']}\n")
    f.write(f"- IP Changed: {summary['changed']}\n")
    f.write(f"- Total: {summary['total']}\n\n")

    f.write("## Added\n" + fmt(added, new_map) + "\n\n")
    f.write("## Removed\n" + fmt(removed, old_map) + "\n\n")
    f.write("## IP Changed\n" + fmt(changed, new_map) + "\n")

with open("release_body.txt", "w") as f:
    f.write("DERP Update\n\n")
    f.write("## Summary\n")
    f.write(f"- Added: {summary['added']}\n")
    f.write(f"- Removed: {summary['removed']}\n")
    f.write(f"- IP Changed: {summary['changed']}\n")
    f.write(f"- Total: {summary['total']}\n")
