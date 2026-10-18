"""Chapter 9: Lists (16 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Lists")
    X = c.ctx
    VN, VL = X["vnames"], X["vl"]
    n1, n2, n3, n4 = X["n1"], X["n2"], X["n3"], X["n4"]
    q1, d = X["q1"], X["d"]

    c.add("intro_lists", "Introduction to Lists", "Lists", "hold many values in one list",
          [T("The scenario", "<<biz>> tracks four <<things>>. Four variables work, but forty would be a mess, and you could not loop over them or sort them. Programs hold groups of values in **lists**."),
           T("What a list is", "A **list** is an ordered collection in square brackets:\n\n```python\ncolours = [\"red\", \"green\", \"blue\"]\nprint(len(colours))     # 3\nprint(colours)          # ['red', 'green', 'blue']\n```\n\n- **Ordered**: items keep the position you gave them\n- **Any type**, and types can be mixed\n- **Changeable**: you can add, remove and replace items (the next lessons)"),
           T("Lists are everywhere", "A list of names, readings, prices, tickets, lines in a file. Almost every real program is a list plus a loop. Over this chapter you will learn to create, read, change, search, sort and copy them."),
           P('items = ["a", "b"]\nprint(len(items), items)', "2 ['a', 'b']", ["2 a b", "['a', 'b'] 2"], "len gives 2, and print shows a list with square brackets and quotes."),
           Q("What do square brackets around values create?", ["A list", "A tuple", "A dictionary"], 0, "Square brackets make a list. Round brackets make a tuple and curly braces a dictionary or set.")],
          "Create the project's two lists and describe them. Make `<<vnames>>` hold the four names and `counts` the four quantities, then print how many names there are, the names list and the counts list. It should print:\n\n<<OUT>>",
          "# <<vnames>> = the four names; counts = the four quantities\n# print len(<<vnames>>), then <<vnames>>, then counts\n",
          '<<vnames>> = <<nlist>>\ncounts = <<qlist>>\nprint(len(<<vnames>>))\nprint(<<vnames>>)\nprint(counts)\n',
          checks=[("var", VN), ("var", "counts")], hints=["Separate the items with commas inside square brackets.", "Text items need quotes, numbers do not."], emoji="📃")

    c.add("creating_lists", "Creating and Initializing Lists", "Creating", "create lists in several ways",
          [T("The scenario", "Sometimes you know the items. Sometimes you need a list of 12 zeros to count into, or the letters of a tag, or the numbers 1 to 5. Python has a short way for each."),
           T("Ways to create a list", "```python\nnames = [\"a\", \"b\"]          # literal\nempty = []                   # empty, to fill later\nzeros = [0] * 3              # [0, 0, 0]\nletters = list(\"abc\")        # ['a', 'b', 'c']\nnumbers = list(range(1, 6))  # [1, 2, 3, 4, 5]\nparts = \"x,y\".split(\",\")     # ['x', 'y']\n```\n\n`range` makes numbers and `list(...)` turns anything iterable into a list. `split` turns text into a list of pieces."),
           P("print([0] * 3, list(\"ab\"))", "[0, 0, 0] ['a', 'b']", ["[0, 0, 0] ab", "[0] ['a', 'b']"], "Multiplying a list repeats its items, and list(\"ab\") splits text into letters."),
           Q("Which creates the list [1, 2, 3]?", ["list(range(1, 4))", "list(range(1, 3))", "[1] * 3"], 0, "range stops before its end value, so range(1, 4) is 1, 2, 3.")],
          "Create five lists and print them in this order. It should print:\n\n<<OUT>>\n\n- `empty`: an empty list\n- `zeros`: four zeros made with `*`\n- `tag_letters`: the letters of `\"<<stag>>\"`\n- `first_five`: the numbers 1 to 5 using `range`\n- `parts`: `\"<<n1>>,<<n2>>\"` split on the comma",
          "# empty, zeros, tag_letters, first_five, parts: then print each one\n",
          'empty = []\nzeros = [0] * 4\ntag_letters = list("<<stag>>")\nfirst_five = list(range(1, 6))\nparts = "<<n1>>,<<n2>>".split(",")\nprint(empty)\nprint(zeros)\nprint(tag_letters)\nprint(first_five)\nprint(parts)\n',
          checks=[("var", "zeros"), ("var", "first_five"), ("var", "parts")], hints=["[0] * 4 repeats a one-item list four times.", "range(1, 6) ends before 6."], emoji="🧱")

    c.add("accessing_elements", "Accessing List Elements", "Reading items", "read items by position",
          [T("The scenario", "The first <<thing>> in the list is the one on today's front page, and the last is the newest. To use an item you must say **where** in the list it is."),
           T("Positions start at 0", "Square brackets after a list pick one item. Counting starts at **zero**:\n\n```python\nitems = [\"a\", \"b\", \"c\", \"d\"]\nprint(items[0])     # a   (first)\nprint(items[2])     # c\nprint(items[-1])    # d   (last)\nprint(items[-2])    # c   (second to last)\n```\n\nNegative numbers count from the end, so `-1` is always the last item."),
           T("Going too far", "Asking for a position that does not exist is an **IndexError**:\n\n```python\nitems[4]    # IndexError: list index out of range\n```\n\nA list of 4 items has positions 0 to 3. The last valid position is always `len(items) - 1`."),
           P('items = ["a", "b", "c"]\nprint(items[0], items[-1])', "a c", ["a b", "c a"], "Position 0 is the first item and -1 is the last."),
           Q("A list has 5 items. What is the last valid positive position?", ["4", "5", "6"], 0, "Positions run from 0 to 4 for 5 items.")],
          "Read items from `<<vnames>>` and print them, one per line: the first, the last, the item at position 2, and the second to last. It should print:\n\n<<OUT>>",
          "# print <<vnames>>[0], the last, position 2 and the second to last\n",
          'print(<<vnames>>[0])\nprint(<<vnames>>[-1])\nprint(<<vnames>>[2])\nprint(<<vnames>>[-2])\n',
          checks=[("prints", 4)], hints=["Use [-1] for the last item.", "Position 2 is the third item."], emoji="📍")

    c.add("list_indexing", "List Indexing", "Indexing", "find positions and use parallel lists",
          [T("The scenario", "Two lists stay in step: the names and their counts. Position 2 in one matches position 2 in the other. To look up the count of a named <<thing>> you first need its **position**."),
           T("index() and parallel lists", "`list.index(x)` returns the position of the first match (and raises ValueError if absent):\n\n```python\nnames = [\"a\", \"b\", \"c\"]\ncounts = [10, 20, 30]\npos = names.index(\"b\")     # 1\nprint(counts[pos])         # 20\n```\n\nLooping with positions uses `range(len(...))`:\n\n```python\nfor i in range(len(names)):\n    print(i, names[i], counts[i])\n```"),
           P('names = ["a", "b", "c"]\ncounts = [10, 20, 30]\nprint(counts[names.index("c")])', "30", ["2", "20"], "index(\"c\") is 2, so counts[2] is 30."),
           Q("What does names.index(\"z\") do when \"z\" is not in the list?", ["Raises a ValueError", "Returns -1", "Returns None"], 0, "index raises ValueError for a missing item. You will see safer ways to search soon.")],
          "Find the position of `\"<<n3>>\"` in `<<vnames>>`, print it and the matching count from `counts`. Then loop over the positions and print `position name count` for each. It should print:\n\n<<OUT>>",
          'counts = <<qlist>>\n# position = the index of "<<n3>>"; print position, then the matching count\n# then for each position print: position name count\n',
          'counts = <<qlist>>\nposition = <<vnames>>.index("<<n3>>")\nprint(position)\nprint(counts[position])\nfor i in range(len(<<vnames>>)):\n    print(i, <<vnames>>[i], counts[i])\n',
          checks=[("var", "position", True)], hints=["position = <<vnames>>.index(\"<<n3>>\")", "Inside the loop use <<vnames>>[i] and counts[i]."], emoji="🧭")

    c.add("list_slicing", "List Slicing", "Slicing", "take parts of a list with slices",
          [T("The scenario", "The morning briefing needs only the three newest readings; the audit needs every other one; the chart needs them reversed. Slices cut a list into pieces without a loop."),
           T("The slice syntax", "`items[start:stop:step]` gives a **new list**. The start is included and the stop is not.\n\n```python\nn = [10, 20, 30, 40, 50]\nprint(n[1:4])      # [20, 30, 40]\nprint(n[:2])       # [10, 20]\nprint(n[-2:])      # [40, 50]\nprint(n[::2])      # [10, 30, 50]\nprint(n[::-1])     # [50, 40, 30, 20, 10]\n```\n\nAny part may be left out. Slices never raise IndexError: an over-long slice just stops at the end."),
           P("n = [1, 2, 3, 4, 5]\nprint(n[1:3], n[-2:])", "[2, 3] [4, 5]", ["[1, 2, 3] [4, 5]", "[2, 3] [3, 4]"], "[1:3] takes positions 1 and 2. [-2:] takes the last two."),
           Q("What does n[::-1] give?", ["The list reversed", "The first item only", "An error"], 0, "A step of -1 walks the list backwards.")],
          "Slice the five readings into five new lists, and print each in order. It should print:\n\n<<OUT>>\n\n`first_three`, `last_two`, `middle` (positions 1 to 3), `backwards` and `every_other`.",
          "readings = <<sreads>>\n# first_three, last_two, middle (positions 1 to 3), backwards, every_other\n# print each one\n",
          'readings = <<sreads>>\nfirst_three = readings[:3]\nlast_two = readings[-2:]\nmiddle = readings[1:4]\nbackwards = readings[::-1]\nevery_other = readings[::2]\nprint(first_three)\nprint(last_two)\nprint(middle)\nprint(backwards)\nprint(every_other)\n',
          checks=[("var", "first_three"), ("var", "middle"), ("var", "every_other")], hints=["readings[1:4] stops before position 4.", "Step 2 takes every second item starting at 0."], emoji="🔪")

    c.add("modifying_elements", "Modifying List Elements", "Changing items", "change items in place",
          [T("The scenario", "A delivery of <<d>> arrives for the first <<thing>>, and the second is withdrawn completely. The list has to be **updated**, not rebuilt. Lists are mutable: you can change them in place."),
           T("Assign to a position", "```python\ncounts = [10, 20, 30]\ncounts[0] = 15          # replace\ncounts[1] += 5          # update using the old value\nprint(counts)           # [15, 25, 30]\n```\n\nA position must already exist: you cannot assign to `counts[5]` in a 3-item list. Slices can be assigned too: `counts[1:3] = [0, 0]`."),
           T("Strings cannot", "Text is **immutable**: `name[0] = \"X\"` raises a TypeError, and you build a new string instead. Lists and (later) dictionaries are the changeable ones. This difference matters when you pass them to functions."),
           P("counts = [10, 20, 30]\ncounts[0] = 15\ncounts[1] += 5\nprint(counts)", "[15, 25, 30]", ["[10, 25, 30]", "[15, 20, 30]"], "Both lines change the list in place."),
           Q("Which of these can be changed in place?", ["A list", "A string", "A number"], 0, "Lists are mutable. Strings and numbers are not.")],
          "Start from `counts = <<qlist>>`. Add the delivery of <<d>> to the first count, set the second count to 0, and double the last count. Print `counts` after each of the three changes. It should print:\n\n<<OUT>>",
          "counts = <<qlist>>\n# three changes, printing counts after each: add <<d>> to the first, set the second to 0, double the last\n",
          'counts = <<qlist>>\ncounts[0] += <<d>>\nprint(counts)\ncounts[1] = 0\nprint(counts)\ncounts[-1] *= 2\nprint(counts)\n',
          checks=[("var", "counts")], hints=["counts[0] += <<d>> adds to the first item.", "counts[-1] *= 2 doubles the last one."], emoji="✏️")

    c.add("append_insert", "Adding Elements with append() and insert()", "Adding items", "grow a list with append, insert and extend",
          [T("The scenario", "New <<things>> arrive all the time. A list that cannot grow would be useless. Python gives you three ways to add: at the end, at a chosen position, or a whole batch."),
           T("Three ways to add", "```python\nq = [\"b\"]\nq.append(\"c\")            # ['b', 'c']      add one to the end\nq.insert(0, \"a\")          # ['a', 'b', 'c']  add at position 0\nq.extend([\"d\", \"e\"])      # ['a','b','c','d','e']  add many\nq = q + [\"f\"]             # a + joins and makes a new list\n```\n\n`append` and `insert` add **one** item. Appending a list adds the list as a single item, which surprises people: use `extend` to add its items."),
           P("a = [1]\na.append([2, 3])\nprint(a)", "[1, [2, 3]]", ["[1, 2, 3]", "[[2, 3]]"], "append adds its argument as one item, even if it is a list. extend would have added 2 and 3 separately."),
           Q("Which adds several items from another list?", ["extend", "append", "insert"], 0, "extend adds each item. append adds the whole thing as one item.")],
          "Build a queue from nothing and print it after each of the five steps. It should print:\n\n<<OUT>>\n\nStart with `queue = []`, append `\"<<n1>>\"`, append `\"<<n2>>\"`, insert `\"<<n3>>\"` at position 0, extend with `[\"<<n4>>\", \"<<n1>>\"]`.",
          'queue = []\nprint(queue)\n# append "<<n1>>", print; append "<<n2>>", print; insert "<<n3>>" at 0, print; extend with the two names, print\n',
          'queue = []\nprint(queue)\nqueue.append("<<n1>>")\nprint(queue)\nqueue.append("<<n2>>")\nprint(queue)\nqueue.insert(0, "<<n3>>")\nprint(queue)\nqueue.extend(["<<n4>>", "<<n1>>"])\nprint(queue)\n',
          checks=[("var", "queue")], hints=["queue.insert(0, name) puts it at the front.", "extend takes a list of names."], emoji="➕")

    c.add("removing_elements", "Removing Elements from Lists", "Removing items", "remove items by value and by position",
          [T("The scenario", "Items leave the list too: a duplicate entry, the oldest reading, a <<thing>> that is discontinued. Python can remove by **value** or by **position**."),
           T("Four ways to remove", "```python\nitems = [\"a\", \"b\", \"c\", \"b\"]\nitems.remove(\"b\")     # removes the FIRST \"b\"   -> ['a','c','b']\nlast = items.pop()    # removes and returns the last -> 'b'\nfirst = items.pop(0)  # by position -> 'a'\ndel items[0]          # by position, returns nothing\nitems.clear()         # empties the list\n```\n\n`remove` raises a ValueError if the value is absent, and `pop` raises an IndexError on an empty list."),
           P('x = ["a", "b", "a"]\nx.remove("a")\nprint(x)', "['b', 'a']", ["['b']", "['a', 'b']"], "remove deletes only the first matching item."),
           Q("What does pop() return?", ["The item it removed", "The list", "Nothing"], 0, "pop removes the item and gives it back, so you can use it.")],
          "Start with `items = [\"<<n1>>\", \"<<n2>>\", \"<<n3>>\", \"<<n4>>\", \"<<n2>>\"]`. Remove the **first** `\"<<n2>>\"`, pop the last item into `popped`, then delete the item at position 0. Print `items` after each step, and `popped` at the end. It should print:\n\n<<OUT>>",
          'items = ["<<n1>>", "<<n2>>", "<<n3>>", "<<n4>>", "<<n2>>"]\n# remove the first "<<n2>>", pop the last into popped, del position 0; print items after each; print popped last\n',
          'items = ["<<n1>>", "<<n2>>", "<<n3>>", "<<n4>>", "<<n2>>"]\nitems.remove("<<n2>>")\nprint(items)\npopped = items.pop()\nprint(items)\ndel items[0]\nprint(items)\nprint(popped)\n',
          checks=[("var", "items"), ("var", "popped")], hints=["items.remove(\"<<n2>>\") only removes the first one.", "popped = items.pop() removes the last item and keeps it."], emoji="➖")

    c.add("list_methods", "List Methods", "Methods", "use the main list methods",
          [T("The scenario", "Counting how often a reading occurs, putting values in order, finding where the highest sits: the list type already knows how. A method is a function attached to a value, called with a dot."),
           T("The main methods", "```python\nn = [3, 1, 4, 1, 5]\nn.count(1)       # 2\nn.index(4)       # 2\nn.sort()         # n is now [1, 1, 3, 4, 5]\nn.reverse()      # n is now [5, 4, 3, 1, 1]\nm = n.copy()     # a separate copy\n```\n\nBuilt-ins that work on lists: `len`, `sum`, `min`, `max`, `sorted`. Notice that `sort`, `reverse`, `append` and `remove` **change the list and return None**: writing `x = x.sort()` sets x to None."),
           P("n = [3, 1, 2]\nx = n.sort()\nprint(x, n)", "None [1, 2, 3]", ["[1, 2, 3] [1, 2, 3]", "None [3, 1, 2]"], "sort changes n in place and returns None."),
           Q("What does list.sort() return?", ["None", "The sorted list", "The original list"], 0, "Methods that change a list in place return None. Use sorted() for a new list.")],
          "Use the list methods on `numbers`. Print five lines: how often 5 occurs, where 4 sits, then the list after `sort()`, after `reverse()`, and the sum and length together. It should print:\n\n<<OUT>>",
          "numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]\n# count of 5, index of 4; sort and print; reverse and print; print sum and len\n",
          'numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]\nprint(numbers.count(5))\nprint(numbers.index(4))\nnumbers.sort()\nprint(numbers)\nnumbers.reverse()\nprint(numbers)\nprint(sum(numbers), len(numbers))\n',
          checks=[("var", "numbers")], hints=["Print count and index directly: print(numbers.count(5)).", "Do not write x = numbers.sort()."], emoji="🧰")

    c.add("iterating_lists", "Iterating Through Lists", "Walking a list", "loop over lists, with positions and in pairs",
          [T("The scenario", "The daily report must walk through every name and its count together. There are several ways to walk a list, and each one fits a different job."),
           T("Ways to loop", "```python\nnames = [\"a\", \"b\"]\ncounts = [10, 20]\nfor n in names:                       # items only\n    print(n)\nfor i, n in enumerate(names, 1):      # position and item\n    print(i, n)\nfor n, c in zip(names, counts):       # two lists in step\n    print(n, c)\n```\n\n`enumerate` numbers the items and `zip` pairs lists up. `zip` stops at the shorter list."),
           T("Do not change while looping", "Adding or removing items from a list **while looping over it** skips items and causes strange bugs. Build a **new** list instead, or loop over a copy."),
           P('for i, x in enumerate(["a", "b"], 1):\n    print(i, x)', "1 a\n2 b", ["0 a\n1 b", "a\nb"], "enumerate with a start of 1 numbers the items from 1."),
           Q("What does zip(names, counts) do?", ["Pairs each name with its count", "Joins the lists into one", "Sorts both lists"], 0, "zip walks both lists together and gives one pair at a time.")],
          "Print the report with `zip` and `enumerate`. It should print:\n\n<<OUT>>\n\nEach line is `number. name: count`. Use `counts = <<qlist>>` and your `<<vnames>>` list.",
          'counts = <<qlist>>\n# for each name and count (numbered from 1), print: number. name: count\n',
          'counts = <<qlist>>\nfor number, (name, count) in enumerate(zip(<<vnames>>, counts), 1):\n    print(f"{number}. {name}: {count}")\n',
          checks=[("ast", "For", "a for loop")], hints=["for number, (name, count) in enumerate(zip(a, b), 1): works, or use a loop over range(len(...)).", "Use an f-string: f\"{number}. {name}: {count}\""], emoji="🚶")

    c.add("list_search", "List Membership and Searching", "Searching", "check membership and search a list",
          [T("The scenario", "A customer asks whether you carry a <<thing>>. The <<system>> must answer yes or no, and if yes, where it is. Searching a list is one of the most common tasks in programming."),
           T("in and manual search", "`in` answers yes or no:\n\n```python\nif \"b\" in [\"a\", \"b\"]:\n    print(\"found\")\n```\n\nFor the **position**, a linear search walks the list and returns when it finds the target, or `-1` when it does not:\n\n```python\ndef find_position(items, target):\n    for i in range(len(items)):\n        if items[i] == target:\n            return i\n    return -1\n```\n\n`return` inside the loop stops the search the moment it succeeds."),
           P('print("b" in ["a", "b"], "z" in ["a", "b"])', "True False", ["b z", "True True"], "`in` gives a boolean for each test."),
           Q("Why does find_position return -1 for a missing item?", ["-1 can never be a real position", "Python requires it", "It is faster"], 0, "A real position is 0 or more, so -1 safely means \"not found\".")],
          "Write `find_position(items, target)` that returns the position of `target` or `-1`. Then use it on `<<vnames>>` for `\"<<n3>>\"` and for `\"<<missing>>\"`, and print `\"<<n2>>\" in <<vnames>>`. It should print:\n\n<<OUT>>",
          "# find_position(items, target): loop with range(len(items)) and return the position, or -1\n# print find_position(<<vnames>>, \"<<n3>>\"), find_position(<<vnames>>, \"<<missing>>\"), then \"<<n2>>\" in <<vnames>>\n",
          'def find_position(items, target):\n    for i in range(len(items)):\n        if items[i] == target:\n            return i\n    return -1\n\n\nprint(find_position(<<vnames>>, "<<n3>>"))\nprint(find_position(<<vnames>>, "<<missing>>"))\nprint("<<n2>>" in <<vnames>>)\n',
          checks=[("ftest", "find_position", [[[[n1, n2, n3, n4], n3], 2], [[[n1, n2, n3, n4], "zzz"], -1]])], hints=["return i inside the if, and return -1 after the loop.", "The return -1 must be outside (after) the loop."], emoji="🔎")

    c.add("sorting_reversing", "Sorting and Reversing Lists", "Sorting", "sort lists in different ways",
          [T("The scenario", "Reports are easier to read in order: names A to Z, biggest stock first, shortest names on top. Python can sort any list, and `key` lets you choose **what to sort by**."),
           T("sort and sorted", "```python\nn = [3, 1, 2]\nprint(sorted(n))                 # [1, 2, 3]  new list, n unchanged\nn.sort(reverse=True)             # in place, descending\nwords = [\"ccc\", \"a\", \"bb\"]\nprint(sorted(words, key=len))    # ['a', 'bb', 'ccc']\n```\n\n- `sorted(x)` returns a **new** list. `x.sort()` changes x\n- `reverse=True` sorts descending\n- `key` is a function applied to each item to decide the order, often a `lambda`"),
           P('print(sorted(["bb", "a", "ccc"], key=len, reverse=True))', "['ccc', 'bb', 'a']", ["['a', 'bb', 'ccc']", "['ccc', 'a', 'bb']"], "Sorting by length, longest first."),
           Q("Which leaves the original list unchanged?", ["sorted(x)", "x.sort()", "x.reverse()"], 0, "sorted builds a new list. The methods change the list itself.")],
          "Sort the project data three ways, and print each. It should print:\n\n<<OUT>>\n\n- `by_length`: the names sorted by length (shortest first)\n- `by_count`: the names sorted by their count, biggest first (use `key=lambda name: counts[<<vnames>>.index(name)]`)\n- `reversed_names`: the names in reverse order using `reversed`",
          "counts = <<qlist>>\n# by_length, by_count (biggest count first), reversed_names = list(reversed(<<vnames>>)); print each\n",
          'counts = <<qlist>>\nby_length = sorted(<<vnames>>, key=len)\nby_count = sorted(<<vnames>>, key=lambda name: counts[<<vnames>>.index(name)], reverse=True)\nreversed_names = list(reversed(<<vnames>>))\nprint(by_length)\nprint(by_count)\nprint(reversed_names)\n',
          checks=[("var", "by_count"), ("var", "reversed_names")], hints=["sorted(names, key=len) sorts by length.", "reverse=True puts the biggest first."], emoji="📶")

    c.add("list_comprehensions", "List Comprehensions", "Comprehensions", "build lists with comprehensions",
          [T("The scenario", "Build a list from another list: the distances from target, only the low items, the names in capitals. Doing it with a loop and `append` takes four lines. A **comprehension** does it in one."),
           T("The pattern", "```python\nnums = [1, 2, 3, 4]\ndoubled = [n * 2 for n in nums]            # [2, 4, 6, 8]\nevens = [n for n in nums if n % 2 == 0]   # [2, 4]\n```\n\nRead it left to right: *\"give me `n * 2` for each `n` in `nums`\"*, and with `if`, *\"but only when the test is true\"*. The result is always a **new** list."),
           T("When not to", "If the comprehension needs two conditions, nested loops or more than about 70 characters, write the plain loop. Clear beats clever."),
           P("print([n * n for n in range(4)])", "[0, 1, 4, 9]", ["[1, 4, 9, 16]", "[0, 1, 2, 3]"], "range(4) is 0, 1, 2, 3, and each is squared."),
           Q("What does [n for n in nums if n > 2] do?", ["Keeps only items bigger than 2", "Doubles every item", "Removes items bigger than 2"], 0, "The if at the end is a filter.")],
          "Write three comprehensions and print each. It should print:\n\n<<OUT>>\n\n- `distances`: for each reading, its distance from <<starget>> (use `abs`)\n- `shouting`: each name in capital letters (`.upper()`)\n- `low_names`: the names whose count is at or below `<<vl>>` (use `zip`)",
          "readings = <<sreads>>\ncounts = <<qlist>>\n# distances, shouting, low_names: one comprehension each, then print them\n",
          'readings = <<sreads>>\ncounts = <<qlist>>\ndistances = [abs(r - <<starget>>) for r in readings]\nshouting = [name.upper() for name in <<vnames>>]\nlow_names = [name for name, count in zip(<<vnames>>, counts) if count <= <<vl>>]\nprint(distances)\nprint(shouting)\nprint(low_names)\n',
          checks=[("ast", "ListComp", "a list comprehension"), ("var", "distances"), ("var", "low_names")], hints=["[abs(r - target) for r in readings]", "Filter with if count <= <<vl>> at the end."], emoji="⚡")

    c.add("nested_lists", "Nested Lists", "Lists of lists", "work with lists of lists",
          [T("The scenario", "A table has rows and columns: each row holds a name, a count and a rate. A list can hold other lists as items, which is how programs store grids, tables and spreadsheets."),
           T("Rows and columns", "```python\ngrid = [[1, 2, 3],\n        [4, 5, 6]]\nprint(grid[1])        # [4, 5, 6]   a whole row\nprint(grid[1][2])     # 6           row 1, column 2\ngrid[0][0] = 9        # change one cell\n```\n\nThe **first** index chooses the row, the **second** chooses the item inside it. Loop over rows, then over items for a full walk."),
           P("grid = [[1, 2], [3, 4]]\nprint(grid[1][0], len(grid))", "3 2", ["1 2", "2 2"], "grid[1] is [3, 4], and its position 0 is 3. The grid has 2 rows."),
           Q("In grid[2][0], what does the 2 choose?", ["The row", "The column", "The value"], 0, "The first index picks the row.")],
          "Build `table` with one row per <<thing>>: `[name, count, rate]`, using `zip` over `<<vnames>>`, `counts` and `prices`. Then print the first row, the count in the third row, and the total value (count times rate, added up over all rows). It should print:\n\n<<OUT>>",
          "counts = <<qlist>>\nprices = <<plist>>\n# table = a list of [name, count, rate] rows (a comprehension with zip works well)\n# print table[0], table[2][1] and the total value\n",
          'counts = <<qlist>>\nprices = <<plist>>\ntable = [[name, count, rate] for name, count, rate in zip(<<vnames>>, counts, prices)]\nprint(table[0])\nprint(table[2][1])\nprint(sum([row[1] * row[2] for row in table]))\n',
          checks=[("var", "table"), ("var", "prices")], hints=["[[a, b, c] for a, b, c in zip(x, y, z)]", "row[1] * row[2] is count times rate."], emoji="🧮")

    c.add("copying_lists", "Copying Lists", "Copies", "copy a list safely",
          [T("The scenario", "A teammate \"copies\" the stock list to try out a what-if, and the **real** list changes too. Nothing crashes, the numbers are just wrong. It is the most famous list bug, and it comes from how assignment works."),
           T("Assignment does not copy", "```python\na = [1, 2, 3]\nb = a            # NOT a copy: both names point to the SAME list\nb.append(4)\nprint(a)         # [1, 2, 3, 4]\n```\n\nTo get a real, separate copy:\n\n```python\nb = a.copy()     # or a[:] or list(a)\n```"),
           T("Shallow vs deep", "`copy()` makes a **shallow** copy: the outer list is new, but any lists *inside* are still shared. For nested lists use `copy.deepcopy(a)` after `import copy`."),
           P("a = [1, 2]\nb = a\nb.append(3)\nprint(a)", "[1, 2, 3]", ["[1, 2]", "[3]"], "b and a are the same list, so the append shows through a."),
           Q("Which line makes a separate copy of a list?", ["b = a.copy()", "b = a", "b == a"], 0, "Plain assignment shares the list. copy() makes a new one.")],
          "The what-if code changes the real stock because `scenario = stock` shares the list. Fix it so `stock` stays as it was. It should print:\n\n<<OUT>>",
          'stock = <<qlist>>\nscenario = stock\nscenario[0] += <<d>>\nscenario.append(0)\nprint("Real stock:", stock)\nprint("What-if:", scenario)\n',
          'stock = <<qlist>>\nscenario = stock.copy()\nscenario[0] += <<d>>\nscenario.append(0)\nprint("Real stock:", stock)\nprint("What-if:", scenario)\n',
          checks=[("var", "stock")], hints=["A copy is made with stock.copy().", "Change only the line that creates scenario."], emoji="📑")

    c.add("common_list_operations", "Common List Operations", "Chapter 9 project", "combine list skills into reusable helpers",
          [T("The scenario", "Real list code keeps needing the same helpers: remove duplicates, split into groups, flatten a table. You will write three of them and keep them for the rest of the course."),
           T("Three classics", "- **unique** removes repeats and keeps the first-seen order\n- **chunk** splits a list into pieces of a given size\n- **flatten** turns a list of lists into one list\n\nEach is a small loop plus `append`, or a comprehension. You will also meet them again under different names in later chapters."),
           T("Build, then test", "Write each as a function that **returns** a new list. Test it on a tiny input you can check by hand, such as `chunk([1, 2, 3, 4, 5], 2)`. If it works on small cases, it will work on big ones."),
           Q("What does chunk([1, 2, 3, 4, 5], 2) give?", ["[[1, 2], [3, 4], [5]]", "[[1, 2], [3, 4]]", "[1, 2, 3, 4, 5]"], 0, "The last piece may be shorter.")],
          "Write `unique(items)`, `chunk(items, size)` and `flatten(nested)`, then print one result from each. It should print:\n\n<<OUT>>",
          "# unique keeps first-seen order; chunk splits into pieces of size; flatten joins a list of lists\n# print unique([3, 1, 3, 2, 1]), chunk([1, 2, 3, 4, 5], 2) and flatten([[1, 2], [3], [4, 5]])\n",
          'def unique(items):\n    result = []\n    for item in items:\n        if item not in result:\n            result.append(item)\n    return result\n\n\ndef chunk(items, size):\n    return [items[i:i + size] for i in range(0, len(items), size)]\n\n\ndef flatten(nested):\n    return [item for row in nested for item in row]\n\n\nprint(unique([3, 1, 3, 2, 1]))\nprint(chunk([1, 2, 3, 4, 5], 2))\nprint(flatten([[1, 2], [3], [4, 5]]))\n',
          checks=[("ftest", "unique", [[[[3, 1, 3, 2, 1]], [3, 1, 2]]]), ("ftest", "chunk", [[[[1, 2, 3, 4, 5], 2], [[1, 2], [3, 4], [5]]]]), ("ftest", "flatten", [[[[[1, 2], [3], [4, 5]]], [1, 2, 3, 4, 5]]])],
          hints=["unique: only append an item if it is not already in the result.", "chunk: a slice starting at i of length size, for i in range(0, len(items), size).", "flatten: two for clauses in a comprehension, row then item."], emoji="🏁")
