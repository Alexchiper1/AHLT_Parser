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
            left = left.strip()
            right = right.split()
            if left not in rules:
                rules[left] = []

            rules[left].append(right)

def parse(symbol, position, words, tags):
    if symbol not in rules:
        if position < len(tags) and tags[position] == symbol:
            return [symbol, words[position]], position + 1
        return None

    for rule in rules[symbol]:
        children = []
        current = position
        valid = True
        for part in rule:
            result = parse(part, current, words, tags)
            if result is None:
                valid = False
                break
            node, current = result
            children.append(node)
        if valid:
            return [symbol] + children, current
    return None


def brackets(node):
    if len(node) == 2 and isinstance(node[1], str):
        return "[" + node[0] + " " + node[1] + "]"
    result = "[" + node[0]

    for child in node[1:]:
        result += " " + brackets(child)
    return result + "]"

def tree(node, indent=""):
    print(indent + node[0])
    for child in node[1:]:
        if isinstance(child, list):
            tree(child, indent + "    ")
        else:
            print(indent + "    " + child)

sentence = input("Enter sentence: ")
words = sentence.lower().split()
tags = []

valid_words = True

for word in words:
    if word not in lexicon:
        print("Unknown word:", word)
        valid_words = False
        break
    tags.append(lexicon[word])

if valid_words:
    print("\nWords:")
    print(words)
    print("\nPOS:")
    print(tags)

    result = parse("S", 0, words, tags)

    if result is not None:
        parsed_tree, end = result
        if end == len(words):
            print("ACCEPTED")
            print("Bracketed structure:")
            print(brackets(parsed_tree))
            print("Parse tree:")
            tree(parsed_tree)
        else:
            print("REJECTED")
    else:
        print("REJECTED")