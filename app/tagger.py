def tag_text(text: str) -> str:
    lines = text.split("\n")
    tagged_lines = []

    for line in lines:
        line = line.strip()

        if line.lower().startswith("q"):
            tagged_lines.append(f"#Q {line}")
        elif line.startswith("("):
            tagged_lines.append(f"#OPT {line}")
        elif "=" in line or "^" in line:
            tagged_lines.append(f"#EQ {line}")
        else:
            tagged_lines.append(line)

    return "\n".join(tagged_lines)
