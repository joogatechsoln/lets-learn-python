"""Chapter 7: Comparisons (12 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Comparisons")
    X = c.ctx
    VL, VQ, level, q1, q2 = X["vl"], X["vq"], X["level"], X["q1"], X["q2"]

    c.add("intro_comparisons", "Introduction to Comparison Operators", "Comparing", "compare values with six operators",
          [T("The scenario", "<<rule>> A program can only follow a rule like that if it can **compare** numbers and get a yes or a no. Comparisons are how code makes decisions."),
           T("Six operators", "A comparison gives back a `bool`: `True` or `False`.\n\n- `==` equal to\n- `!=` not equal to\n- `<` less than, `>` greater than\n- `<=` less than or equal, `>=` greater than or equal\n\n```python\nprint(5 > 3)     # True\nprint(5 == 6)    # False\nprint(5 != 6)    # True\n```"),
           T("Answers, not actions", "A comparison does not *do* anything by itself. It **evaluates to a value** you can print, store in a variable, or use to decide what to run next. That last use arrives in this chapter."),
           P("print(5 > 3, 5 == 6, 5 != 6)", "True False True", ["True True True", "False False True"], "5 > 3 is true, 5 == 6 is false, and 5 != 6 is true."),
           Q("What type does `5 > 3` give back?", ["bool", "int", "str"], 0, "Every comparison evaluates to True or False, which is a bool.")],
          "Compare <<q1>> with <<q2>> using all six operators, one print line each, in this order: `==`, `!=`, `<`, `>`, `<=`, `>=`. It should print:\n\n<<OUT>>",
          "# six print lines comparing <<q1>> with <<q2>>\n",
          "print(<<q1>> == <<q2>>)\nprint(<<q1>> != <<q2>>)\nprint(<<q1>> < <<q2>>)\nprint(<<q1>> > <<q2>>)\nprint(<<q1>> <= <<q2>>)\nprint(<<q1>> >= <<q2>>)\n",
          checks=[("prints", 6)], hints=["print(<<q1>> == <<q2>>) is the first line.", "Change only the operator for the next five."], emoji="⚖️")

    c.add("equality", "Equality and Inequality", "== and !=", "tell = from == and compare safely",
          [T("The scenario", "The most common comparison bug in the world is a single missing character: typing `=` where `==` was meant. Three lines in the <<system>> have that bug or its cousins."),
           T("= stores, == compares", "- `=` **assigns**: `units = 5`\n- `==` **compares**: `units == 5` is `True`\n\nIn a print call, `print(units = 5)` is a `TypeError`, because Python thinks you are naming a keyword argument."),
           T("Equal does not mean the same type", "`5 == 5.0` is `True` (the same number), but `\"5\" == 5` is `False` (text is not a number). And never use `==` on computed floats: `0.1 + 0.2 == 0.3` is `False`. Round first."),
           P('print(5 == 5.0, "5" == 5)', "True False", ["False False", "True True"], "5 and 5.0 are the same number, but text and a number are never equal."),
           Q("Which line compares two values?", ["x == 5", "x = 5", "x := 5 is not allowed here"], 0, "== compares. A single = assigns.")],
          "Three lines should each print `True`, but they do not. Fix them:\n\n- the first mixes up `=` and `==`\n- the second compares a number with text\n- the third compares computed floats\n\nIt should print:\n\n<<OUT>>",
          'units = <<q1>>\nprint(units = <<q1>>)\nprint(units == "<<q1>>")\nprint(0.1 + 0.2 == 0.3)\n',
          'units = <<q1>>\nprint(units == <<q1>>)\nprint(str(units) == "<<q1>>")\nprint(round(0.1 + 0.2, 2) == 0.3)\n',
          hints=["The first line needs ==.", "Turn the number into text with str() before comparing with text, or compare numbers with numbers.", "round(value, 2) removes the tiny error."], emoji="🟰")

    c.add("greater_less", "Greater Than and Less Than", "Ordering", "compare with <, <=, >, >=",
          [T("The scenario", "Whether the rule fires at **exactly** the limit is the question that causes the most arguments in real systems. Boundaries decide who gets a refund, which truck leaves, which ticket breaches. Today you set the rule number for <<biz>> and check where it bites."),
           T("Strict and inclusive", "- `<` and `>` are **strict**: the boundary value does *not* count\n- `<=` and `>=` are **inclusive**: the boundary *does* count\n\n```python\nlimit = 10\nprint(10 <= limit)    # True\nprint(10 < limit)     # False\n```"),
           T("Test the edges", "For any limit, always check three values: **just below**, **exactly on**, and **just above**. If you only test 3 and 50 against a limit of 10, an off-by-one mistake slips through."),
           P("limit = 10\nprint(9 <= limit, 10 <= limit, 11 <= limit)", "True True False", ["True False False", "True True True"], "<= includes the boundary, so 10 <= 10 is True."),
           Q("Which operator includes the boundary value?", ["<=", "<", ">"], 0, "<= and >= are inclusive. < and > are strict.")],
          "Set the rule number and apply it. Create `<<vl>> = <<level>>`, then print `<<vq>> <= <<vl>>`-style results for the four starting quantities (<<q1>>, <<q2>>, <<q3>>, <<q4>>) against `<<vl>>`, then two **boundary** checks: whether `<<vl>> <= <<vl>>`, and whether `<<vl>> + 1 <= <<vl>>`. It should print:\n\n<<OUT>>",
          "# <<vl>> = <<level>>\n# four lines: each quantity <= <<vl>>, then the two boundary checks\n",
          "<<vl>> = <<level>>\nprint(<<q1>> <= <<vl>>)\nprint(<<q2>> <= <<vl>>)\nprint(<<q3>> <= <<vl>>)\nprint(<<q4>> <= <<vl>>)\nprint(<<vl>> <= <<vl>>)\nprint(<<vl>> + 1 <= <<vl>>)\n",
          checks=[("var", VL)], hints=["Start with the line <<vl>> = <<level>>.", "The two boundary lines use <<vl>> itself."], emoji="📏")

    c.add("comparing_strings", "Comparing Strings", "Text order", "compare text by case and alphabet",
          [T("The scenario", "Names sometimes arrive as `maize flour`, `Maize flour` or `MAIZE FLOUR`. To a person they match. To Python they are three different strings. Comparing text safely takes a little care."),
           T("How text is compared", "- `==` needs **exactly** the same characters, including capitals and spaces\n- `<` and `>` compare **dictionary-style, character by character**, using character codes. All **capitals come before lowercase** letters\n- Digits in text compare as characters: `\"10\" < \"9\"` is `True` because `\"1\"` comes before `\"9\"`"),
           T("Compare like with like", "To ignore case, convert both sides first with `.lower()`, and strip stray spaces with `.strip()`:\n\n```python\nname.strip().lower() == \"maize flour\"\n```"),
           P('print("apple" < "banana", "Zebra" < "apple", "10" < "9")', "True True True", ["True False False", "False True True"], "Capitals sort before lowercase, and text digits compare character by character."),
           Q("Why is \"10\" < \"9\" True?", ["Text is compared character by character, and \"1\" comes before \"9\"", "10 is smaller than 9", "Python is wrong"], 0, "For numeric order you must convert the text to numbers first.")],
          "Print five comparisons, one per line: `\"apple\" < \"banana\"`, `\"Zebra\" < \"apple\"`, `\"10\" < \"9\"`, whether `\"<<n1>>\"` equals its own `.lower()`, and whether `\"<<n1>>\".lower()` equals `\"<<n1_lower>>\"`. It should print:\n\n<<OUT>>",
          "# five print lines, as in the task\n",
          'print("apple" < "banana")\nprint("Zebra" < "apple")\nprint("10" < "9")\nprint("<<n1>>" == "<<n1>>".lower())\nprint("<<n1>>".lower() == "<<n1_lower>>")\n',
          checks=[("prints", 5)], hints=["\"text\".lower() returns the lowercase version.", "Compare each pair with the right operator."], emoji="🔤")

    c.add("different_types", "Comparing Different Data Types", "Mixed types", "compare across types safely",
          [T("The scenario", "A comparison that works with numbers can crash with text. The rule of thumb: **convert first, compare second**."),
           T("What Python allows", "- `int` and `float` compare happily: `5 == 5.0`\n- `bool` is a number: `True == 1` is `True`\n- `==` between **unrelated types is just `False`**: `\"5\" == 5`\n- `<` and `>` between unrelated types is a `TypeError`: `\"5\" < 7`"),
           T("The safe habit", "```python\nint(\"5\") < 7        # convert text to a number first\n```\n\nWhen data comes from outside (a form, a file, a feed) it is text until you convert it. Convert at the door, and your comparisons stay simple."),
           P('print(5 == 5.0, "5" == 5, True == 1)', "True False True", ["True True True", "False False False"], "Numbers equal across int and float, text never equals a number, and True counts as 1."),
           Q("What does \"5\" < 7 do?", ["Raises a TypeError", "Gives True", "Gives False"], 0, "Python refuses to order text against a number.")],
          "Four comparisons are below, and the third crashes with a `TypeError`. Fix it so the program prints:\n\n<<OUT>>",
          'print(5 == 5.0)\nprint("5" == 5)\nprint("5" < 7)\nprint(True == 1)\n',
          'print(5 == 5.0)\nprint("5" == 5)\nprint(int("5") < 7)\nprint(True == 1)\n',
          hints=["The text \"5\" must become a number before it can be ordered against 7.", "int(\"5\") converts it."], emoji="🔀")

    c.add("booleans_if", "Boolean Values", "Booleans and if", "use booleans to make decisions with if",
          [T("The scenario", "<<rule>> Now that you can compare, the <<system>> can finally **act on** the answer. Booleans are what decisions are made of."),
           T("bool", "`True` and `False` (capital first letter) are the only two bool values. Store a comparison in a variable and give it a good name:\n\n```python\nis_low = units <= limit\n```\n\nNames that start with `is_`, `has_` or `needs_` make code read like English."),
           T("if / else", "An **if statement** runs code only when a condition is True:\n\n```python\nif is_low:\n    print(\"Reorder\")\nelse:\n    print(\"Fine\")\n```\n\nThe condition ends with a colon, and the lines that belong to it are **indented**. `else` runs when the condition is False. Add `elif` for extra cases."),
           P("x = 5\nif x > 3:\n    print(\"big\")\nelse:\n    print(\"small\")", "big", ["small", "big\nsmall"], "5 > 3 is True, so only the if branch runs."),
           Q("What does the else branch run on?", ["When the condition is False", "Always", "When the program has an error"], 0, "else is the \"otherwise\" branch.")],
          "Apply the rule to the first <<thing>>. If `<<vq>> <= <<vl>>`, print `<<msg_le_f>>`. Otherwise print `<<msg_gt_f>>`. It should print:\n\n<<OUT>>",
          "# if <<vq>> is at or below <<vl>>, print the first message\n# otherwise print the second message\n",
          'if <<vq>> <= <<vl>>:\n    print("<<msg_le_f>>")\nelse:\n    print("<<msg_gt_f>>")\n',
          checks=[("ast", "If", "an if statement")], hints=["The condition is <<vq>> <= <<vl>>", "Remember the colon and the indentation under if and else."], emoji="🚦")

    c.add("logical_operators", "Logical Operators: and, or, and not", "and / or / not", "combine conditions with and, or, not",
          [T("The scenario", "A <<thing>> should be reordered only when it is low **and** no order has been placed yet. Real rules mix several yes-or-no facts, and logical operators join them."),
           T("Three operators", "- `A and B`: True only if **both** are True\n- `A or B`: True if **at least one** is True\n- `not A`: flips True and False\n\n| A | B | A and B | A or B |\n|---|---|---|---|\n| T | T | T | T |\n| T | F | F | T |\n| F | T | F | T |\n| F | F | F | F |"),
           T("Short-circuit", "Python stops as soon as the answer is known: in `A and B`, if A is False it never looks at B. In `A or B`, if A is True it skips B. This is useful for guarding risky checks, and sometimes the cause of surprises."),
           P("print(True and False, True or False, not True)", "False True False", ["True True False", "False False True"], "and needs both, or needs one, and not flips."),
           Q("When is `A or B` False?", ["Only when both are False", "When either is False", "Never"], 0, "or is True unless both sides are False.")],
          "Create `is_low = <<q2>> <= <<vl>>` and `order_placed = False`. Then print four lines: `needs_order` (low **and** not ordered), `is_low or order_placed`, `not is_low`, and `is_low and order_placed`. It should print:\n\n<<OUT>>",
          "is_low = <<q2>> <= <<vl>>\norder_placed = False\n# needs_order = is_low and not order_placed\n# then print needs_order and the three other expressions\n",
          'is_low = <<q2>> <= <<vl>>\norder_placed = False\nneeds_order = is_low and not order_placed\nprint(needs_order)\nprint(is_low or order_placed)\nprint(not is_low)\nprint(is_low and order_placed)\n',
          checks=[("var", "needs_order", True)], hints=["needs_order = is_low and not order_placed", "Print each of the four values on its own line."], emoji="🔗")

    c.add("combining_comparisons", "Combining Comparison Expressions", "Tiers", "write multi-way decisions",
          [T("The scenario", "Two answers (reorder or not) are rarely enough. <<biz>> wants **three tiers**: critical, low and ok. Combining comparisons with `if / elif / else` gives a clean multi-way decision."),
           T("elif", "Python checks the conditions **top to bottom** and runs the **first** one that is True:\n\n```python\nif units <= 5:\n    label = \"critical\"\nelif units <= 10:\n    label = \"low\"\nelse:\n    label = \"ok\"\n```\n\nBecause the first match wins, order the conditions from most specific to least."),
           T("Precedence", "Among the logical operators, `not` goes first, then `and`, then `or`. When you mix them, **use brackets**: `(a or b) and c` says exactly what you mean."),
           P("def f(n):\n    if n <= 5:\n        return \"low\"\n    elif n <= 10:\n        return \"mid\"\n    else:\n        return \"high\"\nprint(f(5), f(6), f(11))", "low mid high", ["low low high", "low mid mid"], "5 matches the first branch, 6 the second, and 11 falls through to else."),
           Q("In an if/elif/else chain, how many branches can run?", ["At most one", "All that match", "Exactly two"], 0, "Python runs the first matching branch and skips the rest.")],
          "Write `classify_stock(units)` that returns `\"critical\"` when `units` is at or below half of `<<vl>>` (use `<<vl>> // 2`), `\"low\"` when it is at or below `<<vl>>`, and `\"ok\"` otherwise. Print the result for three values: `<<vl>> // 2`, `<<vl>>` and `<<vl>> + 1`. It should print:\n\n<<OUT>>",
          "# classify_stock(units): critical, low or ok. Use <<vl>> and <<vl>> // 2\n# Print the result for <<vl>> // 2, <<vl>> and <<vl>> + 1\n",
          'def classify_stock(units):\n    """Return critical, low or ok for a stock level."""\n    if units <= <<vl>> // 2:\n        return "critical"\n    elif units <= <<vl>>:\n        return "low"\n    else:\n        return "ok"\n\n\nprint(classify_stock(<<vl>> // 2))\nprint(classify_stock(<<vl>>))\nprint(classify_stock(<<vl>> + 1))\n',
          checks=[("ftest", "classify_stock", [[[level // 2], "critical"], [[level], "low"], [[level + 1], "ok"], [[0], "critical"]])], hints=["Check the strictest condition first.", "Return a string in each branch."], emoji="🪜")

    c.add("chained_comparisons", "Chained Comparisons", "Ranges", "check ranges with chained comparisons",
          [T("The scenario", "A probe reading is healthy only if it sits **between** two limits. In most languages you write two comparisons joined by `and`. Python lets you write it the way you say it."),
           T("Chaining", "```python\n0 <= x <= 100      # x is between 0 and 100, inclusive\n```\n\nThat is exactly `0 <= x and x <= 100`, written once. You can chain more: `a < b < c < d`. Each neighbouring pair is checked, and Python stops at the first False."),
           T("Typical uses", "Ranges and bands: valid percentages, temperature windows, working hours, grade boundaries. Always say whether each end is inclusive (`<=`) or strict (`<`)."),
           P("x = 7\nprint(1 < x < 10, 10 < x < 20)", "True False", ["True True", "False False"], "7 is between 1 and 10, but not between 10 and 20."),
           Q("What does `0 <= x <= 100` check?", ["That x is between 0 and 100 inclusive", "That x equals 100", "That x is negative"], 0, "It is shorthand for two comparisons joined by and.")],
          "Define `low_limit = <<starget>> - 2` and `high_limit = <<starget>> + 2`, then `within_limits(reading)` returning whether the reading sits between them (inclusive, using one chained comparison). Print the result for each of the five readings in `<<sreads>>` (use `readings[0]` to `readings[4]`). It should print:\n\n<<OUT>>",
          "readings = <<sreads>>\n# low_limit, high_limit and within_limits(reading), then five print lines\n",
          'readings = <<sreads>>\nlow_limit = <<starget>> - 2\nhigh_limit = <<starget>> + 2\n\n\ndef within_limits(reading):\n    return low_limit <= reading <= high_limit\n\n\nprint(within_limits(readings[0]))\nprint(within_limits(readings[1]))\nprint(within_limits(readings[2]))\nprint(within_limits(readings[3]))\nprint(within_limits(readings[4]))\n',
          checks=[("var", "low_limit"), ("var", "high_limit")], hints=["return low_limit <= reading <= high_limit", "readings[0] is the first reading."], emoji="↔️")

    c.add("identity_operators", "Identity Operators", "is and is not", "use is, is not and None checks",
          [T("The scenario", "Two lists can hold the **same items** and still be **two different lists**, and sometimes that distinction matters a great deal. Python has a separate operator for \"are these the very same object?\"."),
           T("== vs is", "- `==` asks: **do they have equal contents?**\n- `is` asks: **are they the very same object in memory?**\n\n```python\na = [1, 2, 3]\nb = [1, 2, 3]\nc = a\nprint(a == b)   # True: equal contents\nprint(a is b)   # False: two separate lists\nprint(a is c)   # True: c is another name for a\n```"),
           T("The one place you always use is", "Compare with `None` using `is` and `is not`: `x is None`. There is only ever one `None`, so identity is exactly the question, and it is the style everyone expects."),
           P("x = None\nprint(x is None, x == None)", "True True", ["True False", "False False"], "Both work for None, but `is None` is the correct style."),
           Q("When should you use `is`?", ["To compare with None, or to ask if two names point to one object", "To compare numbers", "To compare text"], 0, "Use == for values and is for identity.")],
          "Two equal lists and a `None` alert are set up. Print five lines: `a == b`, `a is b`, `a is c`, `last_alert is None`, `last_alert is not None`. It should print:\n\n<<OUT>>",
          "a = [1, 2, 3]\nb = [1, 2, 3]\nc = a\nlast_alert = None\n# five print lines, as in the task\n",
          'a = [1, 2, 3]\nb = [1, 2, 3]\nc = a\nlast_alert = None\nprint(a == b)\nprint(a is b)\nprint(a is c)\nprint(last_alert is None)\nprint(last_alert is not None)\n',
          checks=[("prints", 5)], hints=["a is b asks about identity, a == b about contents.", "is not is its own operator."], emoji="🪪")

    c.add("membership_operators", "Membership Operators", "in and not in", "test membership with in",
          [T("The scenario", "Is this name one the <<system>> knows? Does the log mention an `ERROR`? Asking \"is it **in** there?\" is so common that Python gives it a word."),
           T("in and not in", "```python\n\"a\" in \"cat\"            # True: a piece of text\n3 in (1, 2, 3)          # True: an item in a tuple or list\n\"z\" not in \"cat\"        # True\n```\n\nFor text, `in` checks for a **substring**. For tuples and lists it checks for an **item**."),
           T("Case matters", "`\"error\" in \"ERROR: no signal\"` is `False`. Lower-case the text first when you do not care: `\"error\" in log.lower()`."),
           P('print("an" in "banana", 4 in (1, 2, 3), "z" not in "cat")', "True False True", ["True True True", "False False False"], "\"an\" is inside banana, 4 is not in the tuple, and z is not in cat."),
           Q("Is \"error\" in \"ERROR: no signal\"?", ["No, case matters", "Yes", "Only in a list"], 0, "Membership is case sensitive for text.")],
          "A tuple `known` holds the four <<things>>, and a short `log` is set up. Print four lines: whether `\"<<n2>>\"` is in `known`, whether `\"<<missing>>\"` is in `known`, whether `\"ERROR\"` is in `log`, and whether `\"CRITICAL\"` is **not** in `log`. It should print:\n\n<<OUT>>",
          'known = ("<<n1>>", "<<n2>>", "<<n3>>", "<<n4>>")\nlog = "08:05 WARN reading high\\n08:10 ERROR no signal"\n# four print lines using in and not in\n',
          'known = ("<<n1>>", "<<n2>>", "<<n3>>", "<<n4>>")\nlog = "08:05 WARN reading high\\n08:10 ERROR no signal"\nprint("<<n2>>" in known)\nprint("<<missing>>" in known)\nprint("ERROR" in log)\nprint("CRITICAL" not in log)\n',
          checks=[("prints", 4)], hints=["in checks whether the left side is inside the right side.", "not in is the opposite."], emoji="🔎")

    c.add("truthy_falsy", "Truthy and Falsy Values", "Truthiness", "use truthy and falsy values",
          [T("The scenario", "Python lets any value stand in for True or False inside an `if`. That makes code shorter (`if items:`) and also makes a famous kind of bug (`if count:` when 0 is a perfectly good count). Chapter seven ends with the full rules."),
           T("Falsy values", "These count as **False**: `False`, `None`, `0`, `0.0`, `\"\"` (empty text), `[]`, `()`, `{}`, `set()`. **Everything else is truthy**, including `\"0\"`, `\"False\"`, `[0]` and `-1`.\n\n```python\nprint(bool(\"\"), bool(\"0\"), bool([]), bool([0]))   # False True False True\n```"),
           T("Idioms and traps", "- `if items:` means \"if the list is not empty\"\n- `name = typed or \"unknown\"` uses `or` to supply a **default** when the text is empty\n- Trap: `if reading:` is False when the reading is **0**, which may be a real value. Use `is not None` when 0 is valid."),
           P('print(bool(""), bool("0"), bool([]), bool([0]))', "False True False True", ["False False False False", "True True True True"], "Empty things are falsy. A text \"0\" and a list holding 0 are not empty, so they are truthy."),
           Q("Which of these is falsy?", ["0.0", "\"0\"", "[0]"], 0, "The number 0.0 is falsy. The text \"0\" and the list [0] are not empty, so they are truthy.")],
          "Print the truthiness of eight values, one per line: `0`, `1`, `\"\"`, `\"0\"`, `None`, `[]`, `[0]`, `0.0`. Then print `label` where `label = typed or \"unknown\"` and `typed = \"\"`. Finally decide with an if/else on `items = []` whether to print `has items` or `empty`. It should print:\n\n<<OUT>>",
          'typed = ""\nitems = []\n# eight print(bool(...)) lines\n# print label, where label = typed or "unknown"\n# if items: print "has items", else print "empty"\n',
          'typed = ""\nitems = []\nprint(bool(0))\nprint(bool(1))\nprint(bool(""))\nprint(bool("0"))\nprint(bool(None))\nprint(bool([]))\nprint(bool([0]))\nprint(bool(0.0))\nlabel = typed or "unknown"\nprint(label)\nif items:\n    print("has items")\nelse:\n    print("empty")\n',
          checks=[("var", "label"), ("ast", "If", "an if statement")], hints=["bool(value) gives True or False.", "typed or \"unknown\" picks the default when typed is empty."], emoji="👻")
