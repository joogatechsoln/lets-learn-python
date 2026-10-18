"""Chapter 1: Introduction to Python (12 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Introduction to Python")

    c.add("what_is_python", "What is Python?", "Hello, Python", "know what Python is and what it is used for",
          [T("The scenario", "<<opening>>"),
           T("What is Python?", "**Python** is a programming language: a way of giving a computer exact instructions in words that are close to English.\n\nYou write the instructions in a text file. A program called the **interpreter** reads the file from the **top to the bottom**, one line at a time, and does what each line says.\n\n```python\nprint(\"Hello\")\n```\n\nPython appeared in 1991. It is free, runs on almost every computer, and works fully offline, like this course."),
           T("What people use Python for", "Python is popular because it is easy to read, and because it can do a huge range of jobs:\n\n- **Websites and apps**, behind the scenes\n- **Data and spreadsheets**: cleaning, counting, charting\n- **Automation**: doing boring repeated work for you\n- **Artificial intelligence**: most AI tools are built with it\n\nAt **<<biz>>** that could mean:\n\n- <<use1>>\n- <<use2>>\n- <<use3>>"),
           T("How this course works", "Every lesson has the same rhythm:\n\n- A short **scenario** from your job\n- The **idea**, explained with a small example\n- A **prediction** or quiz, to check you understood\n- A **task** where you write or fix real code\n\nThe 3D window on the right is your **<<system>>**. It starts as a blueprint and fills in as you finish lessons. It also reacts to the code you run."),
           Q("In what order does Python run a file?", ["Top to bottom, one line at a time", "Bottom to top", "Whichever line it likes best"], 0,
             "Python follows your instructions in order, starting at line 1. That is why the order of your lines matters.")],
          "Python is waiting. The program below is already written. Press **Run** and watch the terminal on the left. It should print:\n\n<<OUT>>",
          '# Your very first program. Nothing to type: just press Run.\nprint("Python is running at <<biz>>")\nprint("Welcome to the <<system>>")\n',
          '# Your very first program. Nothing to type: just press Run.\nprint("Python is running at <<biz>>")\nprint("Welcome to the <<system>>")\n',
          hints=["Press the Run button under the editor, or Ctrl+Enter."], emoji="🐍", run_only=True)

    c.add("first_bug", "Your First Bug", "First bug", "know what a bug is and read a simple one",
          [T("The scenario", "Before you write more code, meet the thing every programmer meets every day: the **bug**. The <<system>> team left you a starter program. It does not work yet, and it is your job to find out why."),
           T("What is a bug?", "A **bug** is any mistake in a program. The word is old: in 1947 engineers found a real moth stuck in a computer and taped it into their logbook as the \"first actual case of a bug\".\n\nBugs come in two kinds:\n\n- **Loud bugs** stop the program and print an error message\n- **Silent bugs** run happily but give a wrong answer\n\nThis lesson is a loud one. Python is very good at telling you what it could not understand, so the skill is to *read* what it says."),
           T("Reading your first error", "When Python cannot find a name, it says so:\n\n```text\nTraceback (most recent call last):\n  File \"first.py\", line 1, in <module>\n    pritn(\"hello\")\nNameError: name 'pritn' is not defined\n```\n\nThe last line is the most useful. `NameError` is the kind of problem. `name 'pritn' is not defined` says which word Python did not recognise. Python does not guess that you meant `print`. It stops and asks you to fix it."),
           P('pritn("hello")', "!NameError", ["hello", 'pritn("hello")'], "Python has no function called `pritn`, so it stops with a NameError. It does not guess what you meant.")],
          "Press **Run** and read the error in the terminal. Fix the first bug, run again, and you will meet the second. When both are fixed the program prints:\n\n<<OUT>>",
          'pritn("The <<system>> is starting")\nPrint("All systems go")\n',
          'print("The <<system>> is starting")\nprint("All systems go")\n',
          hints=["The error names the word Python did not know. Compare it with the real name of the print function.", "Python is case sensitive. `Print` and `print` are different names."], emoji="🪲")

    c.add("hello_world", "Hello, world", "Hello, world", "show output with print()",
          [T("The scenario", "Every programmer's first program says hello. Yours will greet the team at **<<biz>>**, because a program that can talk can report anything: stock, temperatures, errors."),
           T("print() shows things", "`print()` writes a line of text on the screen. The text goes inside **quotes**. Text in quotes is called a **string**.\n\n```python\nprint(\"Hello, world!\")\nprint('Single quotes work too')\n```\n\nEach `print` starts a new line. An empty `print()` gives a blank line. Give `print` several things separated by commas and it puts a space between them:\n\n```python\nprint(\"Hello,\", \"world\")\n```"),
           T("Order matters", "Python runs your lines one after another, so the output comes out in the order you wrote it. If you want a line to appear first, write it first."),
           P('print("Hello,", "world")', "Hello, world", ["Hello,world", 'Hello, "world"'], "A comma between two things in `print` makes Python put one space between them. The quotes are not printed."),
           Q("What does an empty print() do?", ["Prints a blank line", "Stops the program", "Prints the word nothing"], 0, "`print()` with nothing inside just moves to a new line, which leaves a blank line. It is handy for spacing out a report.")],
          "Write a program that prints these four lines. The third line is blank:\n\n<<OUT>>",
          "# Print the four lines shown in the task\n",
          'print("Hello, world!")\nprint("Welcome to <<biz>>")\nprint()\nprint("<<system>> is online")\n',
          hints=["Each line is one print(...) call with the text in quotes.", "For the blank line use print() with nothing inside."], emoji="👋")

    c.add("adding_numbers", "Adding Numbers", "Operators", "do maths with operators",
          [T("The scenario", "<<delivery_note>> has arrived: <<d>> more than the <<q1>> you counted this morning. Python is a very good calculator, and <<biz>> needs it to be."),
           T("Operators", "Symbols that do something to numbers are called **operators**.\n\n- `+` add, `-` subtract\n- `*` multiply, `/` divide\n- `//` divide and drop the remainder\n- `%` the remainder only\n- `**` power\n\n```python\nprint(7 + 2)    # 9\nprint(7 * 2)    # 14\nprint(7 / 2)    # 3.5\nprint(7 // 2)   # 3\nprint(7 % 2)    # 1\n```\n\nNumbers have no quotes. `7` is a number, `\"7\"` is text."),
           T("Two kinds of number", "A whole number like `24` is an **int**. A number with a decimal point like `4.5` is a **float**. Normal division with `/` always gives a float, even when it divides evenly: `8 / 2` is `4.0`."),
           P("print(7 // 2, 7 % 2)", "3 1", ["3.5 1", "3 3"], "`//` gives how many whole times 2 fits into 7 (that is 3). `%` gives what is left over (1).")],
          "Print four results, one per line, using only numbers and operators:\n\n- <<q1>> plus the delivery of <<d>>\n- <<q1>> minus 5\n- <<q1>> multiplied by <<p1>>\n- <<q1>> divided by 4\n\nYou should see:\n\n<<OUT>>",
          "# Four print lines, one for each calculation\n",
          "print(<<q1>> + <<d>>)\nprint(<<q1>> - 5)\nprint(<<q1>> * <<p1>>)\nprint(<<q1>> / 4)\n",
          hints=["Write the maths inside the brackets: print(10 + 5).", "Do not put quotes around the maths, or Python prints it as text instead of calculating it."], emoji="➕")

    c.add("order_of_operations", "Order of Operations", "Order of operations", "predict the order Python calculates in",
          [T("The scenario", "The owner's calculator keeps giving odd answers. She types `<<q1>> + <<d>> * <<p1>>` and expects the new total to be valued at <<p1>> each. Something about the order is off."),
           T("Who goes first?", "Python follows the same rules as school maths. In order:\n\n- **Brackets** `( )`\n- **Powers** `**`\n- **Multiply and divide** `*  /  //  %`, left to right\n- **Add and subtract** `+  -`, left to right\n\n```python\nprint(2 + 3 * 4)     # 14, because 3 * 4 goes first\nprint((2 + 3) * 4)   # 20, brackets go first\nprint(10 - 4 - 3)    # 3, left to right\n```"),
           T("When in doubt, add brackets", "Brackets cost nothing and make your meaning obvious to Python and to the next person who reads the code. If a calculation does not need them, they do no harm."),
           P("print(10 - 4 - 3)", "3", ["9", "11"], "Same-level operators run left to right: 10 - 4 is 6, then 6 - 3 is 3. Not 10 - (4 - 3)."),
           Q("What is 2 + 3 * 4 in Python?", ["14", "20", "24"], 0, "Multiplication goes before addition, so it is 2 + 12.")],
          "Both lines below calculate the wrong thing because of the order. Add brackets so the program prints:\n\n<<OUT>>\n\nThe first line is the **new stock** (<<q1>> plus <<d>>) valued at <<p1>> each. The second is the **average** of <<q1>> and <<q2>>.",
          "# The new stock, valued at <<p1>> each\nprint(<<q1>> + <<d>> * <<p1>>)\n# The average of the first two <<things>>\nprint(<<q1>> + <<q2>> / 2)\n",
          "# The new stock, valued at <<p1>> each\nprint((<<q1>> + <<d>>) * <<p1>>)\n# The average of the first two <<things>>\nprint((<<q1>> + <<q2>>) / 2)\n",
          hints=["Which addition needs to happen before the multiplication?", "Put brackets around the sum, not around the whole line."], emoji="🧮")

    c.add("commenting", "The Art of Commenting", "Commenting", "write helpful comments and disable code",
          [T("The scenario", "A colleague will take over your report next month, and the report still has a leftover debugging line that must not be shared. Good programmers leave notes for the next reader, and switch lines off without deleting them."),
           T("Comments", "A **comment** starts with `#`. Python ignores everything after it on that line.\n\n```python\n# Calculate the value of one product\nprint(24 * 4.5)   # a comment can also follow code\n```\n\nGood comments explain **why**, not what. `# add 1` is useless. `# the new item counts too` is useful."),
           T("Switching code off", "Putting `#` in front of a line **comments it out**: Python skips it, but the line is still there if you need it again.\n\n```python\nprint(\"Keep me\")\n# print(\"Skip me\")\n```\n\nProgrammers do this all the time while testing."),
           P('print("A")\n# print("B")\nprint("C")', "A\nC", ["A\nB\nC", "A\n# print(\"B\")\nC"], "The line starting with `#` is ignored completely, so only A and C are printed."),
           Q("What is a good comment?", ["One that explains why the code does something", "One that repeats the code in English", "One that is as long as possible"], 0, "Code already says *what* it does. A comment is most useful when it says *why*.")],
          "Fix the program for the next reader:\n\n- Comment out the `DEBUG` line so it stops printing\n- Add a comment on its own line above each of the two value calculations, saying what it calculates\n\nThe output should be:\n\n<<OUT>>",
          '# <<system>> daily report\nprint("Report for <<biz>>")\nprint(<<q1>> * <<p1>>)\nprint("DEBUG: remove before sharing")\nprint(<<q2>> * <<p2>>)\n',
          '# <<system>> daily report\nprint("Report for <<biz>>")\n# Value of the first <<thing>>\nprint(<<q1>> * <<p1>>)\n# print("DEBUG: remove before sharing")\n# Value of the second <<thing>>\nprint(<<q2>> * <<p2>>)\n',
          checks=[("comments", 4)], hints=["Put a # at the very start of the DEBUG line.", "Comments must be on their own lines to count. Write # then your note."], emoji="💬")

    c.add("syntax_errors", "Syntax Errors", "Syntax", "read and fix a SyntaxError",
          [T("The scenario", "A teammate pasted three lines of code into the chat. When you run them, nothing happens except an angry message. Time to learn what Python is complaining about."),
           T("What is a syntax error?", "**Syntax** is the grammar of Python. A **SyntaxError** means Python could not even read the line, so it ran **nothing** from the file.\n\n```text\n  File \"report.py\", line 1\n    print(\"Hello)\n          ^\nSyntaxError: unterminated string literal (detected at line 1)\n```\n\nRead it like a detective:\n\n- `line 1` says where to look\n- the `^` points at the trouble\n- the last line says what Python thinks is wrong"),
           T("The usual suspects", "- A **quote** that is never closed\n- A **bracket** `(` that is never closed\n- A missing **comma** between things\n- A missing **colon** or bad spaces at the start of a line (you will meet these soon)\n\nThe real mistake is often at the end of the line above the one Python points at. Look just before the arrow too."),
           Q("What is missing from this line?\n\n```python\nprint(\"Total:\", 5\n```", ["A closing quote", "A closing bracket )", "A colon"], 1, "The `(` after print is never closed. Python says `'(' was never closed`."),
           P('print("Hi")\nprint("Oops)', "!SyntaxError", ["Hi\nOops", "Hi"], "Python reads the whole file first. Because line 2 has a syntax error, **nothing** runs, not even line 1.")],
          "The three lines each have a different syntax error. Python reports **one at a time**, so fix, run, read, repeat. When all three are fixed it prints:\n\n<<OUT>>",
          'print("Opening the <<system>>)\nprint("Units:", <<q1>>\nprint("Value:" <<q1>> * <<p1>>)\n',
          'print("Opening the <<system>>")\nprint("Units:", <<q1>>)\nprint("Value:", <<q1>> * <<p1>>)\n',
          hints=["Line 1: what is missing at the end of the text?", "Line 2: count the opening and closing brackets.", "Line 3: two things inside print need something between them."], emoji="✏️")

    c.add("reading_the_traceback", "Reading the Traceback", "Traceback", "read a traceback from the bottom up",
          [T("The scenario", "Yesterday's report crashed at closing time and nobody could tell why. The error message was right there on the screen, and nobody read it. You will not make that mistake."),
           T("Anatomy of a traceback", "When code crashes, Python prints a **traceback**: the trail of what it was doing.\n\n```text\nTraceback (most recent call last):\n  File \"report.py\", line 3, in <module>\n    per_day = 120 / days\nZeroDivisionError: division by zero\n```\n\n- `File ... line 3` tells you where\n- the next line shows the code itself\n- the **last line** names the error and what went wrong\n\nAlways read it from the **bottom up**: what, then where."),
           T("Errors you will meet", "- `NameError`: a name Python does not know (often a typo)\n- `TypeError`: the wrong kinds of things combined, like text plus a number\n- `ValueError`: the right kind of thing but a bad value, like `int(\"abc\")`\n- `ZeroDivisionError`: dividing by zero\n\nThe **explain** panel in the terminal will help you with each one."),
           Q("Look at this traceback. Which line of the file is blamed?\n\n```text\nTraceback (most recent call last):\n  File \"check.py\", line 3, in <module>\n    result = total / days\nZeroDivisionError: division by zero\n```", ["Line 1", "Line 3", "Line 4"], 1, "The traceback says `line 3` and shows the code on that line. The last line says what kind of error it is."),
           P("print(10 / 0)", "!ZeroDivisionError", ["0", "inf"], "Dividing by zero is not allowed in Python, so it stops with a ZeroDivisionError.")],
          "This program crashes. Run it, read the traceback **from the bottom**, and find the cause. The period was **4 days**. When it works, it prints:\n\n<<OUT>>",
          'days = 0\nprint("Stock check for <<biz>>")\nper_day = <<q1>> / days\nprint(per_day)\n',
          'days = 4\nprint("Stock check for <<biz>>")\nper_day = <<q1>> / days\nprint(per_day)\n',
          hints=["The last line names the error. Which number is on the bottom of the division?", "`days = 0` sets a name to a value (variables get a full chapter soon). Change the value."], emoji="🔍")

    c.add("hunting_the_bug", "Hunting the Bug", "Bug hunt", "find silent bugs by printing values",
          [T("The scenario", "No error this time. The program runs happily and prints a number, and the number is wrong. Silent bugs are the hardest kind, because Python thinks everything is fine."),
           T("Trace it like a detective", "When there is no traceback, you create your own clues:\n\n- **Predict**: work out by hand what the answer *should* be\n- **Look**: `print` the values on the way, to see what Python really holds\n- **Compare**: find the first value that is not what you expected\n- **Fix** that one thing, then run again\n\n```python\nprint(\"DEBUG opening:\", opening)\n```\n\nPrinting values to look inside a program is called **print debugging**. It is simple and professionals use it every day."),
           T("Tidy up afterwards", "Debug prints are scaffolding. Once the bug is fixed, delete them or comment them out, so the report only shows what it should."),
           Q("The program prints 6 but you expect 44. What is the smartest next step?", ["Print the values it uses and compare them with what you expected", "Rewrite the whole program", "Add more numbers until it looks right"], 0, "Find the **first** value that is wrong. The bug is at or just before that line."),
           P('a = 10\nb = 4\nprint("DEBUG", a - b)\nprint(a + b)', "DEBUG 6\n14", ["14", "DEBUG 14\n6"], "Both prints run in order. The debug line shows 10 - 4 = 6, then the real result is 14.")],
          "The closing count of <<n1>> should be the opening count (<<q1>>) **plus** the delivery (<<d>>). The program prints the wrong number with no error.\n\n- Add `print` lines to look at the values\n- Find **both** bugs and fix them\n- The last line printed must be `Closing: <<final>>`",
          'opening = <<q2>>\ndelivery = <<d>>\nclosing = opening - delivery\nprint("Closing:", closing)\n',
          'opening = <<q1>>\ndelivery = <<d>>\nprint("DEBUG opening:", opening)\nclosing = opening + delivery\nprint("Closing:", closing)\n',
          checks=[("prints", 2)], last_only=True,
          hints=["Add print(opening) and print(delivery) before the calculation. Do the numbers match the task?", "There are two bugs: one wrong number and one wrong operator."], emoji="🕵️")

    c.add("testing_vs_deploying", "Testing vs. Deploying", "Test and deploy", "test code on sample data before using it for real",
          [T("The scenario", "Every program has two lives. In the first you **test** it with made-up numbers where you know the answer. In the second you **deploy** it: it runs on the real data, and people rely on it. A bug found in testing costs nothing. A bug found after deploying can cost real money."),
           T("assert: a one-line test", "`assert` checks that something is true. If it is not, the program stops with an **AssertionError** and your message.\n\n```python\nassert 2 + 2 == 4, \"Maths is broken\"   # passes quietly\nassert 2 + 2 == 5, \"Maths is broken\"   # stops here\n```\n\nNote `==` means **is equal to**. A single `=` stores a value."),
           T("A safe order", "1. **Test** the calculation on sample data where you know the answer\n2. **Fix** until every test passes\n3. **Deploy**: run it on the real data\n\nBecause Python stops at a failed `assert`, anything written after it is protected. It only runs if the tests passed."),
           P('assert 2 + 2 == 5, "Maths is broken"\nprint("Deployed")', "!AssertionError", ["Deployed", "Maths is broken"], "The assert fails, so the program stops. The `print` after it never runs. That is exactly how a test protects a deployment."),
           Q("Why does the program stop at a failing assert?", ["The condition was False, so something is wrong and it is not safe to continue", "assert always stops the program", "Python found a typo"], 0, "assert passes silently when the condition is True and stops the program when it is False.")],
          "The sample test below fails because of a bug in the calculation. 10 units at 2.5 each should be worth 25.0.\n\n- Run it and read the AssertionError\n- Fix the bug in the **calculation**, not the test\n- When the test passes, the deploy section runs. It prints:\n\n<<OUT>>",
          '# --- TEST: sample data where we know the answer ---\nsample_units = 10\nsample_price = 2.5\nsample_value = sample_units + sample_price\nassert sample_value == 25.0, "Test failed: value is wrong"\nprint("Test passed")\n\n# --- DEPLOY: only reached if the test passed ---\nprint("Deploying <<system>> to <<biz>>")\nprint("Live value:", <<q1>> * <<p1>>)\n',
          '# --- TEST: sample data where we know the answer ---\nsample_units = 10\nsample_price = 2.5\nsample_value = sample_units * sample_price\nassert sample_value == 25.0, "Test failed: value is wrong"\nprint("Test passed")\n\n# --- DEPLOY: only reached if the test passed ---\nprint("Deploying <<system>> to <<biz>>")\nprint("Live value:", <<q1>> * <<p1>>)\n',
          hints=["The test says the value should be 25.0 when you have 10 units at 2.5 each. Which operator gives that?", "Never change the expected value in the test to match a wrong answer."], emoji="🧪")

    c.add("data_types_trap", "The Data Types Trap", "Data types", "keep numbers and text apart",
          [T("The scenario", "<<delivery_note>> is typed into a form, and forms hand everything to your program as **text**, even digits. The report adds it to the opening count, and Python refuses. Mixing up numbers and text is one of the most common beginner traps."),
           T("Numbers vs text", "`\"5\"` in quotes is **text**. `5` without quotes is a **number**. They look alike and behave very differently:\n\n```python\nprint(5 + 3)        # 8\nprint(\"5\" + \"3\")    # 53   (text is joined)\nprint(\"5\" + 3)      # TypeError\n```\n\nPlus on numbers adds. Plus on text **joins**. Plus on one of each is an error."),
           T("Converting", "- `int(\"5\")` turns text into a whole number\n- `float(\"4.5\")` turns text into a decimal\n- `str(5)` turns a number into text\n- `type(5)` tells you what something is\n\n```python\nprint(int(\"5\") + 3)       # 8\nprint(\"Count: \" + str(5)) # Count: 5\n```"),
           P('print("5" + "3")', "53", ["8", "!TypeError"], "Both are text, so `+` joins them into the text 53. It does no maths."),
           Q("Which line works?", ["print(\"Total: \" + str(5))", "print(\"Total: \" + 5)", "print(5 + \"3\")"], 0, "`str(5)` makes the number into text first, so both sides are text and can be joined.")],
          "Both lines at the bottom mix text and numbers. Fix them so the program prints:\n\n<<OUT>>\n\nThe delivery arrived as text. The label needs the opening count turned into text.",
          '# <<delivery_note>> arrives as text\ndelivery = "<<d>>"\nopening = <<q1>>\nprint("New total:", opening + delivery)\nprint("Label: " + opening)\n',
          '# <<delivery_note>> arrives as text\ndelivery = "<<d>>"\nopening = <<q1>>\nprint("New total:", opening + int(delivery))\nprint("Label: " + str(opening))\n',
          hints=["Line 4: the delivery is text. Which function turns text into a number?", "Line 5: the label is text, so the number needs to become text."], emoji="🔤")

    c.add("blank_slate", "The Blank Slate", "Chapter 1 project", "write a small program from scratch",
          [T("The scenario", "Chapter one is done, and there is no starter code this time. A real report is waiting for **<<biz>>**, and you have every tool you need: `print`, operators, brackets, comments, and the sense to check your output."),
           T("A plan beats a guess", "Before typing, read the five lines you must produce and decide how each one is made. Which are plain text? Which need a calculation? Which need brackets?\n\nBuild it **one line at a time**, running after each. When a line misbehaves you will know exactly which one."),
           T("Checklist", "- Every line shows exactly what the task asks for\n- Brackets where the order of operations needs them\n- At least two comments of your own, on their own lines\n- No leftover debug lines")],
          "Write the whole program yourself. It must print these five lines exactly:\n\n<<OUT>>\n\nThe last value is the **new** stock (<<q1>> plus <<d>>) times <<p1>>. Add at least two comment lines of your own.",
          "# Blank slate: write the whole program yourself.\n# Aim: print the five lines shown in the task.\n",
          '# Blank slate: write the whole program yourself.\n# Aim: print the five lines shown in the task.\n# Banner\nprint("=== <<system>> for <<biz>> ===")\nprint("First <<thing>>: <<n1>>")\n# Opening count and the delivery\nprint("Opening:", <<q1>>)\nprint("After <<delivery_note>>:", <<q1>> + <<d>>)\n# Value of the new stock, with brackets so the order is right\nprint("Value:", (<<q1>> + <<d>>) * <<p1>>)\n',
          checks=[("prints", 5), ("comments", 4)],
          hints=["Use print(\"text\", number) to mix words and a calculation on one line.", "The last line needs brackets: (opening + delivery) * price.", "Two comments are already in the starter. Add two more of your own."], emoji="📄")
