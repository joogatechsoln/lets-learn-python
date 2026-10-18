"""Chapter 10: Dictionaries (15 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Dictionaries")
    X = c.ctx
    VS, VR, VREP, VFIND = X["vstock"], X["vrates"], X["vrep"], X["vfind"]
    n1, n2, n3 = X["n1"], X["n2"], X["n3"]
    q1, q2, d = X["q1"], X["q2"], X["d"]
    PRE = "counts = <<qlist>>\nprice_list = <<plist>>\n"

    c.add("intro_dicts", "Introduction to Dictionaries", "Dictionaries", "describe a thing with key-value pairs",
          [T("The scenario", "A list tells you what you have, in order. It cannot tell you what each number **means**: position 1 is the count, position 2 the rate, but who remembers that? A **dictionary** labels every value with a key."),
           T("Key and value", "A dictionary stores **pairs**: a key, then its value.\n\n```python\nperson = {\"name\": \"Ada\", \"age\": 36}\nprint(person[\"name\"])     # Ada\nprint(len(person))        # 2\n```\n\nYou look values up by **key**, not by position. That is why dictionaries are fast and why the code reads like English: `price[\"Rice\"]`."),
           T("When to use which", "- **List**: an ordered collection of similar things\n- **Dictionary**: a lookup table, or one thing with named parts\n\nMost real data is dictionaries: a record, a settings file, a JSON message from a web service."),
           P('p = {"name": "Ada", "age": 36}\nprint(p["age"], len(p))', "36 2", ["Ada 2", "age 36"], "p[\"age\"] looks up the value 36, and len counts the two pairs."),
           Q("How do you read a value from a dictionary?", ["With its key in square brackets", "With its position number", "With a dot and a number"], 0, "A dictionary is a lookup by key.")],
          "Describe the first <<thing>> as a dictionary called `record` with three keys: `\"name\"` (`\"<<n1>>\"`), `\"<<aq>>\"` (<<q1>>) and `\"<<ar>>\"` (<<p1>>). Print the whole record and then just its name. It should print:\n\n<<OUT>>",
          "# record = a dictionary with the keys name, <<aq>> and <<ar>>\n# print the record, then record[\"name\"]\n",
          'record = {"name": "<<n1>>", "<<aq>>": <<q1>>, "<<ar>>": <<p1>>}\nprint(record)\nprint(record["name"])\n',
          checks=[("var", "record")], hints=["Pairs are written key: value, separated by commas.", "Keys that are text need quotes."], emoji="🗃️")

    c.add("creating_dicts", "Creating Dictionaries", "Creating", "create dictionaries in several ways",
          [T("The scenario", "The <<system>> needs two lookups: how many of each <<thing>> are on hand, and what each costs. They already exist as lists. You will turn them into dictionaries, which become the project's data store."),
           T("Ways to create one", "```python\nd = {\"a\": 1, \"b\": 2}                 # literal\nempty = {}                             # empty (not a set!)\nd2 = dict(zip([\"a\", \"b\"], [1, 2]))     # from two lists\nflags = dict.fromkeys([\"a\", \"b\"], False)   # same value for every key\n```\n\n`zip` pairs the two lists item by item, and `dict` turns the pairs into entries."),
           T("Order and duplicates", "Dictionaries keep **insertion order**. A key can appear only once: if you repeat a key, the last value wins."),
           P('print(dict(zip(["a", "b"], [1, 2])))', "{'a': 1, 'b': 2}", ["[('a', 1), ('b', 2)]", "{1: 'a', 2: 'b'}"], "zip pairs names with numbers, and dict turns the pairs into a dictionary."),
           Q("What does {} create?", ["An empty dictionary", "An empty set", "An empty list"], 0, "Empty curly braces are a dictionary. An empty set is set().")],
          "Create the project's two lookup tables and some practice ones, and print them. It should print:\n\n<<OUT>>\n\n- `<<vstock>>`: each name mapped to its count, built with `dict(zip(...))`\n- `<<vrates>>`: each name mapped to its rate, as a dictionary literal\n- `empty`: an empty dictionary\n- `seen`: every name mapped to `False`, with `dict.fromkeys`",
          PRE + "# <<vstock>> from zip, <<vrates>> as a literal, empty, seen\n# print them in that order\n",
          PRE + '<<vstock>> = dict(zip(<<vnames>>, counts))\n<<vrates>> = {"<<n1>>": <<p1>>, "<<n2>>": <<p2>>, "<<n3>>": <<p3>>, "<<n4>>": <<p4>>}\nempty = {}\nseen = dict.fromkeys(<<vnames>>, False)\nprint(<<vstock>>)\nprint(<<vrates>>)\nprint(empty)\nprint(seen)\n',
          checks=[("var", VS), ("var", VR)], hints=["dict(zip(names, counts)) pairs them up.", "The literal needs four pairs: \"name\": rate."], emoji="🧱")

    c.add("keys_values", "Keys and Values", "Keys and values", "use keys(), values() and items()",
          [T("The scenario", "A manager wants three quick facts: which <<things>> exist, how many there are in total, and how many different ones. The dictionary can answer each if you ask for its **keys**, its **values** or its **pairs**."),
           T("The three views", "```python\nd = {\"a\": 1, \"b\": 2}\nd.keys()      # the keys:   dict_keys(['a', 'b'])\nd.values()    # the values: dict_values([1, 2])\nd.items()     # the pairs:  dict_items([('a', 1), ('b', 2)])\n```\n\nWrap them in `list(...)` to see them as a normal list, and use `sum`, `max`, `len` on them directly."),
           T("What can be a key?", "Keys must be **hashable**: text, numbers and tuples are fine. A list cannot be a key (TypeError: unhashable type). Values can be anything, even other dictionaries."),
           P('d = {"a": 1, "b": 2}\nprint(list(d.keys()), sum(d.values()))', "['a', 'b'] 3", ["['a', 'b'] [1, 2]", "[1, 2] 3"], "The keys as a list, and the values added together."),
           Q("Which of these cannot be a dictionary key?", ["A list", "A string", "A tuple of numbers"], 0, "Lists are mutable and unhashable, so they cannot be keys.")],
          "Ask `<<vstock>>` three questions and print the answers. It should print:\n\n<<OUT>>\n\n- the list of its keys\n- the list of its values\n- the total of all its values, then how many keys it has",
          "# print list(<<vstock>>.keys()), list(<<vstock>>.values()), then sum of the values and len of the dictionary\n",
          'print(list(<<vstock>>.keys()))\nprint(list(<<vstock>>.values()))\nprint(sum(<<vstock>>.values()), len(<<vstock>>))\n',
          checks=[("prints", 3)], hints=["list(d.keys()) shows the keys as a list.", "sum(d.values()) adds the values."], emoji="🔑")

    c.add("dict_access", "Accessing Dictionary Elements", "Looking up", "read values by key and handle a missing key",
          [T("The scenario", "A customer asks for the count of the <<n2>> and the rate of the <<n3>>. Two lookups, by name. And someone will ask about something you do not stock, which will teach you about `KeyError`."),
           T("Square brackets", "```python\nd = {\"a\": 1, \"b\": 2}\nprint(d[\"b\"])       # 2\nprint(d[\"z\"])       # KeyError: 'z'\n```\n\nKeys are matched **exactly**, capitals included. A missing key raises a **KeyError** whose message is the key Python could not find."),
           T("Never by position", "You cannot ask a dictionary for item number 0. If you ever need the first key, use `list(d)[0]`, but it is a sign you wanted a list. Next lessons show safe lookups with `in` and `get`."),
           P('d = {"a": 1}\nprint(d["a"])\nprint(d["b"])', "!KeyError", ["1", "None"], "Python prints 1 first, then stops with a KeyError on the second line. Because the whole program crashes, the question is about the error type."),
           Q("What does d[\"z\"] do if \"z\" is not a key?", ["Raises a KeyError", "Returns None", "Returns 0"], 0, "Square-bracket lookup insists the key exists.")],
          "Look values up in the two project dictionaries and print them. It should print:\n\n<<OUT>>\n\n- the count of `\"<<n2>>\"`\n- the rate of `\"<<n3>>\"`\n- the value of that rate times that count of `\"<<n3>>\"`, from both dictionaries\n- the first key, using `list(<<vstock>>)[0]`",
          "# four prints using <<vstock>> and <<vrates>>\n",
          'print(<<vstock>>["<<n2>>"])\nprint(<<vrates>>["<<n3>>"])\nprint(<<vstock>>["<<n3>>"] * <<vrates>>["<<n3>>"])\nprint(list(<<vstock>>)[0])\n',
          checks=[("prints", 4)], hints=["<<vstock>>[\"name\"] looks up a count.", "Check the spelling and capitals of every key."], emoji="🔍")

    c.add("dict_add_update", "Adding and Updating Key-Value Pairs", "Changing entries", "add and update entries",
          [T("The scenario", "A new <<thing>> is stocked and an existing one receives a delivery. The same line of code does both jobs: it **adds** the key if it is new and **updates** it if it exists."),
           T("Assignment", "```python\nd = {\"a\": 1}\nd[\"b\"] = 2          # new key: added\nd[\"a\"] = 10         # existing key: replaced\nd[\"a\"] += 5         # update using the old value\nd.update({\"c\": 3, \"b\": 20})   # many at once\n```\n\nBecause the same syntax adds and updates, a **typo in a key silently creates a new entry** instead of failing. Check your spelling."),
           P('d = {"a": 1}\nd["b"] = 2\nd["a"] += 5\nprint(d)', "{'a': 6, 'b': 2}", ["{'a': 1, 'b': 2}", "{'a': 6}"], "b is added and a goes from 1 to 6."),
           Q("What does d[\"x\"] = 5 do when \"x\" already exists?", ["Replaces its value", "Raises a KeyError", "Adds a second x"], 0, "A key exists once. Assignment replaces the value.")],
          "Work on a **copy** of the stock so the original stays safe. Make `inventory = <<vstock>>.copy()`, add `\"<<missing>>\"` with a count of 0, add the delivery of <<d>> to `\"<<n1>>\"`, and merge in `{\"<<n2>>\": 0}` using `update`. Print `inventory` after each of the three changes. It should print:\n\n<<OUT>>",
          "inventory = <<vstock>>.copy()\n# three changes, printing inventory after each\n",
          'inventory = <<vstock>>.copy()\ninventory["<<missing>>"] = 0\nprint(inventory)\ninventory["<<n1>>"] += <<d>>\nprint(inventory)\ninventory.update({"<<n2>>": 0})\nprint(inventory)\n',
          checks=[("var", "inventory")], hints=["inventory[\"new key\"] = 0 adds an entry.", "update takes a dictionary of changes."], emoji="➕")

    c.add("dict_removing", "Removing Dictionary Elements", "Removing entries", "remove entries safely",
          [T("The scenario", "A <<thing>> is discontinued and must come off the list. Python removes dictionary entries by key, and offers a way to remove **and keep** the value."),
           T("Ways to remove", "```python\nd = {\"a\": 1, \"b\": 2, \"c\": 3}\nv = d.pop(\"a\")            # removes and returns 1\nv = d.pop(\"z\", 0)         # a default avoids KeyError\ndel d[\"b\"]                # removes, returns nothing\nlast = d.popitem()        # removes the last pair\nd.clear()                 # empties it\n```\n\n`pop` and `del` raise a KeyError for a missing key, unless `pop` is given a default."),
           P('d = {"a": 1, "b": 2}\nx = d.pop("a")\nprint(x, d)', "1 {'b': 2}", ["{'b': 2} 1", "1 {'a': 1, 'b': 2}"], "pop removes the entry and hands back its value."),
           Q("Which removes a key without raising an error if it is missing?", ["d.pop(key, default)", "del d[key]", "d.remove(key)"], 0, "pop with a default value never raises KeyError.")],
          "On a copy `inventory = <<vstock>>.copy()`, pop `\"<<n2>>\"` into `popped`, delete `\"<<n3>>\"` with `del`, and try to pop `\"<<missing>>\"` with a default of `-1` into `ghost`. Print `inventory`, then `popped`, then `ghost`. It should print:\n\n<<OUT>>",
          "inventory = <<vstock>>.copy()\n# popped = pop \"<<n2>>\"; del \"<<n3>>\"; ghost = pop \"<<missing>>\" with default -1\n# print inventory, popped, ghost\n",
          'inventory = <<vstock>>.copy()\npopped = inventory.pop("<<n2>>")\ndel inventory["<<n3>>"]\nghost = inventory.pop("<<missing>>", -1)\nprint(inventory)\nprint(popped)\nprint(ghost)\n',
          checks=[("var", "popped"), ("var", "ghost")], hints=["inventory.pop(\"key\") returns the removed value.", "pop(\"key\", -1) returns -1 when the key is absent."], emoji="➖")

    c.add("dict_methods", "Dictionary Methods", "Methods", "use the main dictionary methods",
          [T("The scenario", "Everyday dictionary jobs have ready-made methods: give a missing key a starting value, merge another dictionary in, copy a whole table. Learn the short list and you will rarely write a loop for them."),
           T("The short list", "```python\nd = {\"a\": 1}\nd.get(\"z\", 0)             # 0, no KeyError\nd.setdefault(\"b\", 5)       # adds b=5 if absent, returns the value\nd.update({\"c\": 7})         # merge another dictionary in\ne = d.copy()               # a separate shallow copy\nd.items()                  # pairs for a loop\n```\n\n`setdefault` is perfect for \"create it if it is not there yet\" and is the heart of grouping data."),
           P('d = {"a": 1}\nd.setdefault("a", 9)\nd.setdefault("b", 9)\nprint(d)', "{'a': 1, 'b': 9}", ["{'a': 9, 'b': 9}", "{'a': 1}"], "setdefault leaves an existing key alone and only adds a missing one."),
           Q("What does setdefault(key, v) do if the key exists?", ["Leaves it unchanged", "Replaces it with v", "Raises a KeyError"], 0, "It only adds the key when it is absent.")],
          "Try four methods on a copy `shelf = <<vstock>>.copy()`. It should print:\n\n<<OUT>>\n\n- `shelf.get(\"<<missing>>\", 0)`\n- `shelf.setdefault(\"<<missing>>\", 5)`, then print `shelf`\n- `shelf.update({\"<<n1>>\": 0})`, then print `shelf`\n- the number of keys",
          "shelf = <<vstock>>.copy()\n# four steps, each printing something\n",
          'shelf = <<vstock>>.copy()\nprint(shelf.get("<<missing>>", 0))\nprint(shelf.setdefault("<<missing>>", 5))\nprint(shelf)\nshelf.update({"<<n1>>": 0})\nprint(shelf)\nprint(len(shelf))\n',
          checks=[("var", "shelf")], hints=["get with a default never raises.", "setdefault returns the value after adding it."], emoji="🧰")

    c.add("dict_iterating", "Iterating Through Dictionaries", "Looping", "loop over dictionaries and build the report",
          [T("The scenario", "Time for the project's first real report: every <<thing>>, its total, and a grand total. That needs a loop over the dictionary, and the report will become a function you keep."),
           T("Three ways to loop", "```python\nd = {\"a\": 1, \"b\": 2}\nfor key in d:                   # keys (the default)\n    print(key)\nfor value in d.values():        # values only\n    print(value)\nfor key, value in d.items():    # both at once\n    print(key, value)\n```\n\n`items()` is the one you will use most. `sorted(d)` loops in key order."),
           P('d = {"a": 1, "b": 2}\nfor k, v in d.items():\n    print(k, v * 10)', "a 10\nb 20", ["a 1\nb 2", "10\n20"], "items gives each key and value, and the body prints the key and ten times the value."),
           Q("What does a plain `for x in d:` give you?", ["The keys", "The values", "The pairs"], 0, "Looping over a dictionary visits its keys.")],
          "Write the report as a function `<<vrep>>()` that loops over `<<vstock>>`, and prints one line per <<thing>> and a total. It must use `<<vfn>>` from the functions chapter and `<<vrates>>` for the rates. Call it once. It should print:\n\n<<OUT>>",
          "# def <<vrep>>(): loop over <<vstock>>, look up each rate in <<vrates>>, print a line, add to the total, print the total\n# then call <<vrep>>()\n",
          'def <<vrep>>():\n    grand_total = 0\n    for name, <<aq>> in <<vstock>>.items():\n        <<ar>> = <<vrates>>[name]\n        line_total = <<vfn>>(<<aq>>, <<ar>>)\n        print(f"- {name}: {<<aq>>} x <<rp>>{<<ar>>}<<rs>> = <<tp>>{line_total}<<ts>>")\n        grand_total += line_total\n    print(f"<<total_label>>: <<tp>>{grand_total}<<ts>>")\n\n\n<<vrep>>()\n',
          checks=[("ast", "For", "a for loop"), ("fout", VREP)], hints=["for name, <<aq>> in <<vstock>>.items():", "The total is a running sum: grand_total += line_total."], emoji="🔁")

    c.add("key_membership", "Checking Key Membership", "Is it there?", "test whether a key exists",
          [T("The scenario", "Before reading a count, the program should ask: *do we even stock that?* Checking first avoids the KeyError. The same test also powers one of the most useful patterns in programming: counting."),
           T("in and not in", "`in` on a dictionary checks the **keys**:\n\n```python\nd = {\"a\": 1}\nprint(\"a\" in d)        # True\nprint(\"z\" in d)        # False\nprint(\"z\" not in d)    # True\n```\n\nThe values are not searched: `1 in d` is False. To search values use `1 in d.values()`."),
           T("Counting with a dictionary", "```python\ncounts = {}\nfor ch in \"banana\":\n    if ch in counts:\n        counts[ch] += 1\n    else:\n        counts[ch] = 1\n```\n\nFirst sight of a letter creates its entry, later sights add one."),
           P('d = {"a": 1}\nprint("a" in d, 1 in d)', "True False", ["True True", "False False"], "`in` looks at keys only. 1 is a value, not a key."),
           Q("Does `in` search a dictionary's keys or values?", ["Keys", "Values", "Both"], 0, "Use `in d.values()` to search values.")],
          "First print three membership tests: `\"<<n2>>\" in <<vstock>>`, `\"<<missing>>\" in <<vstock>>` and `\"<<missing>>\" not in <<vstock>>`. Then count the letters of `\"<<stag>><<stag>>\"` into a dictionary `letter_counts` with the pattern above and print it. It should print:\n\n<<OUT>>",
          "# three membership prints, then count the letters of \"<<stag>><<stag>>\" into letter_counts and print it\n",
          'print("<<n2>>" in <<vstock>>)\nprint("<<missing>>" in <<vstock>>)\nprint("<<missing>>" not in <<vstock>>)\nletter_counts = {}\nfor ch in "<<stag>><<stag>>":\n    if ch in letter_counts:\n        letter_counts[ch] += 1\n    else:\n        letter_counts[ch] = 1\nprint(letter_counts)\n',
          checks=[("var", "letter_counts")], hints=["if ch in letter_counts: add one, else: start at 1.", "The three tests print True, False, True."], emoji="❓")

    c.add("dict_get", "The get() Method", "Safe lookup", "look up safely with get()",
          [T("The scenario", "Staff asks the system \"how many <<n2>> do we have?\" all day, and sometimes about things you do not stock. A lookup function must **never crash**. It must answer, or say clearly that it has no answer."),
           T("get", "`d.get(key)` returns the value, or **None** if the key is missing. A second argument is the fallback:\n\n```python\nd = {\"a\": 1}\nd.get(\"a\")        # 1\nd.get(\"z\")        # None\nd.get(\"z\", 0)     # 0\n```\n\nBecause `None` means \"nothing\", you test for it with `is None`."),
           T("Your own lookup function", "Wrapping `get` in a function gives the whole team one safe way to look things up, with one place to fix if the rule changes."),
           P('d = {"a": 1}\nprint(d.get("z"), d.get("z", 0))', "None 0", ["0 0", "!KeyError"], "get returns None when the key is missing, or the fallback if you give one."),
           Q("What does d.get(\"missing\") return?", ["None", "0", "An error"], 0, "None, unless you pass a different default.")],
          "Write `<<vfind>>(name)` that returns the count of that <<thing>> from `<<vstock>>`, or `None` if it is not stocked. Then print the count for `\"<<n2>>\"`, and for `\"<<missing>>\"` print `<<missing_msg_f>>` when the result is `None`. It should print:\n\n<<OUT>>",
          "# def <<vfind>>(name): return the count or None\n# print the count for \"<<n2>>\"; look up \"<<missing>>\" and print the message when the result is None\n",
          'def <<vfind>>(name):\n    return <<vstock>>.get(name)\n\n\nprint(<<vfind>>("<<n2>>"))\nresult = <<vfind>>("<<missing>>")\nif result is None:\n    print("<<missing_msg_f>>")\n',
          checks=[("ftest", VFIND, [[[n2], q2], [["zzz"], None]])], hints=["return <<vstock>>.get(name) does the whole job.", "Test the result with `is None`."], emoji="🎯")

    c.add("nested_dicts", "Nested Dictionaries", "Dictionaries in dictionaries", "model records inside a lookup table",
          [T("The scenario", "The lookups so far give one number per name. A real <<thing>> has several facts: how many, what rate. Put a **dictionary inside a dictionary**, one record per name."),
           T("Dictionaries as values", "```python\ncatalog = {\n    \"a\": {\"units\": 10, \"price\": 2.5},\n    \"b\": {\"units\": 4,  \"price\": 7.0},\n}\nprint(catalog[\"a\"][\"price\"])      # 2.5\ncatalog[\"b\"][\"units\"] += 1        # update inside\n```\n\nThe first key picks the record and the second picks the fact. Chains like `catalog[\"a\"][\"price\"]` read left to right."),
           P('c = {"a": {"n": 1}}\nc["a"]["n"] += 4\nprint(c)', "{'a': {'n': 5}}", ["{'a': {'n': 1}}", "{'a': 5}"], "The inner dictionary is changed in place."),
           Q("In catalog[\"a\"][\"price\"], what does catalog[\"a\"] give?", ["The inner dictionary for a", "The price", "An error"], 0, "The first lookup returns the inner dictionary, and the second reads from it.")],
          "Build `catalog`: one record per name with the keys `\"units\"` and `\"price\"`, using a loop over `zip(<<vnames>>, counts, price_list)`. Then print the units of `\"<<n2>>\"`, add the delivery of <<d>> to them and print that record, and finally print the total value of the whole catalog. It should print:\n\n<<OUT>>",
          PRE + "catalog = {}\n# fill catalog; print catalog[\"<<n2>>\"][\"units\"]; add <<d>> to it and print the record; print the total value\n",
          PRE + 'catalog = {}\nfor name, units, price in zip(<<vnames>>, counts, price_list):\n    catalog[name] = {"units": units, "price": price}\nprint(catalog["<<n2>>"]["units"])\ncatalog["<<n2>>"]["units"] += <<d>>\nprint(catalog["<<n2>>"])\ntotal = 0\nfor name in catalog:\n    total += catalog[name]["units"] * catalog[name]["price"]\nprint(total)\n',
          checks=[("var", "catalog"), ("var", "total")], hints=["catalog[name] = {\"units\": units, \"price\": price}", "catalog[name][\"units\"] reads a fact."], emoji="🪆")

    c.add("dict_comprehensions", "Dictionary Comprehensions", "Comprehensions", "build dictionaries with comprehensions",
          [T("The scenario", "Three new tables are needed from the existing data: the value of each <<thing>>, only the low ones, and a reverse lookup from count to name. A **dictionary comprehension** builds each in one line."),
           T("The pattern", "```python\nd = {\"a\": 1, \"b\": 2, \"c\": 3}\ndoubled = {k: v * 2 for k, v in d.items()}        # {'a': 2, 'b': 4, 'c': 6}\nbig = {k: v for k, v in d.items() if v > 1}        # {'b': 2, 'c': 3}\nflipped = {v: k for k, v in d.items()}             # {1: 'a', 2: 'b', 3: 'c'}\n```\n\nThe curly braces and the `key: value` part make it a dictionary. If two entries produce the same key, the later wins."),
           P('d = {"a": 1, "b": 2}\nprint({k: v + 10 for k, v in d.items()})', "{'a': 11, 'b': 12}", ["{'a': 1, 'b': 2}", "[11, 12]"], "Each value gets 10 added, and the keys stay."),
           Q("What does {v: k for k, v in d.items()} do?", ["Swaps keys and values", "Sorts the dictionary", "Deletes the values"], 0, "Each pair is written the other way round.")],
          "Build three dictionaries and print each. It should print:\n\n<<OUT>>\n\n- `values`: each name mapped to its count times its rate (use `<<vfn>>`)\n- `low`: only the names whose count is at or below `<<vl>>`, mapped to their count\n- `by_count`: each count mapped to its name",
          "# values, low, by_count: one dictionary comprehension each, then print them\n",
          'values = {name: <<vfn>>(<<vstock>>[name], <<vrates>>[name]) for name in <<vstock>>}\nlow = {name: count for name, count in <<vstock>>.items() if count <= <<vl>>}\nby_count = {count: name for name, count in <<vstock>>.items()}\nprint(values)\nprint(low)\nprint(by_count)\n',
          checks=[("ast", "DictComp", "a dictionary comprehension"), ("var", "values"), ("var", "low")], hints=["{name: ... for name in <<vstock>>}", "Filter with if count <= <<vl>> at the end."], emoji="⚡")

    c.add("merging_dicts", "Merging Dictionaries", "Merging", "combine dictionaries",
          [T("The scenario", "Every record starts from defaults and then gets the details of the one <<thing>>. Settings files work the same way: defaults, overridden by what the user chose. You need to **merge** dictionaries, with later values winning."),
           T("Ways to merge", "```python\na = {\"x\": 1, \"y\": 2}\nb = {\"y\": 20, \"z\": 30}\nmerged = {**a, **b}        # {'x': 1, 'y': 20, 'z': 30}  (b wins)\na.update(b)                # changes a in place\n```\n\n`{**a, **b}` makes a **new** dictionary and works on every Python version. Newer Pythons (3.9 and up) also offer `a | b`. When a key is in both, the **last one wins**."),
           P('a = {"x": 1, "y": 2}\nb = {"y": 20}\nprint({**a, **b})', "{'x': 1, 'y': 20}", ["{'x': 1, 'y': 2}", "{'y': 20}"], "y appears in both, so b's value 20 wins."),
           Q("In {**a, **b}, which wins for a key in both?", ["b, the later one", "a, the earlier one", "Neither: it raises an error"], 0, "Later entries overwrite earlier ones.")],
          "Merge two layers into `merged`, and add a new item to the stock without changing the original. It should print:\n\n<<OUT>>\n\n- `defaults` is `{\"units\": 0, \"price\": 1.0, \"unit\": \"<<qty_unit>>\"}`\n- `overrides` is `{\"units\": <<q1>>, \"price\": <<p1>>}`\n- `merged` combines them with `{**defaults, **overrides}`\n- `bigger` is `{**<<vstock>>, \"<<missing>>\": 0}`",
          "# defaults, overrides, merged, bigger: then print merged and bigger\n",
          'defaults = {"units": 0, "price": 1.0, "unit": "<<qty_unit>>"}\noverrides = {"units": <<q1>>, "price": <<p1>>}\nmerged = {**defaults, **overrides}\nbigger = {**<<vstock>>, "<<missing>>": 0}\nprint(merged)\nprint(bigger)\n',
          checks=[("var", "merged"), ("var", "bigger")], hints=["{**a, **b} puts a's pairs first and b's after them.", "Adding one pair: {**<<vstock>>, \"key\": 0}"], emoji="🧬")

    c.add("dict_unpacking", "Dictionary Unpacking", "Unpacking", "pass dictionaries as keyword arguments",
          [T("The scenario", "A form delivers a record as a dictionary. A function wants three separate arguments. Writing `f(row[\"name\"], row[\"units\"], row[\"price\"])` every time is tedious. The `**` operator unpacks the dictionary into named arguments."),
           T("** in a call and in a definition", "```python\ndef describe(name, units, price):\n    return f\"{name}: {units} at {price}\"\n\nrow = {\"name\": \"Rice\", \"units\": 15, \"price\": 5.0}\nprint(describe(**row))        # keys become keyword arguments\n```\n\nThe other direction collects extra keywords into a dictionary:\n\n```python\ndef show(**details):\n    for key in sorted(details):\n        print(key, details[key])\n```"),
           P('def f(a, b):\n    return a - b\nprint(f(**{"b": 1, "a": 5}))', "4", ["-4", "!TypeError"], "The keys become the keyword arguments a=5 and b=1."),
           Q("What does f(**row) do?", ["Passes each key and value as a named argument", "Passes the dictionary as one argument", "Deletes the dictionary"], 0, "** unpacks the pairs into keyword arguments.")],
          "Write `make_line(name, units, price)` that returns `name: units x price`, and `show(**details)` that prints each key and value in sorted key order. Use `**` to call `make_line` with the dictionary `row` of the first <<thing>>, and to call `show`. It should print:\n\n<<OUT>>",
          'row = {"name": "<<n1>>", "units": <<q1>>, "price": <<p1>>}\n# make_line(name, units, price) returns "name: units x price"; show(**details) prints key value in sorted order\n# print make_line(**row), then call show(**row)\n',
          'row = {"name": "<<n1>>", "units": <<q1>>, "price": <<p1>>}\n\n\ndef make_line(name, units, price):\n    return f"{name}: {units} x {price}"\n\n\ndef show(**details):\n    for key in sorted(details):\n        print(key, details[key])\n\n\nprint(make_line(**row))\nshow(**row)\n',
          checks=[("ftest", "make_line", [[["a", 2, 3], "a: 2 x 3"]])], hints=["print(make_line(**row))", "Inside show, details is an ordinary dictionary."], emoji="📦")

    c.add("common_dict_operations", "Common Dictionary Operations", "Chapter 10 project", "combine dictionary skills into helpers",
          [T("The scenario", "Three dictionary jobs come up in almost every project: count how often things occur, group things by a property, and find the winner. You will write each as a small function and keep them."),
           T("The patterns", "- **Count**: `counts[x] = counts.get(x, 0) + 1`\n- **Group**: `groups.setdefault(key, []).append(item)`\n- **Winner**: `max(scores, key=scores.get)` returns the key with the biggest value\n\nEach is one or two lines once you know it. Together they cover a huge share of data work."),
           Q("Which line counts occurrences safely?", ["counts[x] = counts.get(x, 0) + 1", "counts[x] += 1 with no setup", "counts = len(x)"], 0, "get supplies 0 the first time, so there is no KeyError.")],
          "Write `count_items(items)` (a dictionary of how often each item occurs), `group_by_length(words)` (a dictionary from word length to the list of words of that length) and `top_item(scores)` (the key with the biggest value). Print one result from each. It should print:\n\n<<OUT>>",
          "# count_items, group_by_length, top_item\n# print count_items([\"a\", \"b\", \"a\", \"c\", \"a\"]), group_by_length(<<vnames>>) and top_item(<<vstock>>)\n",
          'def count_items(items):\n    counts = {}\n    for item in items:\n        counts[item] = counts.get(item, 0) + 1\n    return counts\n\n\ndef group_by_length(words):\n    groups = {}\n    for word in words:\n        groups.setdefault(len(word), []).append(word)\n    return groups\n\n\ndef top_item(scores):\n    return max(scores, key=scores.get)\n\n\nprint(count_items(["a", "b", "a", "c", "a"]))\nprint(group_by_length(<<vnames>>))\nprint(top_item(<<vstock>>))\n',
          checks=[("ftest", "count_items", [[[["a", "b", "a"]], {"a": 2, "b": 1}]]), ("ftest", "top_item", [[[{"a": 3, "b": 9}], "b"]])],
          hints=["counts.get(item, 0) + 1 is the counting line.", "groups.setdefault(len(word), []) creates the list on first sight.", "max(scores, key=scores.get) picks the key with the largest value."], emoji="🏁")
