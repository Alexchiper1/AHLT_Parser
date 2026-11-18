lexicon = {}

with open("lexicon.txt") as file:
    for line in file:
        if not line.strip():
            continue

        word, pos, root, num = [x.strip() for x in line.split(",")]

        if num == "singular":
            pos += "_SG"
        elif num == "plural":
            pos += "_PL"

        lexicon[word.lower()] = pos

rules = {}

with open("rules.txt") as file:
    for line in file:
        if "->" in line:
            left, right = line.split("->")
            rules.setdefault(left.strip(), []).append(right.split())
