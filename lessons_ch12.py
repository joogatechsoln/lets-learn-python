"""Chapter 12: Errors (15 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Errors")
    X = c.ctx
    VREAD = X["vread"]
    q1, d = X["q1"], X["d"]

    c.add("intro_errors", "Introduction to Errors and Exceptions", "Errors", "tell the three kinds of error apart",
          [T("The scenario", "Every program the <<system>> team has ever shipped has had errors. The difference between a beginner and a professional is not avoiding them: it is knowing **what kind** each one is, because the kind tells you where to look."),
           T("Three kinds", "- **Syntax errors**: the code is written wrongly, so Python cannot even start. Nothing runs\n- **Runtime errors** (exceptions): the code is valid but fails while running, like dividing by zero. Everything before the failing line has already run\n- **Logical errors**: the code runs to the end and gives the **wrong answer**. No message at all\n\nSyntax errors are the easiest to find and logical errors the hardest."),
           T("What is an exception?", "When something goes wrong at runtime, Python **raises an exception**: an object that describes the problem (`ZeroDivisionError`, `KeyError`, ...). If nothing **handles** it, the program stops and prints a traceback. This chapter ends with you handling and raising exceptions yourself."),
           P('print("start")\nprint(1 / 0)', "!ZeroDivisionError", ["start", "start\n0"], "\"start\" is printed first, and then the division raises a ZeroDivisionError and the program stops."),
           Q("A program runs without any message but prints a wrong total. What kind of error is it?", ["A logical error", "A syntax error", "A runtime error"], 0, "No crash and a wrong answer is a logical error.")],
          "Classify three situations by setting the variables `kind_a`, `kind_b` and `kind_c` to `\"syntax\"`, `\"runtime\"` or `\"logic\"`, then print them. It should print:\n\n<<OUT>>\n\n- a: Python refuses to start a file because a bracket is never closed\n- b: the program prints a total that is 10 too small, with no message\n- c: the program stops halfway through with `KeyError: '<<missing>>'`",
          'kind_a = ""\nkind_b = ""\nkind_c = ""\nprint(kind_a, kind_b, kind_c)\n',
          'kind_a = "syntax"\nkind_b = "logic"\nkind_c = "runtime"\nprint(kind_a, kind_b, kind_c)\n',
          checks=[("var", "kind_a"), ("var", "kind_b"), ("var", "kind_c")], hints=["Does anything run at all in case a?", "Case b has no error message, so what kind is it?"], emoji="🧭")

    c.add("syntax_errors_review", "Syntax Errors", "Syntax", "find and fix syntax errors quickly",
          [T("The scenario", "A colleague's script will not start. You have met syntax errors in chapter one. Now you will find them faster, by knowing **where** Python usually points and which mistakes cause which message."),
           T("Messages and causes", "- `SyntaxError: expected ':'` a missing colon after `def`, `if`, `for`, `while`\n- `SyntaxError: '(' was never closed` an opening bracket without its partner\n- `IndentationError: expected an indented block` a body that is not indented\n- `SyntaxError: invalid syntax` often a missing comma, a stray symbol or `=` where `==` was meant\n\nPython reports the **first** problem it finds, and the true mistake is often on the line **above** the one it shows."),
           P("def f()\n    return 1", "!SyntaxError", ["1", "None"], "A def line must end with a colon. Nothing runs when the file has a syntax error."),
           Q("Python points at line 6 for \"'(' was never closed\". Where is the real mistake?", ["On the line with the opening bracket, earlier", "Always on line 6", "On the last line of the file"], 0, "Look for the opening bracket that is missing its partner.")],
          "The script has three syntax errors, one after the other. Fix them all so it prints:\n\n<<OUT>>",
          'def total(a, b)\n    return a + b\n\n\nvalues = [1, 2, 3\nfor v in values:\nprint(total(v, <<d>>))\n',
          'def total(a, b):\n    return a + b\n\n\nvalues = [1, 2, 3]\nfor v in values:\n    print(total(v, <<d>>))\n',
          hints=["The def line needs a colon.", "The list is never closed.", "The loop body must be indented."], emoji="✏️")

    c.add("runtime_errors", "Runtime Errors", "Runtime", "understand errors that appear while running",
          [T("The scenario", "The report prints a banner, starts on the readings, and then crashes on the third one. Everything before the crash ran fine. That is the signature of a runtime error: valid code, bad situation."),
           T("Runtime means \"while it runs\"", "Python only meets the failing line when it gets there. So:\n\n- output **before** the crash is real and stays on screen\n- the same code may work on some data and fail on other data\n- the traceback names the line, and the last line names the problem\n\nThe fix is to deal with the **situation** the line cannot handle, here a zero in the data, or to remove it earlier."),
           P('for r in [2, 0, 4]:\n    print(8 / r)', "!ZeroDivisionError", ["4.0\n0\n2.0", "4.0"], "It prints 4.0 for the first reading, then the division by 0 raises the error. The question is about the error that ends it."),
           Q("Why did the first lines print before the program crashed?", ["Python runs line by line and only fails when it reaches the bad line", "The crash was a syntax error", "Python guessed wrongly"], 0, "Runtime errors happen at the moment the bad line runs.")],
          "The loop crashes on the zero reading. Make it **skip** zero readings with an `if`, so it prints the result for the others. It should print:\n\n<<OUT>>",
          'readings = [4.0, 2.0, 0, 8.0]\nprint("Start")\nfor r in readings:\n    print(16 / r)\nprint("End")\n',
          'readings = [4.0, 2.0, 0, 8.0]\nprint("Start")\nfor r in readings:\n    if r == 0:\n        continue\n    print(16 / r)\nprint("End")\n',
          hints=["Check r == 0 before dividing.", "continue jumps straight to the next reading."], emoji="💥")

    c.add("logical_errors", "Logical Errors", "Logic", "find errors that give no message",
          [T("The scenario", "The program has been running for a week. It never crashed. But the stock numbers are slightly off, and nobody noticed until the audit. This is the dangerous kind: **the code does exactly what you wrote, which is not what you meant**."),
           T("Where logic bugs hide", "- **Off by one**: `range(n)` when you needed `range(1, n + 1)`\n- **Wrong comparison**: `<` where `<=` was meant\n- **Wrong operator**: `/` where `//` was meant\n- **Wrong variable**: using `total` where you meant `count`\n- **Order of operations**: a missing bracket"),
           T("How to find them", "Work out the right answer **by hand** for a small case, then print the values along the way and find the first one that disagrees. Tests (chapter five) catch these automatically."),
           P("total = 0\nfor n in range(1, 4):\n    total += n\nprint(total)", "6", ["10", "3"], "range(1, 4) is 1, 2, 3, which add to 6. Using range(4) would have given 0 + 1 + 2 + 3, also 6, so the bug is often a start or end that is off by one."),
           Q("What is the best first step for a logical error?", ["Work out the right answer by hand and compare", "Add more code", "Read the traceback"], 0, "There is no traceback. You need to know what the answer should be.")],
          "Three logic bugs make the output wrong, with no error. Fix all three so it prints:\n\n<<OUT>>\n\nThe sum should include 1 to 5, the check should treat a count **equal** to <<level>> as low, and the average must be a true decimal.",
          'total = 0\nfor n in range(1, 5):\n    total += n\nprint("Sum:", total)\ncount = <<level>>\nif count < <<level>>:\n    print("LOW")\nelse:\n    print("OK")\nprint("Average:", (<<q1>> + <<d>>) // 2)\n',
          'total = 0\nfor n in range(1, 6):\n    total += n\nprint("Sum:", total)\ncount = <<level>>\nif count <= <<level>>:\n    print("LOW")\nelse:\n    print("OK")\nprint("Average:", (<<q1>> + <<d>>) / 2)\n',
          hints=["range(1, 5) stops before 5.", "Which comparison includes equality?", "// drops the decimals. / does not."], emoji="🧩")

    c.add("common_exceptions", "Common Python Exceptions", "Common exceptions", "recognise the usual exceptions",
          [T("The scenario", "Most errors you will ever meet come from a short list. Knowing the list by heart means you often understand a traceback from the **last line alone**."),
           T("The usual suspects", "- `NameError`: a name that does not exist (typo, or used too early)\n- `TypeError`: the wrong type, like text plus a number\n- `ValueError`: right type, bad value, like `int(\"abc\")`\n- `KeyError`: a dictionary key that is not there\n- `IndexError`: a list position that does not exist\n- `ZeroDivisionError`: dividing by zero\n- `AttributeError`: an object has no such attribute or method\n- `FileNotFoundError`, `ImportError`, `RecursionError`, `AssertionError`"),
           T("Match message to cause", "`KeyError: 'c'` names the missing key. `IndexError: list index out of range` means the position is past the end. `ValueError: invalid literal for int() with base 10: 'abc'` shows the text that could not be converted. The message is the clue."),
           P('items = ["x", "y"]\nprint(items[2])', "!IndexError", ["y", "None"], "Positions are 0 and 1, so 2 does not exist."),
           Q("`ValueError: invalid literal for int()` means...", ["The right type but a value that cannot be converted", "A missing dictionary key", "A misspelt name"], 0, "The text was a string, but not one that looks like a whole number.")],
          "Four lines fail with four different exceptions. Fix each line (not by deleting it) so the program prints:\n\n<<OUT>>",
          'data = {"a": 1, "b": 2}\nitems = ["x", "y"]\nprint(data["c"])\nprint(items[2])\nprint(int("abc"))\nprint("n: " + 5)\n',
          'data = {"a": 1, "b": 2}\nitems = ["x", "y"]\nprint(data["b"])\nprint(items[1])\nprint(int("12"))\nprint("n: " + str(5))\n',
          hints=["KeyError: the key c is not in the dictionary.", "IndexError: the list only has positions 0 and 1.", "ValueError needs a string of digits.", "TypeError: str(5) makes the number into text."], emoji="📚")

    c.add("tracebacks_deep", "Understanding Tracebacks", "Tracebacks", "read tracebacks through several functions",
          [T("The scenario", "In real programs a crash happens deep inside functions that call functions. The traceback is a **trail**, and reading it well takes you straight to the line to fix."),
           T("The trail", "```text\nTraceback (most recent call last):\n  File \"app.py\", line 9, in <module>\n    report()\n  File \"app.py\", line 6, in report\n    return per_item(total, count)\n  File \"app.py\", line 2, in per_item\n    return total / count\nZeroDivisionError: division by zero\n```\n\nRead it **bottom to top**: the last line is the error, the line above is where it happened, and each earlier entry is the caller. Fix the error where its **cause** is, which is often a caller higher up, not the last line."),
           Q("In the trail above, which function actually divided?", ["per_item", "report", "The main program"], 0, "The bottom frame is where the exception was raised.")],
          "The chain of three functions crashes with a `ZeroDivisionError` in `per_item`, but the real cause is higher up: `batch_count` returns 0. Fix the **cause** so the program prints:\n\n<<OUT>>",
          'def per_item(total, count):\n    return total / count\n\n\ndef batch_count(units, size):\n    return units // size\n\n\ndef report():\n    count = batch_count(<<q1>>, <<q1>> + 1)\n    return per_item(<<q1>>, count)\n\n\nprint(report())\n',
          'def per_item(total, count):\n    return total / count\n\n\ndef batch_count(units, size):\n    return units // size\n\n\ndef report():\n    count = batch_count(<<q1>>, 1)\n    return per_item(<<q1>>, count)\n\n\nprint(report())\n',
          hints=["Follow the trail up: where does count come from?", "A batch size bigger than the units gives 0 batches."], emoji="🔎")

    c.add("try_except", "Handling Exceptions with try and except", "try / except", "handle an exception instead of crashing",
          [T("The scenario", "The delivery notes are typed in by hand. Usually the entry is a number, but sometimes it says `n/a`. One bad entry must **not** bring down the whole report. You can ask Python to try risky code and say what to do if it fails."),
           T("try and except", "```python\ntry:\n    age = int(\"abc\")\nexcept ValueError:\n    age = 0\nprint(age)      # 0\n```\n\n- the `try` block runs normally\n- if it raises a `ValueError`, Python jumps to `except ValueError`\n- if nothing goes wrong, the `except` block is skipped\n\nName the **specific** error you expect, so real surprises still show up."),
           P('try:\n    int("abc")\nexcept ValueError:\n    print("oops")\nprint("done")', "oops\ndone", ["done", "!ValueError"], "The error is caught, \"oops\" prints, and the program carries on."),
           Q("What happens to the rest of the try block after an error?", ["It is skipped", "It still runs", "It runs twice"], 0, "Python leaves the try block at the first exception.")],
          "Write `<<vread>>(text)` that turns the text into a whole number and returns it, or returns `0` if the text is not a number. Then print the result for `\"<<d>>\"`, for `\"n/a\"` and for an empty string. It should print:\n\n<<OUT>>",
          "# def <<vread>>(text): try int(text), return 0 on ValueError\n# print <<vread>>(\"<<d>>\"), <<vread>>(\"n/a\") and <<vread>>(\"\")\n",
          'def <<vread>>(text):\n    try:\n        return int(text)\n    except ValueError:\n        return 0\n\n\nprint(<<vread>>("<<d>>"))\nprint(<<vread>>("n/a"))\nprint(<<vread>>(""))\n',
          checks=[("ast", "Try", "try / except"), ("ftest", VREAD, [[[str(d)], d], [["n/a"], 0], [[""], 0]])], hints=["return int(text) goes inside try.", "except ValueError: return 0"], emoji="🛟")

    c.add("multiple_exceptions", "Handling Multiple Exceptions", "More than one error", "handle several kinds of error",
          [T("The scenario", "A ratio function can fail in two ways: the divisor is zero, or someone passes text. Each needs its own response. Python lets you list several `except` blocks, or catch a group of errors with one."),
           T("Several except blocks", "```python\ntry:\n    result = a / b\nexcept ZeroDivisionError:\n    result = None\nexcept TypeError:\n    result = -1\n```\n\nPython checks the blocks **in order** and runs the first that matches. To treat two errors the same, put them in a tuple: `except (TypeError, ValueError):`."),
           T("Getting the error itself", "```python\nexcept ValueError as e:\n    print(\"Problem:\", e)\n```\n\n`as e` gives you the exception object, whose text is the message. `except Exception` catches almost everything, so use it only as a last resort."),
           P('try:\n    print(1 / 0)\nexcept ZeroDivisionError:\n    print("zero")\nexcept TypeError:\n    print("type")', "zero", ["type", "!ZeroDivisionError"], "The first matching except block runs."),
           Q("How do you handle ValueError and TypeError the same way?", ["except (ValueError, TypeError):", "except ValueError, TypeError:", "except ValueError and TypeError:"], 0, "A tuple of exception types in brackets catches either.")],
          "Write `safe_ratio(a, b)` that returns `a / b`, returns `None` when `b` is zero, and returns `-1` when the arguments are the wrong type. Print `safe_ratio(<<q1>>, 4)`, `safe_ratio(<<q1>>, 0)` and `safe_ratio(\"<<q1>>\", 4)`. It should print:\n\n<<OUT>>",
          "# def safe_ratio(a, b): handle ZeroDivisionError and TypeError separately\n# print the three results\n",
          'def safe_ratio(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None\n    except TypeError:\n        return -1\n\n\nprint(safe_ratio(<<q1>>, 4))\nprint(safe_ratio(<<q1>>, 0))\nprint(safe_ratio("<<q1>>", 4))\n',
          checks=[("ftest", "safe_ratio", [[[6, 3], 2.0], [[1, 0], None], [["a", 1], -1]])], hints=["Two except blocks, one for each error type.", "The return values are the ratio, None and -1."], emoji="🧯")

    c.add("else_clause", "The else Clause", "try / else", "run code only when nothing went wrong",
          [T("The scenario", "After a successful conversion the program should log the value, but if the conversion failed there is nothing to log. Putting the logging inside `try` would also hide errors in the logging itself. The `else` clause is for exactly this."),
           T("try / except / else", "```python\ntry:\n    value = float(text)\nexcept ValueError:\n    print(\"bad\")\nelse:\n    print(\"ok\", value)\n```\n\nThe `else` block runs **only if the try block raised nothing**. Keep the `try` block as small as possible (just the risky line) and put the follow-up work in `else`, so an error in it is not caught by mistake."),
           P('try:\n    x = int("5")\nexcept ValueError:\n    print("bad")\nelse:\n    print("ok", x)', "ok 5", ["bad", "ok"], "No error, so else runs."),
           Q("When does the else block of a try statement run?", ["When the try block raised no exception", "When an exception was raised", "Always"], 0, "else means \"no error happened\".")],
          "Write `convert(text)` that prints `bad: ` and the text when it is not a decimal number, and prints `ok: ` and the number when it is, using `else`. Call it for `\"<<sread>>\"`, `\"n/a\"` and `\"<<p1>>\"`. It should print:\n\n<<OUT>>",
          "# def convert(text): try float(text), except ValueError: print bad, else: print ok\n# call it for \"<<sread>>\", \"n/a\" and \"<<p1>>\"\n",
          'def convert(text):\n    try:\n        value = float(text)\n    except ValueError:\n        print("bad:", text)\n    else:\n        print("ok:", value)\n\n\nconvert("<<sread>>")\nconvert("n/a")\nconvert("<<p1>>")\n',
          checks=[("fout", "convert", ["n/a"])], hints=["The risky line is float(text) only.", "else comes after all the except blocks."], emoji="➡️")

    c.add("finally_clause", "The finally Clause", "finally", "run cleanup code no matter what",
          [T("The scenario", "A job opens a connection, does some work and must always close it, whether the work succeeded or crashed. Cleanup that depends on remembering to do it on every path is cleanup that will eventually be forgotten."),
           T("finally", "```python\ntry:\n    print(\"working\")\n    int(\"x\")\nexcept ValueError:\n    print(\"problem\")\nfinally:\n    print(\"cleanup\")\n```\n\nThe `finally` block runs **always**: after success, after a handled error, and even when an error is not handled and the program is about to crash. Use it to release things: close files, stop timers, write the log line."),
           P('try:\n    print("a")\nfinally:\n    print("b")\nprint("c")', "a\nb\nc", ["a\nc", "a\nb"], "finally runs after the try block, and then the program continues."),
           Q("When does a finally block run?", ["Always, error or not", "Only after an error", "Only if there is no error"], 0, "That is its whole purpose.")],
          "Write `process(text)` that prints `start`, tries `int(text)` and prints the number, prints `bad value` on a `ValueError`, and **always** prints `done` at the end. Call it for `\"<<d>>\"` and for `\"x\"`. It should print:\n\n<<OUT>>",
          "# def process(text): print start; try int(text) and print it; except ValueError: print bad value; finally: print done\n# call process(\"<<d>>\") and process(\"x\")\n",
          'def process(text):\n    print("start")\n    try:\n        print(int(text))\n    except ValueError:\n        print("bad value")\n    finally:\n        print("done")\n\n\nprocess("<<d>>")\nprocess("x")\n',
          checks=[("fout", "process", ["x"])], hints=["finally comes last, after the except block.", "It prints done for both calls."], emoji="🧹")

    c.add("raise_exceptions", "Raising Exceptions with raise", "raise", "raise your own exceptions",
          [T("The scenario", "Your own functions should refuse nonsense: a negative stock count must be rejected loudly, not accepted quietly and discovered a month later. You can **raise** an exception yourself."),
           T("raise", "```python\ndef set_units(units):\n    if units < 0:\n        raise ValueError(\"units cannot be negative\")\n    return units\n```\n\nThe message is for the person reading the error. Choose the built-in type that fits: `ValueError` for a bad value, `TypeError` for a wrong type. The caller decides what to do:\n\n```python\ntry:\n    set_units(-3)\nexcept ValueError as e:\n    print(e)       # units cannot be negative\n```"),
           P('def f(n):\n    if n < 0:\n        raise ValueError("negative")\n    return n\ntry:\n    f(-1)\nexcept ValueError as e:\n    print(e)', "negative", ["-1", "!ValueError"], "The function raises, the caller catches, and print shows the message."),
           Q("Why raise an error instead of returning a special value?", ["It cannot be ignored by accident", "It is faster", "Python requires it"], 0, "An unhandled exception stops the program, so a bad value does not slip through.")],
          "Write `check_units(units)` that returns the units, raises `ValueError(\"units cannot be negative\")` for a negative number and raises `TypeError(\"units must be a whole number\")` when it is not an int. Call it for `<<q1>>`, `-3` and `\"<<q1>>\"` inside `try` blocks that print the result or the message. It should print:\n\n<<OUT>>",
          "# def check_units(units): raise ValueError for negative, TypeError for a non-int\n# call it for <<q1>>, -3 and \"<<q1>>\": print the result, or the message of the error\n",
          'def check_units(units):\n    if not isinstance(units, int):\n        raise TypeError("units must be a whole number")\n    if units < 0:\n        raise ValueError("units cannot be negative")\n    return units\n\n\nfor value in (<<q1>>, -3, "<<q1>>"):\n    try:\n        print(check_units(value))\n    except (TypeError, ValueError) as e:\n        print(e)\n',
          checks=[("ftest", "check_units", [[[q1], q1]])], hints=["Check the type first: not isinstance(units, int).", "Catch both types with one except."], emoji="🚨")

    c.add("custom_exceptions", "Creating Custom Exceptions", "Custom errors", "define your own exception type",
          [T("The scenario", "\"Out of stock\" is a normal business situation with its own meaning. A bare `ValueError` hides that meaning. A custom exception type has a **name** the caller can catch precisely."),
           T("A new exception class", "```python\nclass OutOfStockError(Exception):\n    \"\"\"Raised when a request is bigger than the stock.\"\"\"\n\ndef take(units, amount):\n    if amount > units:\n        raise OutOfStockError(f\"only {units} left\")\n    return units - amount\n```\n\nA class that **inherits from `Exception`** is all you need: it is a new kind of error. (Classes get their own treatment soon. For now, copy the shape.) Catch it by name:\n\n```python\ntry:\n    take(5, 9)\nexcept OutOfStockError as e:\n    print(\"Sorry:\", e)\n```"),
           P('class MyError(Exception):\n    pass\ntry:\n    raise MyError("boom")\nexcept MyError as e:\n    print(e)', "boom", ["MyError", "!MyError"], "The exception carries its message, which print shows."),
           Q("What must a custom exception class inherit from?", ["Exception", "print", "int"], 0, "Inheriting from Exception makes it an error type Python can raise and catch.")],
          "Define `OutOfStockError(Exception)` and `take(units, amount)` that returns what is left, or raises the new error with the message `only N left` (N is the units). Try to take 5 and then 99 from `<<q1>>`, printing the result or `Sorry: ` and the message. It should print:\n\n<<OUT>>",
          "# class OutOfStockError(Exception): ...\n# def take(units, amount): raise OutOfStockError(\"only N left\") when amount > units\n# for amount in (5, 99): try take(<<q1>>, amount) and print the result, or Sorry: message\n",
          'class OutOfStockError(Exception):\n    """Raised when a request is bigger than the stock."""\n\n\ndef take(units, amount):\n    if amount > units:\n        raise OutOfStockError(f"only {units} left")\n    return units - amount\n\n\nfor amount in (5, 99):\n    try:\n        print(take(<<q1>>, amount))\n    except OutOfStockError as e:\n        print("Sorry:", e)\n',
          checks=[("ftest", "take", [[[q1, 5], q1 - 5]])], hints=["The class body can be just a docstring or pass.", "Catch it with except OutOfStockError as e."], emoji="🏷️")

    c.add("assert_statement", "Assertions and the assert Statement", "assert", "use assert to check your own assumptions",
          [T("The scenario", "Some conditions should **never** be false if your own code is correct: an average of an empty list, a negative count after a delivery. An `assert` states the assumption, and fails loudly the moment it is wrong, close to the bug."),
           T("assert", "```python\ndef average(values):\n    assert len(values) > 0, \"need at least one value\"\n    return sum(values) / len(values)\n```\n\nIf the condition is False, Python raises **AssertionError** with your message. Use `assert` to catch **your own mistakes** (a function called wrongly). Do **not** use it to check user input or data from files: that should raise a proper `ValueError`, because asserts can be switched off (`python -O`)."),
           P('try:\n    assert 1 + 1 == 3, "maths"\nexcept AssertionError as e:\n    print("caught", e)', "caught maths", ["!AssertionError", "caught"], "The failed assert raises, and the except block prints the message."),
           Q("When is assert the right tool?", ["To check an assumption about your own code", "To validate what a user typed", "To handle missing files"], 0, "Asserts are for developers. User and file errors need real exceptions.")],
          "Write `average(values)` with an `assert` that the list is not empty (message `need at least one value`). Print the average of `<<sreads>>`. Then call it with an empty list inside `try`/`except AssertionError` and print `caught: ` and the message. It should print:\n\n<<OUT>>",
          "# def average(values): assert len(values) > 0, \"need at least one value\"; return the average\n# print the average of <<sreads>>; then try average([]) and print caught: message\n",
          'def average(values):\n    assert len(values) > 0, "need at least one value"\n    return sum(values) / len(values)\n\n\nprint(average(<<sreads>>))\ntry:\n    average([])\nexcept AssertionError as e:\n    print("caught:", e)\n',
          checks=[("ftest", "average", [[[[2, 4, 6]], 4.0]]), ("ast", "Assert", "an assert")], hints=["assert len(values) > 0, \"message\"", "Catch AssertionError as e to read the message."], emoji="✅")

    c.add("debugging_programs", "Debugging Python Programs", "Debugging", "debug a program step by step",
          [T("The scenario", "A function that should total up a delivery gives a wrong answer for some inputs and no error appears. You have the tools, and now you need a **method**."),
           T("A method that works", "1. **Reproduce**: find the smallest input that shows the bug\n2. **Predict**: work out the right answer by hand\n3. **Observe**: `print` the variables inside the function, or use the debugger (`breakpoint()` stops the program and lets you look around)\n4. **Narrow down**: find the first line where reality and prediction disagree\n5. **Fix one thing**, run again, remove the debug prints\n\nThe bug is almost never where you first think. Trust the printed values, not your memory of the code."),
           T("Other helpers", "The `logging` module prints messages with a level (debug, info, warning, error) and can be turned up or down without editing the code. Tests (chapter five) keep a fixed bug fixed. And explaining the code line by line to someone, or to a rubber duck, finds many bugs by itself."),
           Q("What is the best first step when a function gives a wrong answer?", ["Find the smallest input that shows it", "Rewrite the function", "Add random print statements everywhere"], 0, "A small, repeatable case makes everything else easier.")],
          "`running_total` should return the running total of each reading so far, and `average` the mean of the list, but both have bugs. Debug with prints, fix both functions, and make the program print:\n\n<<OUT>>",
          'def running_total(values):\n    result = []\n    total = 0\n    for v in values:\n        total = v\n        result.append(total)\n    return result\n\n\ndef average(values):\n    return sum(values) / (len(values) + 1)\n\n\nprint(running_total([3, 4, 5]))\nprint(average([3, 4, 5]))\n',
          'def running_total(values):\n    result = []\n    total = 0\n    for v in values:\n        total += v\n        result.append(total)\n    return result\n\n\ndef average(values):\n    return sum(values) / len(values)\n\n\nprint(running_total([3, 4, 5]))\nprint(average([3, 4, 5]))\n',
          checks=[("ftest", "running_total", [[[[1, 2, 3]], [1, 3, 6]]]), ("ftest", "average", [[[[2, 4]], 3.0]])], hints=["Print total inside the loop. Does it grow?", "The average divides by the wrong count."], emoji="🐞")

    c.add("error_best_practices", "Error Handling Best Practices", "Chapter 12 project", "handle errors the professional way",
          [T("The scenario", "A helper called `read_count` has a bare `except:` that returns 0 for **anything**. It looked safe. Then somebody passed `None` by mistake, and the program quietly reported zero stock for a month. The most dangerous error handling is the kind that hides the problem."),
           T("The rules", "- **Catch specific exceptions**, never a bare `except:`\n- **Do not swallow errors**: if you cannot do something useful, let it propagate\n- **Fail early** with `raise` when input is wrong\n- Keep the `try` block **small**\n- Give errors **clear messages** with the bad value in them\n- Use `finally` or `with` to clean up\n- **Handle** what you expect (a typo in a form), and let **bugs** (a None where text belongs) crash loudly so they get fixed"),
           T("EAFP", "Python style prefers \"**E**asier to **A**sk **F**orgiveness than **P**ermission\": try the operation and handle the failure, instead of testing every possible problem first. It is shorter and avoids race conditions."),
           P('try:\n    int(None)\nexcept ValueError:\n    print("value")\nexcept TypeError:\n    print("type")', "type", ["value", "!TypeError"], "int(None) raises a TypeError, not a ValueError, so a handler for ValueError alone would not hide it."),
           Q("What is wrong with a bare `except:`?", ["It hides bugs by catching everything", "It is a syntax error", "It is too slow"], 0, "A bare except even swallows mistakes you did not expect.")],
          "Fix `read_count` so that it only handles the **expected** problem (text that is not a number, which gives 0) and lets other errors such as `None` show up. Then call it for `\"<<d>>\"` and `\"n/a\"`, and prove that `None` is **not** hidden: call it inside `try`/`except TypeError` and print `caller saw TypeError`. It should print:\n\n<<OUT>>",
          'def read_count(text):\n    try:\n        return int(text)\n    except:\n        return 0\n\n\nprint(read_count("<<d>>"))\nprint(read_count("n/a"))\ntry:\n    read_count(None)\nexcept TypeError:\n    print("caller saw TypeError")\n',
          'def read_count(text):\n    try:\n        return int(text)\n    except ValueError:\n        return 0\n\n\nprint(read_count("<<d>>"))\nprint(read_count("n/a"))\ntry:\n    read_count(None)\nexcept TypeError:\n    print("caller saw TypeError")\n',
          hints=["Replace the bare except with the specific exception for text that is not a number.", "A TypeError for None should reach the caller."], emoji="🏁")
