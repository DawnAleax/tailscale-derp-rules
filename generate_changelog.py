import yaml

def load(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except:
        return {}

old = load("old.yaml")
new = load("tailscale_derp.yaml")


# ----------------------------
# 规则标准化：把 DERP 转成 set
# ----------------------------
def normalize_rules(data):
    """
    输出格式：
    {
        ("DOMAIN", "xxx.com", None),
        ("IP-CIDR", "1.1.1.1/32", None),
        ("IP-CIDR6", "xxxx", None)
    }
    """
    s = set()

    payload = data.get("payload", [])
    if not isinstance(payload, list):
        return s

    for r in payload:
        if not isinstance(r, str):
            continue

        parts = r.split(",")

        if len(parts) == 2:
            t, v = parts
            s.add((t.strip(), v.strip(), None))

        elif len(parts) == 3:
            t, v1, v2 = parts
            s.add((t.strip(), v1.strip(), v2.strip()))

    return s


old_s = normalize_rules(old)
new_s = normalize_rules(new)


# ----------------------------
# diff 计算
# ----------------------------
added = new_s - old_s
removed = old_s - new_s
common = old_s & new_s


# ----------------------------
# 变化检测（规则内容变化）
# ----------------------------
changed = []
for rule in common:
    if rule not in new_s:
        changed.append(rule)


# ----------------------------
# 分类统计
# ----------------------------
def classify(rules):
    d = {"DOMAIN": 0, "IP-CIDR": 0, "IP-CIDR6": 0}
    for t, _, _ in rules:
        if t in d:
            d[t] += 1
    return d


added_stat = classify(added)
removed_stat = classify(removed)
changed_stat = classify(changed)


# ----------------------------
# 输出格式化
# ----------------------------
def fmt(title, rules):
    if not rules:
        return f"## {title}\n- None\n"

    lines = [f"## {title}"]
    for t, v1, v2 in sorted(rules):
        if v2:
            lines.append(f"- {t} {v1} -> {v2}")
        else:
            lines.append(f"- {t} {v1}")
    return "\n".join(lines) + "\n"


total = len(new_s)
net = len(added) - len(removed)


# ----------------------------
# CHANGELOG.md
# ----------------------------
with open("CHANGELOG.md", "w", encoding="utf-8") as f:
    f.write("# DERP Update Report\n\n")

    f.write("## Summary\n")
    f.write(f"- Added: {len(added)} (DOMAIN {added_stat['DOMAIN']}, IP {added_stat['IP-CIDR']}, IPv6 {added_stat['IP-CIDR6']})\n")
    f.write(f"- Removed: {len(removed)} (DOMAIN {removed_stat['DOMAIN']}, IP {removed_stat['IP-CIDR']}, IPv6 {removed_stat['IP-CIDR6']})\n")
    f.write(f"- Changed: {len(changed)}\n")
    f.write(f"- Total rules: {total}\n")
    f.write(f"- Net change: {net:+d}\n\n")

    f.write(fmt("Added", added))
    f.write("\n")
    f.write(fmt("Removed", removed))
    f.write("\n")
    f.write(fmt("Changed", changed))


# ----------------------------
# release_body.txt（GitHub Release用）
# ----------------------------
with open("release_body.txt", "w", encoding="utf-8") as f:
    f.write("DERP Update\n\n")

    f.write("## Summary\n")
    f.write(f"- Added: {len(added)}\n")
    f.write(f"- Removed: {len(removed)}\n")
    f.write(f"- Changed: {len(changed)}\n")
    f.write(f"- Total rules: {total}\n")
    f.write(f"- Net change: {net:+d}\n\n")

    if len(added) or len(removed) or len(changed):
        f.write("## Detail\n\n")
        f.write(fmt("Added", added))
        f.write("\n")
        f.write(fmt("Removed", removed))
        f.write("\n")
        f.write(fmt("Changed", changed))
    else:
        f.write("No changes detected.\n")


print("done")
