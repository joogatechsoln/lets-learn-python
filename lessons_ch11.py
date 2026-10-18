"""Chapter 11: Sets (16 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Sets")
    A = "{\"<<n1>>\", \"<<n2>>\", \"<<n3>>\"}"
    B = "{\"<<n3>>\", \"<<n4>>\"}"
    SETS = "shelf_a = " + A + "\nshelf_b = " + B + "\n"
    PR = "print(sorted(%s))\n"

    c.add("intro_sets", "Introduction to Sets", "Sets", "hold unique values in a set",
          [T("The scenario", "Two departments at <<biz>> each send a list of <<things>> that need attention, and many appear on both. You want each one **once**. A list would keep the repeats. A **set** cannot."),
           T("What a set is", "A **set** is a collection of **unique** values with **no order**, written in curly braces:\n\n```python\ntags = {\"a\", \"b\", \"a\"}\nprint(len(tags))        # 2, the repeat vanished\nprint(\"a\" in tags)      # True\n```\n\n- **Unique**: adding something already there changes nothing\n- **Unordered**: there is no first item and no position\n- **Fast** membership tests\n\nBecause the order is not guaranteed, always print `sorted(a_set)` when you want a stable output."),
           T("Mathematics, in code", "Sets follow school set theory: union, intersection, difference. This chapter teaches each, and they solve real problems like \"who is on both lists?\" and \"what is missing?\" in one line."),
           P('s = {3, 1, 3, 2}\nprint(len(s), sorted(s))', "3 [1, 2, 3]", ["4 [3, 1, 3, 2]", "3 {1, 2, 3}"], "The duplicate 3 disappears, leaving three items. sorted gives a list in order."),
           Q("What happens when you add a value that is already in a set?", ["Nothing changes", "The set gets two copies", "It raises an error"], 0, "Sets hold each value once.")],
          "Make a set `tags` from `\"<<n1>>\"`, `\"<<n2>>\"`, `\"<<n1>>\"`, `\"<<n3>>\"` (note the repeat). Print how many it has, the sorted contents, and whether `\"<<n2>>\"` is in it. It should print:\n\n<<OUT>>",
          "# tags = a set of the four values above (one is repeated)\n# print len(tags), sorted(tags), then \"<<n2>>\" in tags\n",
          'tags = {"<<n1>>", "<<n2>>", "<<n1>>", "<<n3>>"}\nprint(len(tags))\nprint(sorted(tags))\nprint("<<n2>>" in tags)\n',
          checks=[("prints", 3)], hints=["Curly braces with items and no colons make a set.", "Print sorted(tags) for a steady order."], emoji="🧺")

    c.add("creating_sets", "Creating Sets", "Creating", "create sets, including the empty set",
          [T("The scenario", "Sets come from many places: typed in, converted from a list, built from the letters of a code. There is one famous trap: the empty set."),
           T("Ways to create a set", "```python\na = {1, 2, 3}              # literal\nb = set([3, 1, 3])         # from a list: {1, 3}\nc = set(\"hello\")           # from text: {'h', 'e', 'l', 'o'}\nd = set()                  # the EMPTY set\ne = {}                     # NOT a set: an empty DICTIONARY\n```\n\nThe empty braces `{}` are already taken by dictionaries, so an empty set must be written `set()`."),
           P('print(type({}).__name__, type(set()).__name__)', "dict set", ["set set", "dict dict"], "{} is an empty dictionary. set() is the empty set."),
           Q("How do you write an empty set?", ["set()", "{}", "[]"], 0, "{} makes a dictionary. Use set() for an empty set.")],
          "Create four sets and print what the task asks. It should print:\n\n<<OUT>>\n\n- `from_list`: from the list `[3, 1, 3, 2, 1]`, printed sorted\n- `letters`: from the text `\"<<stag>>\"`, printed sorted\n- `empty`: an empty set, printed as its length\n- then print the type name of `{}` and the type name of `set()`",
          "# from_list, letters, empty; print sorted(from_list), sorted(letters), len(empty)\n# then the type names of {} and set()\n",
          'from_list = set([3, 1, 3, 2, 1])\nletters = set("<<stag>>")\nempty = set()\nprint(sorted(from_list))\nprint(sorted(letters))\nprint(len(empty))\nprint(type({}).__name__, type(set()).__name__)\n',
          checks=[("var", "from_list"), ("var", "letters")], hints=["set([...]) turns a list into a set.", "type(x).__name__ gives the name of the type."], emoji="🧱")

    c.add("set_uniqueness", "Set Uniqueness and Unordered Elements", "No order", "use sets to remove duplicates",
          [T("The scenario", "A log has many repeated counts and you need the **distinct** ones, how many there are, and, where it matters, in their original order. Sets are the quickest duplicate remover. You must know what they cost: the order."),
           T("Two facts", "```python\nraw = [3, 1, 3, 2, 1]\nprint(sorted(set(raw)))       # [1, 2, 3]  distinct, sorted\nprint(len(set(raw)))          # 3          how many distinct\n```\n\nSets are **unordered**: you cannot index them (`s[0]` is a TypeError), and the printing order of text items can change between runs. To remove duplicates **and keep the order**, use a dictionary trick:\n\n```python\nprint(list(dict.fromkeys(raw)))   # [3, 1, 2]\n```"),
           P("raw = [3, 1, 3, 2, 1]\nprint(list(dict.fromkeys(raw)))", "[3, 1, 2]", ["[1, 2, 3]", "[3, 1, 3, 2, 1]"], "dict keys are unique and keep first-seen order, so this removes repeats and keeps the order."),
           Q("Which can you do with a set?", ["Test membership", "Read item 0", "Sort it in place"], 0, "Sets have no positions, so no indexing and no .sort().")],
          "From `raw = [3, 1, 3, 2, 1, 3]` find: the sorted distinct values `unique_values`, how many distinct there are `how_many`, and the distinct values in first-seen order `ordered_unique`. Print the three. It should print:\n\n<<OUT>>",
          "raw = [3, 1, 3, 2, 1, 3]\n# unique_values (sorted), how_many, ordered_unique (use dict.fromkeys); print them\n",
          'raw = [3, 1, 3, 2, 1, 3]\nunique_values = sorted(set(raw))\nhow_many = len(set(raw))\nordered_unique = list(dict.fromkeys(raw))\nprint(unique_values)\nprint(how_many)\nprint(ordered_unique)\n',
          checks=[("var", "unique_values"), ("var", "how_many"), ("var", "ordered_unique")], hints=["sorted(set(raw)) gives a list.", "list(dict.fromkeys(raw)) keeps order."], emoji="🌀")

    c.add("set_adding", "Adding Elements to Sets", "Adding", "grow a set with add and update",
          [T("The scenario", "Names of <<things>> seen so far are collected as the <<system>> reads its files. Each new name goes in; a repeat should change nothing. Adding to a set is exactly that."),
           T("add and update", "```python\nseen = set()\nseen.add(\"a\")                 # one item\nseen.add(\"a\")                 # no change\nseen.update([\"b\", \"c\", \"c\"])   # many items from any iterable\n```\n\n`add` takes **one** item. `update` takes an **iterable** (a list, another set, a string) and adds each element. Neither raises an error for repeats."),
           P('s = {1}\ns.add(1)\ns.update([2, 2, 3])\nprint(sorted(s))', "[1, 2, 3]", ["[1, 1, 2, 2, 3]", "[1, [2, 2, 3]]"], "Repeats are ignored, leaving 1, 2 and 3."),
           Q("What is the difference between add and update?", ["add takes one item, update takes many", "They are the same", "update removes items"], 0, "add is for one value, update for a collection of values.")],
          "Start with `seen = set()`. Add `\"<<n1>>\"`, add `\"<<n2>>\"`, add `\"<<n1>>\"` again, then update with the list `[\"<<n3>>\", \"<<n4>>\", \"<<n4>>\"]`. Print how many items `seen` has and its sorted contents after each of the four changes. It should print:\n\n<<OUT>>",
          "seen = set()\n# four changes; after each print len(seen) and sorted(seen)\n",
          'seen = set()\nseen.add("<<n1>>")\nprint(len(seen), sorted(seen))\nseen.add("<<n2>>")\nprint(len(seen), sorted(seen))\nseen.add("<<n1>>")\nprint(len(seen), sorted(seen))\nseen.update(["<<n3>>", "<<n4>>", "<<n4>>"])\nprint(len(seen), sorted(seen))\n',
          checks=[("var", "seen")], hints=["The third change does not change the size.", "update takes a list."], emoji="➕")

    c.add("set_removing", "Removing Elements from Sets", "Removing", "remove items with remove, discard and pop",
          [T("The scenario", "Items are retired from the active list. Sometimes you know they are there, sometimes you are not sure. Sets give you both a strict and a forgiving way to remove."),
           T("Three ways", "```python\ns = {1, 2, 3}\ns.remove(2)       # KeyError if absent\ns.discard(9)      # silently does nothing if absent\nx = s.pop()       # removes and returns SOME item (no order!)\ns.clear()         # empties it\n```\n\nUse `discard` when it is fine for the item to be missing, and `remove` when a missing item means a bug. Because sets have no order, `pop` gives an **arbitrary** item: only rely on it for one-element sets or when you do not care which."),
           P('s = {1, 2, 3}\ns.discard(9)\ns.remove(2)\nprint(sorted(s))', "[1, 3]", ["[1, 2, 3]", "!KeyError"], "discard(9) does nothing, and remove(2) takes out the 2."),
           Q("Which raises KeyError if the item is missing?", ["remove", "discard", "add"], 0, "discard is the forgiving one.")],
          "Start with `active = {\"<<n1>>\", \"<<n2>>\", \"<<n3>>\", \"<<n4>>\"}`. Remove `\"<<n2>>\"`, discard `\"<<missing>>\"` (which is not there), and discard `\"<<n4>>\"`. Print the sorted `active`. Then make `last = {\"<<n1>>\"}`, pop it into `item`, and print `item` and the length of `last`. It should print:\n\n<<OUT>>",
          'active = {"<<n1>>", "<<n2>>", "<<n3>>", "<<n4>>"}\n# remove "<<n2>>", discard "<<missing>>", discard "<<n4>>"; print sorted(active)\n# last = {"<<n1>>"}; item = last.pop(); print item and len(last)\n',
          'active = {"<<n1>>", "<<n2>>", "<<n3>>", "<<n4>>"}\nactive.remove("<<n2>>")\nactive.discard("<<missing>>")\nactive.discard("<<n4>>")\nprint(sorted(active))\nlast = {"<<n1>>"}\nitem = last.pop()\nprint(item)\nprint(len(last))\n',
          checks=[("var", "item")], hints=["discard never raises, even for a missing item.", "pop on a one-element set always gives that element."], emoji="➖")

    c.add("set_membership", "Checking Set Membership", "Membership", "test membership quickly",
          [T("The scenario", "Every item arriving at <<biz>> is checked against an approved list. With thousands of items and thousands of approvals, how you store that list decides whether the check takes a blink or a minute."),
           T("in is fast on sets", "```python\nallowed = {\"a\", \"b\"}\nprint(\"a\" in allowed)       # True\nprint(\"z\" not in allowed)   # True\n```\n\nOn a **list**, `in` checks items one by one, so a list of a million items can mean a million comparisons. On a **set** (and a dictionary) Python jumps straight to the answer. If you build a collection mainly to ask \"is it in there?\", make it a set."),
           P('a = {"x", "y"}\nprint("x" in a, "z" in a, "z" not in a)', "True False True", ["True True True", "x y z"], "x is in, z is not, and \"not in\" reverses the answer."),
           Q("When is a set a better choice than a list?", ["For fast yes/no membership tests", "To keep items in order", "To read item number 3"], 0, "Sets answer membership quickly. Lists keep order and positions.")],
          "Write `is_approved(name)` that returns whether the name is in the set `approved = {\"<<n1>>\", \"<<n2>>\", \"<<n3>>\"}`. Print the answer for `\"<<n2>>\"`, for `\"<<n4>>\"` and for `\"<<missing>>\"`. It should print:\n\n<<OUT>>",
          'approved = {"<<n1>>", "<<n2>>", "<<n3>>"}\n# def is_approved(name): return whether name is in approved\n# print is_approved for "<<n2>>", "<<n4>>" and "<<missing>>"\n',
          'approved = {"<<n1>>", "<<n2>>", "<<n3>>"}\n\n\ndef is_approved(name):\n    return name in approved\n\n\nprint(is_approved("<<n2>>"))\nprint(is_approved("<<n4>>"))\nprint(is_approved("<<missing>>"))\n',
          checks=[("ftest", "is_approved", [[["<<n1>>".replace("<<n1>>", c.ctx["n1"])], True], [["zzz"], False]])], hints=["return name in approved", "The answer is a boolean."], emoji="⚡")

    c.add("set_union", "Set Union", "Union", "combine sets with union",
          [T("The scenario", "Two shelves each list the <<things>> they hold, and the office wants one combined list with no repeats. In set language that is the **union**: everything in either set."),
           T("Union", "```python\na = {1, 2, 3}\nb = {3, 4}\nprint(sorted(a | b))          # [1, 2, 3, 4]\nprint(sorted(a.union(b)))     # same thing\n```\n\n`a | b` makes a **new** set and leaves `a` and `b` alone. Anything in both appears once."),
           P("print(sorted({1, 2, 3} | {3, 4}))", "[1, 2, 3, 4]", ["[1, 2, 3, 3, 4]", "[3]"], "Union keeps everything from both, once."),
           Q("What is in a | b?", ["Everything that is in a or in b", "Only what is in both", "Only what is in a"], 0, "| is union.")],
          "Use the two shelves below. Print the sorted union with `|`, then with `.union()`, then how many items it has. It should print:\n\n<<OUT>>",
          SETS + "# print the sorted union with |, with .union(), and its length\n",
          SETS + 'print(sorted(shelf_a | shelf_b))\nprint(sorted(shelf_a.union(shelf_b)))\nprint(len(shelf_a | shelf_b))\n',
          checks=[("prints", 3)], hints=["shelf_a | shelf_b is the union.", "Wrap it in sorted() to print it."], emoji="🔀")

    c.add("set_intersection", "Set Intersection", "Intersection", "find what two sets share",
          [T("The scenario", "Which <<things>> appear on **both** shelves? Those are the ones that can be moved between them. In set language that is the **intersection**."),
           T("Intersection", "```python\na = {1, 2, 3}\nb = {3, 4}\nprint(sorted(a & b))                # [3]\nprint(sorted(a.intersection(b)))    # same\n```\n\nIf the sets share nothing, the result is the empty set `set()`."),
           P("print(sorted({1, 2, 3} & {2, 3, 4}))", "[2, 3]", ["[1, 2, 3, 4]", "[1, 4]"], "Only 2 and 3 are in both."),
           Q("What is in a & b?", ["Only what is in both", "Everything", "Only what is in a but not b"], 0, "& is intersection.")],
          "Using the two shelves, print the sorted intersection with `&`, with `.intersection()`, and then the intersection of `shelf_a` with `{\"<<missing>>\"}` as a sorted list. It should print:\n\n<<OUT>>",
          SETS + "# print the sorted intersection with &, with .intersection(), and shelf_a with {\"<<missing>>\"}\n",
          SETS + 'print(sorted(shelf_a & shelf_b))\nprint(sorted(shelf_a.intersection(shelf_b)))\nprint(sorted(shelf_a & {"<<missing>>"}))\n',
          checks=[("prints", 3)], hints=["& keeps only the shared items.", "No shared items gives an empty list when sorted."], emoji="🔗")

    c.add("set_difference", "Set Difference", "Difference", "find what is in one set and not the other",
          [T("The scenario", "Which <<things>> are on shelf A but **not** on shelf B? Those are the ones to move. Which are on B but not A? Different question, different answer. Difference depends on the order."),
           T("Difference", "```python\na = {1, 2, 3}\nb = {3, 4}\nprint(sorted(a - b))              # [1, 2]   in a, not in b\nprint(sorted(b - a))              # [4]      in b, not in a\nprint(sorted(a.difference(b)))    # same as a - b\n```\n\nUnlike union and intersection, `a - b` and `b - a` are **different**."),
           P("print(sorted({1, 2, 3} - {3, 4}), sorted({3, 4} - {1, 2, 3}))", "[1, 2] [4]", ["[1, 2] [1, 2]", "[4] [1, 2]"], "Each side keeps only what the other lacks."),
           Q("Does a - b equal b - a?", ["Not in general", "Always", "Only for numbers"], 0, "Difference depends on order.")],
          "Print three things about the two shelves, each sorted: what is on A but not B, what is on B but not A, and `shelf_a.difference(shelf_b)`. It should print:\n\n<<OUT>>",
          SETS + "# a minus b, b minus a, and shelf_a.difference(shelf_b)\n",
          SETS + 'print(sorted(shelf_a - shelf_b))\nprint(sorted(shelf_b - shelf_a))\nprint(sorted(shelf_a.difference(shelf_b)))\n',
          checks=[("prints", 3)], hints=["shelf_a - shelf_b keeps what only A has.", "Swap the sets for the other direction."], emoji="➖")

    c.add("set_symmetric_difference", "Symmetric Difference", "Either, not both", "find what is in exactly one of two sets",
          [T("The scenario", "Which <<things>> appear on **one shelf only**, either one? The shared items do not count. This is the **symmetric difference**: everything outside the overlap."),
           T("Symmetric difference", "```python\na = {1, 2, 3}\nb = {3, 4}\nprint(sorted(a ^ b))                          # [1, 2, 4]\nprint(sorted(a.symmetric_difference(b)))     # same\n```\n\nIt equals `(a | b) - (a & b)`: the union with the overlap removed. And unlike plain difference, it does not depend on order."),
           P("print(sorted({1, 2, 3} ^ {3, 4}))", "[1, 2, 4]", ["[3]", "[1, 2, 3, 4]"], "3 is shared, so it drops out. Everything else stays."),
           Q("What is in a ^ b?", ["Items in exactly one of the two", "Items in both", "All items"], 0, "^ is symmetric difference.")],
          "Print, sorted, the symmetric difference with `^`, with the method, and the same answer calculated as `(shelf_a | shelf_b) - (shelf_a & shelf_b)`. It should print:\n\n<<OUT>>",
          SETS + "# three prints: ^, .symmetric_difference(), and (a | b) - (a & b)\n",
          SETS + 'print(sorted(shelf_a ^ shelf_b))\nprint(sorted(shelf_a.symmetric_difference(shelf_b)))\nprint(sorted((shelf_a | shelf_b) - (shelf_a & shelf_b)))\n',
          checks=[("prints", 3)], hints=["The three lines print the same list.", "Brackets matter in the third line."], emoji="⚖️")

    c.add("subsets_supersets", "Subsets and Supersets", "Containment", "test whether one set contains another",
          [T("The scenario", "Does shelf B hold **only** items that shelf A also holds? Is A a complete superset of B? Containment questions are common: \"does this user have all the permissions needed?\""),
           T("Subset and superset", "```python\na = {1, 2, 3}\nb = {1, 2}\nprint(b <= a)                # True   b is a subset of a\nprint(b.issubset(a))         # True\nprint(a >= b)                # True   a is a superset of b\nprint(b < a)                 # True   a PROPER subset (not equal)\nprint(a <= a, a < a)         # True False\n```\n\nEvery set is a subset of itself. A **proper** subset must be strictly smaller."),
           P("print({1, 2} <= {1, 2, 3}, {1, 2} < {1, 2})", "True False", ["True True", "False False"], "{1, 2} is a subset of {1, 2, 3}. It is not a proper subset of itself."),
           Q("What does a >= b test?", ["Whether a is a superset of b", "Whether a is bigger in length", "Whether a comes later in the alphabet"], 0, "For sets, comparison operators test containment.")],
          "Use `small = {\"<<n1>>\", \"<<n3>>\"}` and `shelf_a`. Print, in this order: `small <= shelf_a`, `small.issubset(shelf_a)`, `shelf_a >= small`, `small < small` and `shelf_b <= shelf_a`. It should print:\n\n<<OUT>>",
          SETS + 'small = {"<<n1>>", "<<n3>>"}\n# five prints as listed in the task\n',
          SETS + 'small = {"<<n1>>", "<<n3>>"}\nprint(small <= shelf_a)\nprint(small.issubset(shelf_a))\nprint(shelf_a >= small)\nprint(small < small)\nprint(shelf_b <= shelf_a)\n',
          checks=[("prints", 5)], hints=["<= means subset, >= means superset.", "A set is never a proper subset of itself."], emoji="🎯")

    c.add("disjoint_sets", "Disjoint Sets", "No overlap", "test whether sets share nothing",
          [T("The scenario", "Two teams must not be given the same <<thing>>. Before assigning, the <<system>> must confirm their lists **do not overlap at all**. Such sets are called **disjoint**."),
           T("isdisjoint", "```python\na = {1, 2}\nb = {3, 4}\nprint(a.isdisjoint(b))      # True   nothing in common\nprint(a.isdisjoint({2}))    # False  they share 2\n```\n\n`isdisjoint` is the same as checking that the intersection is empty, but clearer and a little faster. Two empty sets are disjoint."),
           P("print({1, 2}.isdisjoint({3}), {1, 2}.isdisjoint({2, 3}))", "True False", ["False True", "True True"], "The first pair shares nothing. The second shares 2."),
           Q("Two sets are disjoint when...", ["They have no items in common", "They have the same items", "One contains the other"], 0, "Disjoint means an empty intersection.")],
          "Print five checks, in order: whether `shelf_a` and `{\"<<missing>>\"}` are disjoint, whether `shelf_a` and `shelf_b` are disjoint, and the same two tests written as `len(a & b) == 0`. Then print whether two empty sets are disjoint. It should print:\n\n<<OUT>>",
          SETS + "# five prints as listed in the task\n",
          SETS + 'print(shelf_a.isdisjoint({"<<missing>>"}))\nprint(shelf_a.isdisjoint(shelf_b))\nprint(len(shelf_a & {"<<missing>>"}) == 0)\nprint(len(shelf_a & shelf_b) == 0)\nprint(set().isdisjoint(set()))\n',
          checks=[("prints", 5)], hints=["isdisjoint is True when nothing is shared.", "len(a & b) == 0 says the same."], emoji="🚫")

    c.add("set_operators", "Set Operators", "Operators", "use the operator forms and update them in place",
          [T("The scenario", "You now know five set operations. This lesson collects the **operator** versions, plus the in-place forms, which change a set instead of building a new one."),
           T("The operator table", "- `a | b` union, `a & b` intersection\n- `a - b` difference, `a ^ b` symmetric difference\n- `a <= b`, `a < b`, `a >= b`, `a > b` containment\n\nIn-place versions change `a` itself:\n\n```python\na |= b      # add everything from b\na &= b      # keep only what is also in b\na -= b      # remove what is in b\na ^= b      # keep what is in exactly one\n```\n\nThe operators need **sets** on both sides. The method forms (`union`, `update`, ...) accept any iterable."),
           P("a = {1, 2, 3}\na &= {2, 3, 4}\na |= {9}\nprint(sorted(a))", "[2, 3, 9]", ["[1, 2, 3, 4, 9]", "[2, 3]"], "&= keeps 2 and 3, then |= adds 9."),
           Q("What does a -= b do?", ["Removes b's items from a, in place", "Builds a new set", "Adds b to a"], 0, "The augmented operators change the left set.")],
          "On a copy `work = shelf_a.copy()`, do these in order, printing `sorted(work)` after each: `work |= shelf_b`, `work &= {\"<<n1>>\", \"<<n3>>\", \"<<n4>>\"}`, `work -= {\"<<n3>>\"}`, `work ^= {\"<<n1>>\", \"<<missing>>\"}`. It should print:\n\n<<OUT>>",
          SETS + "work = shelf_a.copy()\n# four in-place operations, printing sorted(work) after each\n",
          SETS + 'work = shelf_a.copy()\nwork |= shelf_b\nprint(sorted(work))\nwork &= {"<<n1>>", "<<n3>>", "<<n4>>"}\nprint(sorted(work))\nwork -= {"<<n3>>"}\nprint(sorted(work))\nwork ^= {"<<n1>>", "<<missing>>"}\nprint(sorted(work))\n',
          checks=[("prints", 4)], hints=["Each operator changes work, so the next line starts from the new value.", "Print after every operation."], emoji="🧮")

    c.add("frozensets", "Immutable Sets with frozenset", "frozenset", "use frozenset when a set must not change",
          [T("The scenario", "A pair of <<things>> that are often sold together should be usable as a **dictionary key** (\"pair price\"), in either order. A normal set cannot be a key, because it can change. A `frozenset` cannot change, so it can."),
           T("frozenset", "```python\nf = frozenset({1, 2})\nprint(f | {3})            # works: gives a NEW frozenset\nf.add(5)                  # AttributeError: no add\nprices = {frozenset({\"a\", \"b\"}): 9}\nprint(prices[frozenset({\"b\", \"a\"})])   # 9, order does not matter\n```\n\nA frozenset supports every read-only operation: union, intersection, `in`, `len`. It is **hashable**, so it can be a dictionary key or a member of another set."),
           P("f = frozenset({1, 2})\nprint(len(f), 2 in f)", "2 True", ["2 False", "!AttributeError"], "Reading works. Only changing is forbidden."),
           Q("Why can a frozenset be a dictionary key but a set cannot?", ["It cannot change, so it is hashable", "It is shorter", "It is sorted"], 0, "Keys must be hashable, which needs an unchangeable value.")],
          "Build `bundles`, a dictionary whose keys are frozensets: `frozenset({\"<<n1>>\", \"<<n2>>\"})` mapped to `\"starter pack\"` and `frozenset({\"<<n3>>\", \"<<n4>>\"})` mapped to `\"value pack\"`. Look up the first bundle with the names given in the **opposite order** and print the result, then print `len(bundles)`. It should print:\n\n<<OUT>>",
          "# bundles = a dictionary with two frozenset keys\n# print the lookup of frozenset({\"<<n2>>\", \"<<n1>>\"}), then len(bundles)\n",
          'bundles = {\n    frozenset({"<<n1>>", "<<n2>>"}): "starter pack",\n    frozenset({"<<n3>>", "<<n4>>"}): "value pack",\n}\nprint(bundles[frozenset({"<<n2>>", "<<n1>>"})])\nprint(len(bundles))\n',
          checks=[("prints", 2)], hints=["frozenset({...}) goes in the key position.", "Order inside the braces does not matter."], emoji="🧊")

    c.add("set_comprehensions", "Set Comprehensions", "Comprehensions", "build sets with comprehensions",
          [T("The scenario", "From the names you want the distinct name lengths, the distinct first letters, and the set of low <<things>>. A **set comprehension** builds each in one line, and removes repeats for free."),
           T("The pattern", "```python\nwords = [\"cat\", \"dog\", \"bee\", \"ant\"]\nlengths = {len(w) for w in words}            # {3}\nfirst = {w[0] for w in words}                # {'c', 'd', 'b', 'a'}\nshort = {w for w in words if w[0] < \"c\"}     # filter\n```\n\nIt looks like a list comprehension with curly braces and **no** `key: value` colon (that would make a dictionary). Print sorted to keep the output steady."),
           P('print(sorted({len(w) for w in ["a", "bb", "cc"]}))', "[1, 2]", ["[1, 2, 2]", "[2, 1]"], "The lengths are 1, 2, 2 and the set keeps each once."),
           Q("What do the curly braces and a for-clause without a colon make?", ["A set", "A dictionary", "A tuple"], 0, "Curly braces with key: value make a dictionary. Without the colon, a set.")],
          "Write three set comprehensions over `<<vnames>>` and the counts, and print each sorted. It should print:\n\n<<OUT>>\n\n- `lengths`: the lengths of the names\n- `initials`: the first letter of each name\n- `low_set`: the names whose count is at or below `<<vl>>` (use `zip` with `counts`)",
          "counts = <<qlist>>\n# lengths, initials, low_set: one set comprehension each, then print sorted versions\n",
          'counts = <<qlist>>\nlengths = {len(name) for name in <<vnames>>}\ninitials = {name[0] for name in <<vnames>>}\nlow_set = {name for name, count in zip(<<vnames>>, counts) if count <= <<vl>>}\nprint(sorted(lengths))\nprint(sorted(initials))\nprint(sorted(low_set))\n',
          checks=[("ast", "SetComp", "a set comprehension"), ("var", "lengths")], hints=["{expression for item in collection}", "A filter goes at the end with if."], emoji="⚡")

    c.add("common_set_operations", "Common Set Operations", "Chapter 11 project", "combine set skills into helpers",
          [T("The scenario", "Three set jobs come up constantly: find the duplicates in a list, find what two lists share, and find what is missing from a required list. They make short, powerful helpers for the <<system>>."),
           T("The patterns", "- **Duplicates**: walk the list with a `seen` set. An item already seen is a duplicate\n- **In common**: `set(a) & set(b)`\n- **Missing**: `set(required) - set(present)`\n\nEach returns a **sorted list**, so the answer is steady and easy to compare."),
           Q("Which expression finds what is required but not present?", ["set(required) - set(present)", "set(required) & set(present)", "set(present) - set(required)"], 0, "Required, minus what is present, leaves what is missing.")],
          "Write `duplicates(items)` (sorted list of items that appear more than once), `common(first, second)` (sorted list of what both share) and `missing_from(required, present)` (sorted list of what is required but absent). Print one result from each. It should print:\n\n<<OUT>>",
          "# duplicates, common, missing_from: each returns a sorted list\n# print duplicates([3, 1, 3, 2, 1]), common([1, 2, 3], [2, 3, 4]) and missing_from([\"a\", \"b\", \"c\"], [\"b\"])\n",
          'def duplicates(items):\n    seen = set()\n    dupes = set()\n    for item in items:\n        if item in seen:\n            dupes.add(item)\n        else:\n            seen.add(item)\n    return sorted(dupes)\n\n\ndef common(first, second):\n    return sorted(set(first) & set(second))\n\n\ndef missing_from(required, present):\n    return sorted(set(required) - set(present))\n\n\nprint(duplicates([3, 1, 3, 2, 1]))\nprint(common([1, 2, 3], [2, 3, 4]))\nprint(missing_from(["a", "b", "c"], ["b"]))\n',
          checks=[("ftest", "duplicates", [[[[3, 1, 3, 2, 1]], [1, 3]]]), ("ftest", "common", [[[[1, 2, 3], [2, 3, 4]], [2, 3]]]), ("ftest", "missing_from", [[[["a", "b", "c"], ["b"]], ["a", "c"]]])],
          hints=["duplicates: an item already in seen goes into dupes.", "& finds the overlap, - finds the missing ones."], emoji="🏁")
