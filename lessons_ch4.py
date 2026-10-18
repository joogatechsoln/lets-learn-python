"""Chapter 4: Scope (10 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Scope")
    q1, q2, p1, d = c.ctx["q1"], c.ctx["q2"], c.ctx["p1"], c.ctx["d"]

    c.add("intro_scope", "Introduction to Scope", "Scope", "explain where a name can be used",
          [T("The scenario", "A teammate's function works perfectly, but the line right after it crashes with a `NameError` about a variable that was *definitely* defined. The variable exists, but only **inside** the function. Where a name can be used is called its **scope**."),
           T("Rooms in a building", "Think of a program as a building. A name created in one room is not visible from the corridor. Python builds a new \"room\" every time a function runs.\n\n```python\ndef f():\n    x = 5        # x lives inside f\n\nf()\nprint(x)         # NameError: x is not defined here\n```\n\nThe rule: a name is visible in the place it was created, and in the places nested inside that place."),
           T("Getting a value out", "Because a function's variables stay inside, the proper way to get a result **out** is `return`:\n\n```python\ndef f():\n    x = 5\n    return x\n\nx = f()      # store the returned value outside\n```"),
           P("def f():\n    x = 5\nf()\nprint(x)", "!NameError", ["5", "None"], "x only existed inside f. Outside, Python has never heard of it."),
           Q("What is the scope of a name?", ["The part of the program where the name can be used", "How large its value is", "The type of its value"], 0, "Scope answers: from where can I see this name?")],
          "This program crashes because `stock_total` only exists inside the function. Fix it by making the function **return** the value and storing it outside. It should print:\n\n<<OUT>>",
          'def compute_value():\n    stock_total = <<q1>> * <<p1>>\n\n\ncompute_value()\nprint(stock_total)\n',
          'def compute_value():\n    stock_total = <<q1>> * <<p1>>\n    return stock_total\n\n\nstock_total = compute_value()\nprint(stock_total)\n',
          checks=[("var", "stock_total")], hints=["Add a return line inside the function.", "Store the result with stock_total = compute_value()."], emoji="🔭")

    c.add("local_variables", "Local Variables", "Local", "use variables that live inside one function",
          [T("The scenario", "Two reports at <<biz>>, the opening and the closing, each build a text label before printing. Both are naturally called `label`, and neither should interfere with the other. Local variables make that safe."),
           T("Local means private", "A variable created inside a function is **local** to it:\n\n- it is created when the function runs\n- it is **thrown away** when the function ends\n- every call gets a **fresh** one\n- the same name in two functions means **two separate** variables"),
           T("Why that is a gift", "Local variables mean a function cannot accidentally break the rest of the program, and the rest cannot break it. You can use short, natural names inside functions without worrying about clashes, which is why large teams can write functions independently."),
           P("def a():\n    n = 1\n    return n\ndef b():\n    n = 2\n    return n\nprint(a(), b())", "1 2", ["2 2", "1 1"], "Each function has its own n, so they never interfere."),
           Q("When a function finishes, its local variables are...", ["discarded", "kept for the next call", "turned into global variables"], 0, "The function's room is cleared up when it ends.")],
          "Both report functions use a local variable called `label`. Finish `closing_report()` so it returns the text `Closing: ` followed by the closing count (<<q1>> plus <<d>>). It should print:\n\n<<OUT>>\n\nAfterwards `label` must **not** exist outside the functions.",
          'def opening_report():\n    label = "Opening"\n    return label + ": " + str(<<q1>>)\n\n\ndef closing_report():\n    # use a local variable called label here too, and return label + ": " + the closing count\n    pass\n\n\nprint(opening_report())\nprint(closing_report())\n',
          'def opening_report():\n    label = "Opening"\n    return label + ": " + str(<<q1>>)\n\n\ndef closing_report():\n    label = "Closing"\n    return label + ": " + str(<<q1>> + <<d>>)\n\n\nprint(opening_report())\nprint(closing_report())\n',
          checks=[("absent", "label"), ("ftest", "closing_report", [[[], f"Closing: {q1 + d}"]])], hints=["Mirror opening_report: a local label, then return label + \": \" + str(...).", "Do not create label outside the functions."], emoji="🏠")

    c.add("global_variables", "Global Variables", "Global", "read module-level variables from functions",
          [T("The scenario", "Some facts are true everywhere in the program: the company name, the rule number. Passing them into every function would be tedious. Variables created at the **top level** of the file are **global** and visible everywhere."),
           T("Reading a global", "A function can **read** a global with no special keyword:\n\n```python\nrate = 3\n\ndef show():\n    print(rate)      # finds the global\n\nshow()               # 3\n```\n\nGlobals are best used for **constants**: values that never change, written in UPPER_CASE so every reader knows."),
           T("Use with care", "Reading globals is fine. The danger starts when many functions change them, because then any function could be the cause of a wrong value. Next lesson you will see how Python protects you from changing a global by accident."),
           P("rate = 3\ndef show():\n    print(rate)\nshow()", "3", ["!NameError", "None"], "The function does not have its own rate, so Python looks outward and finds the global."),
           Q("Can a function read a global variable without any special keyword?", ["Yes", "No, it needs global", "Only if it is a number"], 0, "Reading needs nothing special. Changing is the part that needs care.")],
          "A global `OWNER` and the rule constant `<<VL>>` (set in chapter two) are available. Finish the two functions so that:\n\n- `signature()` returns `OWNER` followed by ` / <<system>>`\n- `level_note()` returns `Rule number: ` followed by the value of `<<VL>>`\n\nIt should print:\n\n<<OUT>>",
          'OWNER = "<<biz>>"\n\n\ndef signature():\n    # return OWNER + " / <<system>>"\n    pass\n\n\ndef level_note():\n    # return "Rule number: " followed by <<VL>>\n    pass\n\n\nprint(signature())\nprint(level_note())\n',
          'OWNER = "<<biz>>"\n\n\ndef signature():\n    return OWNER + " / <<system>>"\n\n\ndef level_note():\n    return "Rule number: " + str(<<VL>>)\n\n\nprint(signature())\nprint(level_note())\n',
          checks=[("ftest", "signature", [[[], c.ctx["biz"] + " / " + c.ctx["system"]]])], hints=["Use the global names directly inside the function.", "<<VL>> is a number, so wrap it in str() before joining it to text."], emoji="🌍")

    c.add("global_keyword", "The global Keyword", "global", "change a global from inside a function",
          [T("The scenario", "The till counts sales through the day with a global `sales_today`. A teammate wrote a function to add one sale, and Python answers with a confusing `UnboundLocalError`. You will learn why, and how the `global` keyword solves it."),
           T("Why the error happens", "When a function **assigns** to a name (`=`, `+=`), Python decides that name is **local** to that function. So `sales_today += 1` tries to read a *local* `sales_today` that does not exist yet.\n\n```python\ncount = 0\ndef bump():\n    count += 1      # UnboundLocalError\n```"),
           T("global", "Declare the name with `global` at the top of the function to say \"I mean the one outside\":\n\n```python\ncount = 0\ndef bump():\n    global count\n    count += 1\n\nbump()\nprint(count)     # 1\n```\n\nIt works, but treat `global` as a last resort. A function that **returns** a value is easier to understand and test."),
           P("n = 0\ndef add():\n    global n\n    n += 5\nadd()\nprint(n)", "5", ["0", "!UnboundLocalError"], "With `global n`, the function changes the outside variable."),
           Q("Why is changing globals from many functions risky?", ["Any function might be the one that changed it, so bugs are hard to trace", "Python forbids it", "It is always slower"], 0, "Shared mutable state makes it hard to tell who changed what.")],
          "`record_sale()` should add one to the global `sales_today`, but it raises an `UnboundLocalError`. Fix it with `global`. After three calls it should print:\n\n<<OUT>>",
          'sales_today = 0\n\n\ndef record_sale():\n    sales_today += 1\n\n\nrecord_sale()\nrecord_sale()\nrecord_sale()\nprint("Sales today:", sales_today)\n',
          'sales_today = 0\n\n\ndef record_sale():\n    global sales_today\n    sales_today += 1\n\n\nrecord_sale()\nrecord_sale()\nrecord_sale()\nprint("Sales today:", sales_today)\n',
          checks=[("var", "sales_today")], hints=["Read the last line of the error: it says the variable is referenced before assignment.", "Add global sales_today as the first line of the function."], emoji="🌐")

    c.add("nonlocal_keyword", "The nonlocal Keyword", "nonlocal", "change a variable of an enclosing function",
          [T("The scenario", "The front desk needs a **counter** that remembers how many <<things>> have been logged since the shift began, without using a global. Python lets a function nested inside another function keep and change the outer function's variable."),
           T("Functions inside functions", "You can define a function inside another one. The inner function can **read** the outer function's variables. To **change** one, you need `nonlocal`, the sibling of `global`:\n\n```python\ndef make_counter():\n    count = 0\n    def add_one():\n        nonlocal count\n        count += 1\n        return count\n    return add_one\n\nnext_number = make_counter()\nprint(next_number())    # 1\nprint(next_number())    # 2\n```"),
           T("Memory between calls", "The function that `make_counter` returns *remembers* `count`, even though `make_counter` itself has finished. This is called a **closure**. Each call to `make_counter()` builds a brand-new counter with its own memory."),
           P("def outer():\n    x = 1\n    def inner():\n        nonlocal x\n        x = 2\n    inner()\n    return x\nprint(outer())", "2", ["1", "!UnboundLocalError"], "nonlocal x makes inner change outer's x, so outer returns 2."),
           Q("`nonlocal` refers to a variable in...", ["the nearest enclosing function", "the global scope", "any function that has the same name"], 0, "It looks outward one function at a time, but never to the global scope.")],
          "Finish the inner function so that every call adds one to `count` and returns the new total. Calling the counter three times should print:\n\n<<OUT>>",
          'def make_tally():\n    count = 0\n\n    def add_one():\n        # add one to count (it belongs to make_tally, not to add_one) and return it\n        pass\n\n    return add_one\n\n\nunit_counter = make_tally()\nprint(unit_counter())\nprint(unit_counter())\nprint(unit_counter())\n',
          'def make_tally():\n    count = 0\n\n    def add_one():\n        nonlocal count\n        count += 1\n        return count\n\n    return add_one\n\n\nunit_counter = make_tally()\nprint(unit_counter())\nprint(unit_counter())\nprint(unit_counter())\n',
          hints=["Declare nonlocal count at the top of add_one.", "Then count += 1 and return count."], emoji="🔢")

    c.add("nested_scopes", "Enclosing and Nested Scopes", "Closures", "build functions that remember values",
          [T("The scenario", "Different customers of <<biz>> pay different rates. Rather than pass the rate into every single call, you can build a **custom function for each rate**: a function factory."),
           T("Functions that build functions", "An outer function can create and **return** an inner function. The inner function remembers the outer function's parameters:\n\n```python\ndef make_adder(n):\n    def add(x):\n        return x + n\n    return add\n\nadd5 = make_adder(5)\nprint(add5(10))      # 15\n```\n\n`n` stays attached to `add`, even after `make_adder` has finished."),
           T("Why it is useful", "You configure once, then call many times with less to type: a pricer for each rate, a formatter for each unit, a checker for each limit. It is also the idea behind many Python tools you will meet later."),
           P("def make_adder(n):\n    def add(x):\n        return x + n\n    return add\nadd5 = make_adder(5)\nprint(add5(10))", "15", ["10", "5"], "add5 remembers n = 5, so add5(10) is 15."),
           Q("An inner function can read variables from...", ["the function that encloses it", "only its own parameters", "nowhere else"], 0, "Python looks outward through enclosing functions.")],
          "Write `make_pricer(<<ar>>)` that returns a function `price_for(<<aq>>)` which gives <<aq>> times that rate. Build a pricer for the first <<thing>> and use it twice. It should print:\n\n<<OUT>>",
          'def make_pricer(<<ar>>):\n    # define price_for(<<aq>>) inside, returning <<aq>> * <<ar>>, then return price_for\n    pass\n\n\nprice_for = make_pricer(<<p1>>)\nprint(price_for(<<q1>>))\nprint(price_for(<<q2>>))\n',
          'def make_pricer(<<ar>>):\n    def price_for(<<aq>>):\n        return <<aq>> * <<ar>>\n    return price_for\n\n\nprice_for = make_pricer(<<p1>>)\nprint(price_for(<<q1>>))\nprint(price_for(<<q2>>))\n',
          checks=[("ftest", "price_for", [[[q1], q1 * p1], [[q2], q2 * p1]])], hints=["Define the inner function inside make_pricer.", "Return the inner function itself, without brackets."], emoji="🪆")

    c.add("legb_rule", "The LEGB Rule", "LEGB", "predict which variable Python finds",
          [T("The scenario", "Three variables all called `level_name` exist at once: one global, one in an outer function, one in an inner function. Which one does Python use? There is a precise answer, and it is the key to every scope puzzle."),
           T("L, E, G, B", "When you use a name, Python searches **four places in order** and stops at the first match:\n\n- **L**ocal: inside the current function\n- **E**nclosing: inside any functions around it, innermost first\n- **G**lobal: the top level of the file\n- **B**uilt-in: Python's own names like `len` and `print`\n\nIf none match, you get a `NameError`."),
           T("Reading it in practice", "To work out what a line will use, start where the line is and look **outward**. The nearest match wins, so a name inside a function **hides** a name outside with the same spelling. That hiding is the subject of the next lesson."),
           P('x = "G"\ndef f():\n    x = "L"\n    return x\nprint(f(), x)', "L G", ["G G", "L L"], "Inside f, the local x is found first. Outside, only the global exists."),
           Q("In what order does Python search for a name?", ["Local, Enclosing, Global, Built-in", "Global, Local, Built-in, Enclosing", "Built-in, Global, Enclosing, Local"], 0, "Remember LEGB: Local, Enclosing, Global, Built-in.")],
          "The code below sets `level_name` in three places. Add one `print(level_name)` at each of the three marked spots so that each prints the value from **its own** scope. It should print:\n\n<<OUT>>",
          'level_name = "global"\n\n\ndef outer():\n    level_name = "enclosing"\n\n    def inner():\n        level_name = "local"\n        # print level_name here\n\n    inner()\n    # print level_name here\n\n\nouter()\n# print level_name here\n',
          'level_name = "global"\n\n\ndef outer():\n    level_name = "enclosing"\n\n    def inner():\n        level_name = "local"\n        print(level_name)\n\n    inner()\n    print(level_name)\n\n\nouter()\nprint(level_name)\n',
          checks=[("prints", 3)], hints=["Inside inner, the nearest level_name is the local one.", "After inner() returns, you are back in outer, so you see the enclosing one."], emoji="🔍")

    c.add("variable_shadowing", "Variable Shadowing", "Shadowing", "avoid hiding names by accident",
          [T("The scenario", "A teammate named a variable `max` because it holds the maximum count. Later, the program calls the built-in `max(...)` and crashes with a baffling message. The variable has **shadowed** the function."),
           T("What shadowing is", "When a name in an inner scope (or a later line) has the same spelling as one further out, it **hides** the outer one. Python never warns you:\n\n```python\nmax = 5\nprint(max(1, 2))    # TypeError: 'int' object is not callable\n```\n\nThe built-in is still there, but your variable is found first (LEGB), and a number cannot be called like a function."),
           T("How to avoid it", "- Never name variables after built-ins: `max`, `min`, `sum`, `len`, `list`, `type`, `str`, `id`\n- Use descriptive names: `highest_count`, `total_value`\n- Shadowing a *global* inside a function is sometimes intended, but do it knowingly\n\nIf a built-in suddenly \"stops working\", check whether you shadowed it."),
           P('len = 3\nprint(len("abc"))', "!TypeError", ["3", "abc"], "len is now the number 3, and a number cannot be called."),
           Q("What is the safest fix for a variable called `sum`?", ["Rename the variable to something descriptive", "Delete the program", "Put the variable in quotes"], 0, "A descriptive name like total_count avoids the clash entirely.")],
          "The first line shadows a built-in and the second line crashes. Rename the variable to `highest_count` so the program prints the count and then the real maximum of <<q1>>, <<q2>> and <<d>>. It should print:\n\n<<OUT>>",
          'max = <<q1>>\nprint(max, max(<<q1>>, <<q2>>, <<d>>))\n',
          'highest_count = <<q1>>\nprint(highest_count, max(<<q1>>, <<q2>>, <<d>>))\n',
          checks=[("var", "highest_count"), ("absent", "max")], hints=["The error says an int cannot be called: something named max is not the function any more.", "Pick a name that says what the number is."], emoji="🕶️")

    c.add("scope_parameters", "Scope and Function Parameters", "Parameters", "know that parameters are local variables",
          [T("The scenario", "The `apply_delivery` function adds a delivery to a count. Inside the function the number is right. Outside, the original count has not changed at all, and the shelf still shows the old figure. Where did the update go?"),
           T("Parameters are locals", "A parameter is a **local variable** that is given a value when the function is called. Re-assigning it inside the function changes only the local copy:\n\n```python\ndef bump(n):\n    n += 1\n    return n\n\nx = 5\nbump(x)\nprint(x)       # still 5\n```\n\nNumbers, text and tuples are never changed by a function that receives them. The function gets its own name for the same value."),
           T("The fix: return and reassign", "To get an updated value out, **return** it and store it where you need it:\n\n```python\nx = bump(x)      # now x is 6\n```\n\nThis style, in which data goes in and results come out, keeps functions simple and easy to test. (Lists behave differently, and you will see why in the chapter on lists.)"),
           P("def bump(n):\n    n += 1\n    return n\nx = 5\nbump(x)\nprint(x)", "5", ["6", "!NameError"], "bump returned 6 but the result was thrown away. x itself never changed."),
           Q("A parameter is...", ["a local variable of the function", "a global variable", "a constant"], 0, "Parameters live only for the duration of the call.")],
          "The count `on_shelf` is still the old figure after the function runs. Make `apply_delivery` **return** the new count and store it back in `on_shelf`. It should print:\n\n<<OUT>>",
          'def apply_delivery(units, delivered):\n    units = units + delivered\n    print("Inside:", units)\n\n\non_shelf = <<q1>>\napply_delivery(on_shelf, <<d>>)\nprint("Outside:", on_shelf)\n',
          'def apply_delivery(units, delivered):\n    units = units + delivered\n    print("Inside:", units)\n    return units\n\n\non_shelf = <<q1>>\non_shelf = apply_delivery(on_shelf, <<d>>)\nprint("Outside:", on_shelf)\n',
          checks=[("var", "on_shelf")], hints=["Add return units at the end of the function.", "Assign the call's result back: on_shelf = apply_delivery(...)"], emoji="📦")

    c.add("common_scope_errors", "Common Scope Errors", "Chapter 4 project", "diagnose the usual scope bugs",
          [T("The scenario", "Chapter four ends with a repair job. A colleague's program has **three scope bugs**, one after the other. Python only reports one at a time, so you will read, fix, run and repeat, exactly like real debugging."),
           T("The usual suspects", "- **NameError**: using a name outside the function where it was created, or misspelling it\n- **UnboundLocalError**: assigning to a name inside a function without `global` or `nonlocal`\n- **TypeError: ... object is not callable**: a variable shadowing a built-in\n- A function that **prints** where it should **return**, or the reverse\n- Changing a global from many places and losing track"),
           T("A routine", "1. Read the last line of the traceback: the error type tells you which suspect it is\n2. Find the line it points to and ask: *where was this name created?*\n3. Fix one thing, run again, read the next error\n\nAfter fixing, ask whether the code can avoid the global altogether by returning a value."),
           Q("`UnboundLocalError: cannot access local variable` usually means...", ["A function assigned to a name it did not declare global", "A typo in a function's name", "A missing import"], 0, "Assignment makes the name local, so reading it before assigning fails.")],
          "Fix all **three** scope bugs so the program prints:\n\n<<OUT>>\n\nRun it, read the error, fix it, and repeat. The tally must be kept in the global `tally`.",
          'tally = 0\n\n\ndef add_delivery(amount):\n    tally = tally + amount\n\n\ndef describe():\n    return "Tally is " + str(total)\n\n\nsum = <<q1>> + <<d>>\nadd_delivery(<<d>>)\nprint(describe())\nprint(sum, sum([1, 2, 3]))\n',
          'tally = 0\n\n\ndef add_delivery(amount):\n    global tally\n    tally = tally + amount\n\n\ndef describe():\n    return "Tally is " + str(tally)\n\n\nclosing_total = <<q1>> + <<d>>\nadd_delivery(<<d>>)\nprint(describe())\nprint(closing_total, sum([1, 2, 3]))\n',
          checks=[("var", "tally"), ("absent", "sum")], hints=["The first error is an UnboundLocalError: add_delivery assigns to tally.", "The second is a NameError: describe uses a name that does not exist.", "The third: a variable called sum hides the built-in sum. Rename it."], emoji="🛠️")
