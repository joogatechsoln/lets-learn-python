"""Chapter 8: Loops (12 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Loops")
    X = c.ctx
    VN, VL = X["vnames"], X["vl"]
    names = [X[f"n{i}"] for i in range(1, 5)]
    qs = [X[f"q{i}"] for i in range(1, 5)]
    q1, d = X["q1"], X["d"]
    LIST4 = "[" + ", ".join(f'"{n}"' for n in names) + "]"
    QS = "[" + ", ".join(str(q) for q in qs) + "]"

    c.add("intro_loops", "Introduction to Loops", "Repetition", "repeat work with a for loop",
          [T("The scenario", "The morning check at <<biz>> visits every <<thing>>: four today, four hundred next year. Writing one print line per item is impossible at that size. Computers are made for repetition, and **loops** are how you ask for it."),
           T("Repeat instead of copy", "These do the same job:\n\n```python\nprint(\"Checking: a\")\nprint(\"Checking: b\")\nprint(\"Checking: c\")\n```\n\n```python\nfor item in (\"a\", \"b\", \"c\"):\n    print(\"Checking:\", item)\n```\n\nThe indented lines are the **body**. Python runs it once for each item, with `item` set to the next value each time."),
           T("Two kinds of loop", "- `for` repeats **once per item** in a collection\n- `while` repeats **as long as a condition is True**\n\nUse `for` when you know what you are looping over. Use `while` when you do not know how many times in advance."),
           P('for n in (1, 2, 3):\n    print(n * 10)', "10\n20\n30", ["10 20 30", "30"], "The body runs three times with n = 1, 2, 3."),
           Q("When does a for loop stop?", ["After the last item", "After one second", "When you press Enter"], 0, "A for loop visits every item once, then ends.")],
          "The starter checks the <<things>> one print at a time. Replace the four prints with a **single for loop** over the tuple of names that prints `Checking: ` and the name. It should print:\n\n<<OUT>>",
          'print("Checking: <<n1>>")\nprint("Checking: <<n2>>")\nprint("Checking: <<n3>>")\nprint("Checking: <<n4>>")\n',
          'for name in ("<<n1>>", "<<n2>>", "<<n3>>", "<<n4>>"):\n    print("Checking:", name)\n',
          checks=[("ast", "For", "a for loop")], hints=["for name in (...): then an indented print.", "Put the four names in a tuple in round brackets."], emoji="🔁")

    c.add("while_loop", "The while Loop", "while", "repeat while a condition holds",
          [T("The scenario", "A delivery of <<d>> arrives each round, and the <<system>> must keep restocking **until** a target is reached. How many rounds? Nobody knows in advance, which is exactly when `while` is the right loop."),
           T("while", "```python\ncount = 0\nwhile count < 3:\n    print(count)\n    count += 1\n```\n\nPython checks the condition **before every pass**. If it is True it runs the body, then checks again. When it is False the loop ends and the program carries on below."),
           T("The loop must change something", "Whatever the condition looks at has to **change inside the body**, otherwise it stays True forever. Every while loop needs three parts: a **start** value, a **condition**, and an **update**."),
           P("n = 3\nwhile n > 0:\n    print(n)\n    n -= 1", "3\n2\n1", ["3\n2\n1\n0", "3"], "It prints 3, 2, 1 and stops as soon as n is 0, because 0 > 0 is False."),
           Q("What are the three parts of a safe while loop?", ["Start value, condition, update", "Start, middle, end of file", "Name, type, value"], 0, "Without an update the condition never changes and the loop never ends.")],
          "Restock until the count reaches `target = <<q1>> + 15`, adding 5 each round. Start with `units = <<q1>>` and count the rounds in `rounds`. Print `Restocked to ` and the new count after each round, then print `Rounds: ` and the number. It should print:\n\n<<OUT>>",
          "units = <<q1>>\ntarget = <<q1>> + 15\nrounds = 0\n# while units < target: add 5, count the round, print Restocked to <units>\n# then print Rounds: <rounds>\n",
          'units = <<q1>>\ntarget = <<q1>> + 15\nrounds = 0\nwhile units < target:\n    units += 5\n    rounds += 1\n    print("Restocked to", units)\nprint("Rounds:", rounds)\n',
          checks=[("var", "rounds", True), ("ast", "While", "a while loop")], hints=["The condition is units < target.", "Update units inside the loop."], emoji="🔄")

    c.add("for_loop", "The for Loop", "for", "loop over text and tuples",
          [T("The scenario", "The tag code of the <<sn>> is `<<stag>>`. Support wants it spelled out one letter per line for a label printer, and the three most recent counts added together. Both are `for` jobs."),
           T("for item in collection", "```python\nfor letter in \"cat\":\n    print(letter)         # c, a, t\n\ntotal = 0\nfor n in (4, 5, 6):\n    total += n\nprint(total)             # 15\n```\n\nThe **loop variable** (`letter`, `n`) takes each value in turn. You choose its name: pick one that says what it holds."),
           T("The accumulator", "Starting a variable at 0 before the loop and adding to it inside is the **accumulator pattern**. It turns a loop into a total, and you will use it constantly."),
           P('for ch in "hi":\n    print(ch.upper())', "H\nI", ["HI", "hi"], "The loop visits h then i, printing each in capitals."),
           Q("In `for n in (4, 5, 6):`, what is n?", ["The current item, a different one each time", "The number of items", "Always 4"], 0, "n is rebound to the next item on every pass.")],
          "Print each letter of `\"<<stag>>\"` on its own line. Then add up the numbers `<<q1>>`, `<<q2>>` and `<<d>>` with a loop and print the total. It should print:\n\n<<OUT>>",
          "# loop over the letters of \"<<stag>>\" and print each\n# loop over (<<q1>>, <<q2>>, <<d>>) adding to total, then print total\n",
          'for letter in "<<stag>>":\n    print(letter)\n\ntotal = 0\nfor n in (<<q1>>, <<q2>>, <<d>>):\n    total += n\nprint(total)\n',
          checks=[("var", "total")], hints=["Start total = 0 before the loop.", "A string is a sequence of letters, so you can loop over it."], emoji="🔤")

    c.add("iterating_sequences", "Iterating Over Sequences", "Sequences", "loop over lists with numbers",
          [T("The scenario", "The <<system>> keeps its <<things>> in a **list**, which you will study in depth in the next chapter. For now you only need to know how to walk along one, and how to number the lines of a report."),
           T("Sequences", "Text, tuples and **lists** (square brackets) are all **sequences**: ordered collections. A for loop walks any sequence from first to last:\n\n```python\nfor fruit in [\"fig\", \"plum\"]:\n    print(fruit)\n```"),
           T("enumerate", "To get a **number with each item**, use `enumerate`:\n\n```python\nfor number, fruit in enumerate([\"fig\", \"plum\"], 1):\n    print(f\"{number}. {fruit}\")     # 1. fig   2. plum\n```\n\nThe second argument is where counting starts. Use it instead of managing a counter by hand."),
           P('for i, x in enumerate(["a", "b"], 1):\n    print(i, x)', "1 a\n2 b", ["0 a\n1 b", "a\nb"], "enumerate pairs a counter, starting at 1, with each item."),
           Q("What does enumerate(items, 1) give you?", ["A counter starting at 1 with each item", "The items in reverse", "The number of items"], 0, "It saves you from keeping a separate counter.")],
          "Create the list `<<vnames>>` with the four <<things>>, then print a numbered list with `enumerate`, starting at 1, like `1. <<n1>>`. It should print:\n\n<<OUT>>",
          "# <<vnames>> = a list of the four names (in square brackets)\n# for number, name in enumerate(...): print like 1. name\n",
          f'{VN} = {LIST4}\nfor number, name in enumerate({VN}, 1):\n    print(f"{{number}}. {{name}}")\n',
          checks=[("var", VN)], hints=["A list is the four names in square brackets, separated by commas.", "enumerate(<<vnames>>, 1) gives number and name."], emoji="🔢")

    c.add("range_function", "The range() Function", "range", "generate number sequences with range",
          [T("The scenario", "Sometimes there is no collection to walk along. You just need \"do this ten times\", or the numbers 5, 10, 15, 20 for a table. `range` produces number sequences on demand."),
           T("range", "```python\nrange(5)          # 0, 1, 2, 3, 4   (stops BEFORE 5)\nrange(2, 6)       # 2, 3, 4, 5\nrange(0, 20, 5)   # 0, 5, 10, 15    (step of 5)\nrange(5, 0, -1)   # 5, 4, 3, 2, 1  (counting down)\n```\n\nThe **end is never included**. Wrap it in `list(...)` to see the values: `list(range(3))` is `[0, 1, 2]`."),
           T("Counting loops", "`for i in range(n):` is the standard way to repeat something exactly `n` times, and `i` is the count from 0. It never builds the whole list in memory, so even `range(10_000_000)` is cheap."),
           P("print(list(range(2, 8, 2)))", "[2, 4, 6]", ["[2, 4, 6, 8]", "[0, 2, 4, 6]"], "It starts at 2, steps by 2, and stops before 8."),
           Q("What is the last number in range(5)?", ["4", "5", "6"], 0, "The end value is excluded.")],
          "Print four ranges as lists (`range(5)`, `range(2, 8)`, `range(0, 20, 5)` and `range(5, 0, -1)`), then use a loop over `range(1, 11)` to add up 1 to 10 into `total`, and print it. It should print:\n\n<<OUT>>",
          "# four print(list(range(...))) lines\n# total of 1 to 10 with a loop, then print total\n",
          'print(list(range(5)))\nprint(list(range(2, 8)))\nprint(list(range(0, 20, 5)))\nprint(list(range(5, 0, -1)))\ntotal = 0\nfor i in range(1, 11):\n    total += i\nprint(total)\n',
          checks=[("var", "total", True)], hints=["range(1, 11) includes 1 and stops before 11.", "list(range(...)) lets print show the numbers."], emoji="📏")

    c.add("break_statement", "The break Statement", "break", "stop a loop early with break",
          [T("The scenario", "The morning check only needs to know **which is the first <<thing>>** that is running low. Once it finds one, walking the remaining items is wasted effort. `break` stops a loop the moment it has its answer."),
           T("break", "```python\nfor n in (3, 8, 12, 5):\n    if n > 10:\n        print(\"found\", n)\n        break\n```\n\n`break` jumps **out of the loop** immediately. Code after the loop carries on as normal. It is the classic way to **search** a collection."),
           T("Remember what you found", "Set a variable before the loop (`found = None`), update it before `break`, and check it afterwards. That way you know both *what* you found and *whether* you found anything."),
           P("for n in (3, 8, 12, 5):\n    if n > 10:\n        print(n)\n        break", "12", ["12\n5", "3\n8\n12"], "It stops at 12 and never visits 5."),
           Q("What does break do?", ["Ends the loop immediately", "Skips to the next item", "Ends the program"], 0, "break leaves the loop. continue skips just one pass.")],
          f"Search for the first <<thing>> whose quantity is at or below `limit`. The names and quantities are set up; `limit` is the lowest quantity plus 5. Loop over the positions with `range(len(...))`, stop at the first match with `break`, and count how many items you checked in `checked`. Print `Found: ` and the name, then `Checked: ` and the number. It should print:\n\n<<OUT>>",
          f'names = {LIST4}\nquantities = {QS}\nlimit = min(quantities) + 5\nfirst_low = None\nchecked = 0\n# loop over the positions, count each check, stop at the first quantity <= limit\n# print Found: <name> and Checked: <checked>\n',
          f'names = {LIST4}\nquantities = {QS}\nlimit = min(quantities) + 5\nfirst_low = None\nchecked = 0\nfor i in range(len(quantities)):\n    checked += 1\n    if quantities[i] <= limit:\n        first_low = names[i]\n        break\nprint("Found:", first_low)\nprint("Checked:", checked)\n',
          checks=[("var", "first_low"), ("var", "checked", True), ("ast", "Break", "a break")], hints=["names[i] and quantities[i] describe the same item.", "Count first, then test, then break."], emoji="🛑")

    c.add("continue_statement", "The continue Statement", "continue", "skip bad items with continue",
          [T("The scenario", "One of the <<sn>>'s readings is a glitch: `999.0`, impossible. A report that averages it in is wrong. The loop should **skip** bad readings and carry on with the next."),
           T("continue", "```python\nfor n in (4, 999, 6):\n    if n > 100:\n        continue        # skip this one\n    print(n)            # 4, then 6\n```\n\n`continue` ends the **current pass** and jumps straight to the next item. `break` ends the whole loop. `continue` ends just one trip round it."),
           T("Filtering with continue", "Putting the skip rule at the **top** of the body, and the real work below, keeps loops flat and easy to read, rather than nesting everything inside one big `if`."),
           P("for n in (1, 2, 3, 4):\n    if n % 2 == 0:\n        continue\n    print(n)", "1\n3", ["2\n4", "1\n2\n3\n4"], "Even numbers are skipped, so only 1 and 3 are printed."),
           Q("How is continue different from break?", ["continue skips one item, break ends the loop", "They are the same", "continue ends the program"], 0, "continue means \"next item please\".")],
          "The readings below contain one glitch, `999.0`. Loop over them, **skip** anything above 500 with `continue`, and keep a running `good_total` and a count `good_count` of the others. Print the total and the count. It should print:\n\n<<OUT>>",
          'values = <<sreads>>[:2] + [999.0] + <<sreads>>[2:]\ngood_total = 0\ngood_count = 0\n# loop over values, skipping anything above 500\n# print good_total, then good_count\n',
          'values = <<sreads>>[:2] + [999.0] + <<sreads>>[2:]\ngood_total = 0\ngood_count = 0\nfor value in values:\n    if value > 500:\n        continue\n    good_total += value\n    good_count += 1\nprint(good_total)\nprint(good_count)\n',
          checks=[("var", "good_total"), ("var", "good_count", True), ("ast", "Continue", "a continue")], hints=["Put the if/continue at the top of the loop body.", "Only the good values reach the lines below it."], emoji="⏭️")

    c.add("pass_statement", "The pass Statement", "pass", "use pass as a placeholder",
          [T("The scenario", "The team agreed that low stock should trigger an alert, but the alert function is not written yet. You still want the rest of the program to run. Python needs *something* in an empty body, and that something is `pass`."),
           T("pass", "A block cannot be empty: `def f():` with nothing under it is a `SyntaxError`. `pass` is a statement that **does nothing**:\n\n```python\ndef send_alert(name):\n    pass          # TODO: write this later\n```\n\nUse it for **stubs** (functions and classes you will fill in later) and for branches that deliberately do nothing."),
           T("A stub is a promise", "Stubs let you build the shape of a program first, then fill it in piece by piece. Put a comment on every `pass` that says what is coming, otherwise it is easy to forget."),
           P("def todo():\n    pass\nprint(todo())", "None", ["pass", "!SyntaxError"], "The function body does nothing, so the call returns None."),
           Q("Why does Python have pass?", ["A block cannot be empty, and pass fills it", "It pauses the program", "It passes a value to a function"], 0, "pass is a do-nothing statement that keeps the syntax valid.")],
          "Write the stub `send_alert(name)` with `pass`, then loop over the names and quantities and call it for every quantity at or below `limit` (the lowest quantity plus 5), counting the alerts in `alerts`. Healthy items must use an `else` branch with `pass` and a comment. Print `Alerts: ` and the count. It should print:\n\n<<OUT>>",
          f'names = {LIST4}\nquantities = {QS}\nlimit = min(quantities) + 5\nalerts = 0\n# def send_alert(name): a stub using pass\n# loop: low items call send_alert and add to alerts; healthy items use pass\n# print Alerts: <alerts>\n',
          f'names = {LIST4}\nquantities = {QS}\nlimit = min(quantities) + 5\nalerts = 0\n\n\ndef send_alert(name):\n    pass          # TODO: send a real alert\n\n\nfor i in range(len(names)):\n    if quantities[i] <= limit:\n        send_alert(names[i])\n        alerts += 1\n    else:\n        pass      # healthy stock needs nothing yet\nprint("Alerts:", alerts)\n',
          checks=[("var", "alerts", True), ("ast", "Pass", "pass")], hints=["def send_alert(name): then an indented pass.", "if ...: do something, else: pass"], emoji="🧱")

    c.add("nested_loops", "Nested Loops", "Loops in loops", "put a loop inside a loop",
          [T("The scenario", "The data centre has racks, and every rack has slots. To label every slot you need to visit **every rack**, and for each rack **every slot**. That is a loop inside a loop."),
           T("Nesting", "```python\nfor row in range(1, 3):\n    for col in range(1, 4):\n        print(row, col)\n```\n\nThe **inner** loop runs completely for each pass of the **outer** loop. Here the outer runs 2 times and the inner 3 times each, so `print` runs 2 x 3 = **6** times."),
           T("Watch the cost", "Nested loops multiply work. 1,000 x 1,000 is a million passes. That is fine for a computer once, but a hidden nested loop in a function you call a million times is a classic reason programs get slow."),
           P("for i in range(2):\n    for j in range(2):\n        print(i, j)", "0 0\n0 1\n1 0\n1 1", ["0 0\n1 1", "0 1\n1 0"], "For each i, j runs through 0 and 1."),
           Q("An outer loop of 4 passes and an inner loop of 5 passes run the inner body...", ["20 times", "9 times", "5 times"], 0, "4 times 5 passes.")],
          "Print a label for every slot: racks 1 to 2 and slots 1 to 3, like `<<stag>>-R1-S1`, using nested loops. Count the labels in `labels` and print `Labels: ` and the count at the end. It should print:\n\n<<OUT>>",
          "labels = 0\n# nested loops over racks 1-2 and slots 1-3: print <<stag>>-R<rack>-S<slot>, counting each\n# then print Labels: <labels>\n",
          'labels = 0\nfor rack in range(1, 3):\n    for slot in range(1, 4):\n        print(f"<<stag>>-R{rack}-S{slot}")\n        labels += 1\nprint("Labels:", labels)\n',
          checks=[("var", "labels", True)], hints=["The inner for is indented inside the outer for.", "range(1, 3) is racks 1 and 2."], emoji="🪆")

    c.add("loop_else", "Looping with else", "for ... else", "use else on a loop to detect not found",
          [T("The scenario", "A search has two outcomes: found (stop and report) or **not found after looking everywhere**. Tracking that second case with an extra flag variable is clumsy. Python loops have an `else` clause made for it."),
           T("for ... else", "```python\nfor n in (3, 8, 12):\n    if n > 100:\n        print(\"found\")\n        break\nelse:\n    print(\"not found\")\n```\n\nThe `else` block runs **only if the loop finished without hitting `break`**. If `break` ran, `else` is skipped."),
           T("Read it as \"no break\"", "Many programmers read the loop `else` as **\"no break\"**. It sounds odd at first, but it removes a flag variable and keeps the search in one place."),
           P('for n in (1, 2):\n    if n > 5:\n        break\nelse:\n    print("none")', "none", ["", "1\n2"], "The loop never breaks, so else runs."),
           Q("When does the else block of a loop run?", ["When the loop ends without break", "Every time", "Only when break runs"], 0, "Think of it as \"no break happened\".")],
          "Write `search(names, target)` that loops over the names and prints `Found <name>` and breaks when it matches, or prints `No <target>` using the loop's `else`. Call it for `\"<<n3>>\"` and for `\"<<missing>>\"`. It should print:\n\n<<OUT>>",
          f'names = {LIST4}\n\n\n# def search(names, target): loop with break, and else for not found\n# call search for "<<n3>>" and then for "<<missing>>"\n',
          f'names = {LIST4}\n\n\ndef search(names, target):\n    for name in names:\n        if name == target:\n            print("Found", name)\n            break\n    else:\n        print("No", target)\n\n\nsearch(names, "<<n3>>")\nsearch(names, "<<missing>>")\n',
          checks=[("fout", "search", [names, X["missing"]])], hints=["The else lines up with the for, not with the if.", "break skips the else."], emoji="🧭")

    c.add("infinite_loops", "Infinite Loops", "Never-ending loops", "recognise and fix infinite loops",
          [T("The scenario", "The program below is meant to count how many days the stock will last, but when you press Run **nothing ever comes back**. A loop that never ends is one of the most common beginner bugs, and your machine is fine: Python will be stopped for you after a few seconds."),
           T("Why loops never end", "Almost always one of these:\n\n- The condition's variable is **never updated** inside the body\n- It is updated **in the wrong direction** (adding when you should subtract)\n- The loop uses `while True` and nothing ever calls `break`\n\nWhen a program hangs, stare at the `while` condition and ask: *which line makes this False?*"),
           T("When infinite is on purpose", "Servers and games run `while True:` forever by design, with a `break` or an exit signal for when they are done. A good habit for learning: add a **safety counter** that breaks after a sensible maximum, so a mistake cannot hang your program."),
           Q("A while loop never ends. What is the first thing to check?", ["Whether the loop body changes the condition's variable", "Whether the computer is old", "Whether print is spelled correctly"], 0, "If nothing inside the loop can make the condition False, it runs forever."),
           P("n = 3\nwhile n > 0:\n    n -= 1\nprint(n)", "0", ["3", "-1"], "n goes 3, 2, 1, 0, and the loop stops when 0 > 0 is False.")],
          "Part one: the first loop never ends because `units` never goes down. Fix it so that **6 are sold per day** and it stops when none are left; it should print `Days: ` and the count. Part two: write a `while True` loop with a `break` that prints `Attempt 1`, `Attempt 2`, `Attempt 3` and then stops. It should print:\n\n<<OUT>>",
          "units = <<q1>>\ndays = 0\nwhile units > 0:\n    days += 1\nprint(\"Days:\", days)\n\n# Part two: while True with a break, printing Attempt 1 to Attempt 3\n",
          'units = <<q1>>\ndays = 0\nwhile units > 0:\n    days += 1\n    units -= 6\nprint("Days:", days)\n\nattempt = 0\nwhile True:\n    attempt += 1\n    print("Attempt", attempt)\n    if attempt == 3:\n        break\n',
          checks=[("var", "days", True), ("ast", "Break", "a break")], slow=True,
          hints=["Inside the first loop, units must go down by 6 each day.", "while True needs an if and a break inside it."], emoji="♾️")

    c.add("looping_patterns", "Common Looping Patterns", "Chapter 8 project", "apply the standard loop patterns",
          [T("The scenario", "Most loops you will ever write are one of a handful of patterns. Learn them once and you will recognise them everywhere: in reports, searches, clean-ups and checks."),
           T("The patterns", "- **Accumulator**: `total += x`\n- **Counter**: `count += 1` when something is true\n- **Tracker**: remember the biggest or smallest seen so far\n- **Filter**: collect only the items that pass a test (`items.append(x)`)\n- **Flag**: a True/False set once something is found\n- **Builder**: assemble a string or list as you go"),
           T("Choosing", "Before writing a loop, say which pattern it is out loud: \"I am **counting** the low ones\". That sentence tells you what to start, what to update, and what to print."),
           Q("Which pattern finds the biggest value in a list?", ["A tracker: remember the biggest so far", "A counter", "A flag"], 0, "Keep a variable holding the best seen so far and replace it when you meet a bigger one."),
           P("best = 0\nfor n in (4, 9, 2):\n    if n > best:\n        best = n\nprint(best)", "9", ["4", "15"], "best is replaced whenever a bigger value turns up, ending at 9.")],
          "Apply five patterns to the names and quantities. Using a loop over positions: add up the quantities (`total`), count those at or below `limit` (`low_count`), track the highest quantity and the name that has it (`top_name`, `top_qty`), and collect the low names in a list `low_names` with `append`. Print the five results as shown. It should print:\n\n<<OUT>>",
          f'names = {LIST4}\nquantities = {QS}\nlimit = min(quantities) + 5\ntotal = 0\nlow_count = 0\ntop_name = None\ntop_qty = 0\nlow_names = []\n# one loop over the positions applying all five patterns\n# print Total, Low count, Top, Low names (joined with ", ")\n',
          f'names = {LIST4}\nquantities = {QS}\nlimit = min(quantities) + 5\ntotal = 0\nlow_count = 0\ntop_name = None\ntop_qty = 0\nlow_names = []\nfor i in range(len(names)):\n    total += quantities[i]\n    if quantities[i] <= limit:\n        low_count += 1\n        low_names.append(names[i])\n    if quantities[i] > top_qty:\n        top_qty = quantities[i]\n        top_name = names[i]\nprint("Total:", total)\nprint("Low count:", low_count)\nprint("Top:", top_name, top_qty)\nprint("Low names:", ", ".join(low_names))\n',
          checks=[("var", "total"), ("var", "low_count", True), ("var", "top_name"), ("var", "low_names")], hints=["One loop can update several variables.", "\", \".join(low_names) turns a list of text into one line."], emoji="🧰")
