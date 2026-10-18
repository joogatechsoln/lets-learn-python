"""Chapter 6: Computing (10 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Computing")
    X = c.ctx
    q1, q2, d, bsz = X["q1"], X["q2"], X["d"], X["bsz"]

    c.add("computational_thinking", "Introduction to Computational Thinking", "Thinking", "break a problem into steps",
          [T("The scenario", "The owner of <<biz>> asks: \"After today's delivery and the daily losses, how many <<things>> will we have?\" Before writing a line of code, a programmer *thinks* about the problem. That habit has a name: **computational thinking**."),
           T("Four moves", "- **Decomposition**: break the problem into small steps\n- **Pattern recognition**: spot what repeats or looks like a problem you solved before\n- **Abstraction**: ignore details that do not matter\n- **Algorithm**: write the steps in an exact order\n\nAn **algorithm** is a precise recipe. A program is an algorithm written in a language a computer can follow."),
           T("From steps to code", "Each step usually becomes a line or two of code, with a **name** for every value. If you can list the steps in plain words, writing the code is the easy part. If you cannot, no amount of typing will help."),
           Q("What is an algorithm?", ["An exact, ordered list of steps that solves a problem", "A kind of variable", "A Python library"], 0, "Algorithms are the recipe. Code is how you write the recipe down for a computer."),
           P("opening = 10\nopening += 5\nopening -= 3\nprint(opening)", "12", ["15", "13"], "Follow the steps in order: 10, then 15, then 12.")],
          "Turn this plain-English algorithm into code, with a named value for each step, and print each step. It should print:\n\n<<OUT>>\n\nThe losses today were 7 sold and 2 spoiled.",
          "# Algorithm:\n# 1. Start with the opening count <<q1>>\n# 2. Add the delivery <<d>>\n# 3. Subtract the 7 sold\n# 4. Subtract the 2 spoiled\n# 5. The result is the closing count\n",
          'opening = <<q1>>\ndelivered = <<d>>\nsold = 7\nspoiled = 2\nclosing = opening + delivered - sold - spoiled\nprint("Opening:", opening)\nprint("Delivered:", delivered)\nprint("Sold:", sold)\nprint("Spoiled:", spoiled)\nprint("Closing:", closing)\n',
          checks=[("var", "closing")], hints=["Give every step its own variable name.", "closing is opening plus delivered, minus sold and spoiled."], emoji="🧠")

    c.add("variables_expressions", "Variables and Expressions", "Expressions", "build expressions step by step",
          [T("The scenario", "A long formula in one line is hard to check. The same formula split into named steps is easy to read, test and fix. Today you write both and prove they agree."),
           T("Expressions and statements", "An **expression** produces a value: `<<q1>> + <<d>>`. A **statement** does something: `total = <<q1>> + <<d>>`. Expressions can be nested and combined as far as you like. Python works out the inside first.\n\n```python\nnet = (10 + 5 - 7) * 2.5      # one expression\nstep1 = 10 + 5                # the same, in steps\nstep2 = step1 - 7\nnet2 = step2 * 2.5\n```"),
           T("Which style?", "Short formulas read fine on one line. When a formula has more than three parts, **name the pieces**. A named step is a tiny piece of documentation, and you can `print` it when something looks wrong."),
           P("a = 10 + 5\nb = a - 7\nprint(b * 2)", "16", ["8", "30"], "a is 15, b is 8, and b * 2 is 16."),
           Q("When is it better to split a formula into named steps?", ["When it has several parts and needs to be understood or checked", "Never, one line is always best", "Only for strings"], 0, "Named steps are easier to read and to debug.")],
          "Work out the net value of the stock after the delivery and 7 going out, valued at <<p1>> each. Do it **twice**: as one expression (`net_one`) and in three named steps (`net_steps`). Then print both and whether they are equal. It should print:\n\n<<OUT>>",
          "# net_one: one expression: (<<q1>> + <<d>> - 7) * <<p1>>\n# net_steps: in three named steps\n# print both, then print whether net_one == net_steps\n",
          'net_one = (<<q1>> + <<d>> - 7) * <<p1>>\nafter_delivery = <<q1>> + <<d>>\nafter_losses = after_delivery - 7\nnet_steps = after_losses * <<p1>>\nprint(net_one)\nprint(net_steps)\nprint(net_one == net_steps)\n',
          checks=[("var", "net_one"), ("var", "net_steps")], hints=["Brackets make the addition and subtraction happen before the multiplication.", "== compares two values and gives True or False."], emoji="🧮")

    c.add("arithmetic_operators", "Arithmetic Operators", "Operators", "use all seven arithmetic operators",
          [T("The scenario", "<<q1>> <<qty_unit>> have to be shared out in groups of <<bsz>>. How many per group, how many left, what is the square? Python has an operator for each question."),
           T("The seven", "- `+` `-` `*` ordinary add, subtract, multiply\n- `/` true division, always a **float**\n- `//` floor division, rounds **down**\n- `%` remainder (modulo)\n- `**` power\n\n```python\nprint(7 / 2)     # 3.5\nprint(7 // 2)    # 3\nprint(7 % 2)     # 1\nprint(2 ** 3)    # 8\n```"),
           T("A negative surprise", "Floor division rounds **down**, which for negative numbers means *away from zero*:\n\n```python\nprint(-7 // 2)    # -4, not -3\nprint(-7 % 2)     # 1\n```\n\nThe pair always satisfies `a == (a // b) * b + a % b`. That identity is a handy self-check."),
           P("print(-7 // 2, -7 % 2)", "-4 1", ["-3 -1", "-3 1"], "Floor division rounds down to -4, and the remainder that makes the identity work is 1."),
           Q("What is 2 ** 3?", ["8", "6", "9"], 0, "** is the power operator: 2 * 2 * 2.")],
          "With `a = <<q1>>` and `b = <<bsz>>`, print the result of **all seven** operators, each on its own line like `a // b = ...`. It should print:\n\n<<OUT>>",
          "a = <<q1>>\nb = <<bsz>>\n# one print line per operator: + - * / // % **\n",
          'a = <<q1>>\nb = <<bsz>>\nprint("a + b =", a + b)\nprint("a - b =", a - b)\nprint("a * b =", a * b)\nprint("a / b =", a / b)\nprint("a // b =", a // b)\nprint("a % b =", a % b)\nprint("a ** 2 =", a ** 2)\n',
          checks=[("prints", 7)], hints=["print(\"a + b =\", a + b) is the pattern.", "The last one uses a ** 2, a squared."], emoji="➗")

    c.add("operator_precedence", "Operator Precedence", "Precedence", "predict and control evaluation order",
          [T("The scenario", "Four lines in the <<system>> print numbers nobody expected. Each is correct maths in the wrong order. You will diagnose each and use brackets to say what was meant."),
           T("The ladder", "From strongest to weakest:\n\n1. `( )` brackets\n2. `**` power (right to left)\n3. `-x` unary minus\n4. `*  /  //  %`\n5. `+  -`\n6. comparisons, then `not`, `and`, `or` (later chapter)\n\nSame level runs **left to right**, except `**`."),
           T("The famous trap", "`-3 ** 2` is `-(3 ** 2)`, which is `-9`, because `**` binds tighter than the minus sign. To square negative three you must write `(-3) ** 2`. When in doubt, add brackets."),
           P("print(-3 ** 2, (-3) ** 2)", "-9 9", ["9 9", "-9 -9"], "Power goes before the unary minus, so -3 ** 2 is -(3 ** 2) = -9."),
           Q("What is 100 - 20 / 4 + 1?", ["96.0", "21.0", "81.0"], 0, "Division first: 20 / 4 is 5.0. Then 100 - 5.0 + 1 is 96.0.")],
          "Each line prints something unintended. Add brackets so the four lines print the values the comments describe. It should print:\n\n<<OUT>>",
          "print(<<q1>> + <<d>> * 2)        # want: (<<q1>> + <<d>>) doubled\nprint(-3 ** 2)                   # want: 3 squared with the sign flipped first, i.e. 9\nprint(100 - 20 / 4 + 1)          # want: (100 - 20) divided by 4, plus 1\nprint(<<q2>> * 2 ** 3)           # want: (<<q2>> * 2) to the power 3\n",
          "print((<<q1>> + <<d>>) * 2)\nprint((-3) ** 2)\nprint((100 - 20) / 4 + 1)\nprint((<<q2>> * 2) ** 3)\n",
          hints=["Brackets go around the part that must happen first.", "(-3) ** 2 squares the negative number."], emoji="🪜")

    c.add("int_float_arithmetic", "Integer and Floating-Point Arithmetic", "int and float", "understand int and float behaviour",
          [T("The scenario", "A till total of 0.30 shows as 0.30000000000000004 on a report. Nobody typed that number. It is the way computers store decimals, and every programmer has to know about it."),
           T("Ints are exact, floats are close", "- `int`: whole numbers of **any size**, always exact: `2 ** 100` works fine\n- `float`: decimals stored in binary with about 15 to 16 digits of accuracy. Most decimals like 0.1 cannot be stored exactly\n\n```python\nprint(0.1 + 0.2)      # 0.30000000000000004\nprint(round(0.1 + 0.2, 2))   # 0.3\n```"),
           T("What to do about it", "- **Round for display**: `round(x, 2)` or `f\"{x:.2f}\"`\n- **Never compare computed floats with `==`**: use `round` or `math.isclose` (coming up)\n- For money, many programs keep whole **cents** as ints, or use Python's `decimal` module"),
           P("print(0.1 + 0.2 == 0.3)", "False", ["True", "0.3"], "The sum is 0.30000000000000004, which is not equal to 0.3."),
           Q("Which comparison is safest for computed floats?", ["Round both first, or use a tolerance", "Use == directly", "Convert them to text"], 0, "Floats are approximations, so compare with a small tolerance.")],
          "Print six lines that show how ints and floats behave. It should print:\n\n<<OUT>>\n\nThe lines are, in order: `0.1 + 0.2`, the same rounded to 2 places, `7 / 2`, `7 // 2`, `2 ** 100`, and the type name of `10 / 5`.",
          "# six print lines, as listed in the task\n",
          'print(0.1 + 0.2)\nprint(round(0.1 + 0.2, 2))\nprint(7 / 2)\nprint(7 // 2)\nprint(2 ** 100)\nprint(type(10 / 5).__name__)\n',
          checks=[("prints", 6)], hints=["type(10 / 5).__name__ gives the name of the type.", "Python prints huge ints in full."], emoji="🔢")

    c.add("type_conversion_numbers", "Type Conversion", "Converting", "convert values between numeric types",
          [T("The scenario", "A supplier's feed gives every number as **text**, even the count and the rate. Before the <<system>> can do maths, each value must be converted, and Python must be told which kind of number it is."),
           T("Explicit conversion", "```python\nint(\"42\")        # 42\nfloat(\"4.5\")      # 4.5\nint(3.9)          # 3, drops the decimals\nround(3.9)        # 4, rounds\nstr(42)           # \"42\"\nbool(0)           # False\n```\n\n`int(\"4.5\")` is a `ValueError`: go through `float` first."),
           T("Implicit conversion", "Python converts for you in mixed arithmetic: `int + float` gives a **float**. And `bool` counts as a number: `True + True` is `2`.\n\n```python\nprint(2 + 0.5)        # 2.5\nprint(True + True)    # 2\n```"),
           P("print(int(3.9), round(3.9), float(\"2\"))", "3 4 2.0", ["4 4 2", "3 3 2.0"], "int cuts off, round rounds up here, and float(\"2\") is 2.0."),
           Q("What does int(\"4.5\") do?", ["Raises a ValueError", "Gives 4", "Gives 4.5"], 0, "int() only accepts whole-number text. Use float() first.")],
          "The feed gives `feed_units = \"<<q1>>\"` and `feed_rate = \"<<p1>>\"` as text. Convert them, work out `feed_value`, and print the value, the type of each converted number, and `True + True`. It should print:\n\n<<OUT>>",
          'feed_units = "<<q1>>"\nfeed_rate = "<<p1>>"\n# units: an int, rate: a float, feed_value: their product\n# print feed_value, the type name of units, the type name of rate, and True + True\n',
          'feed_units = "<<q1>>"\nfeed_rate = "<<p1>>"\nunits = int(feed_units)\nrate = float(feed_rate)\nfeed_value = units * rate\nprint(feed_value)\nprint(type(units).__name__)\nprint(type(rate).__name__)\nprint(True + True)\n',
          checks=[("var", "feed_value")], hints=["int(feed_units) and float(feed_rate) do the conversions.", "type(x).__name__ gives the type name."], emoji="🔁")

    c.add("assignment_operators", "Assignment Operators", "Shortcuts", "use augmented assignment",
          [T("The scenario", "A till keeps a running total through the day: add a sale, take off a refund, double-check, share out. Writing `total = total + x` forty times is tiring. Assignment operators are shortcuts."),
           T("Augmented assignment", "```python\nx += 5     # x = x + 5\nx -= 2     # x = x - 2\nx *= 3     # x = x * 3\nx /= 2     # x = x / 2 (now a float)\nx //= 2    # floor divide\nx %= 4     # remainder\nx **= 2    # power\n```\n\nThere is one for each arithmetic operator."),
           T("Multiple assignment", "```python\nlow = high = 0        # same value to two names\na, b = 1, 2           # two values at once\na, b = b, a           # swap\n```\n\nAll of these are just convenient ways to write ordinary assignments."),
           P("x = 10\nx += 5\nx *= 2\nx -= 4\nprint(x)", "26", ["21", "30"], "10 becomes 15, then 30, then 26."),
           Q("What is `x //= 2` the same as?", ["x = x // 2", "x = x / 2", "x = 2 // x"], 0, "Every augmented operator is a shorthand for x = x op value.")],
          "Start with `x = <<q1>>` and apply these updates, printing `x` after each: `+= <<d>>`, `-= 5`, `*= 2`, `//= 3`, `%= 7`, `**= 2`. It should print:\n\n<<OUT>>",
          "x = <<q1>>\n# apply the six updates from the task, printing x after each\n",
          'x = <<q1>>\nx += <<d>>\nprint(x)\nx -= 5\nprint(x)\nx *= 2\nprint(x)\nx //= 3\nprint(x)\nx %= 7\nprint(x)\nx **= 2\nprint(x)\n',
          checks=[("var", "x"), ("prints", 6)], hints=["One update then one print, six times.", "Each operator is the one from the task, followed by ="], emoji="➕")

    c.add("numeric_data", "Working with Numeric Data", "Numbers in reports", "summarise and format numbers",
          [T("The scenario", "The owner wants the four <<things>>' values, their total, and what share of the total each one is, formatted so a person can read it without a calculator."),
           T("Summarising", "`sum`, `min`, `max`, `len` and a division give you the total, extremes and average. A **share** is a part divided by the whole:\n\n```python\nshare = part / total        # 0.25\nprint(f\"{share:.1%}\")       # 25.0%\n```"),
           T("Formatting numbers", "Inside an f-string, after the colon:\n\n- `:,` adds thousands separators: `f\"{1234567:,}\"` is `1,234,567`\n- `:.2f` fixes 2 decimals\n- `:,.2f` does both\n- `:.1%` turns 0.256 into `25.6%`\n- `:>10` right-aligns in a 10-character field"),
           P('print(f"{1234567.891:,.2f}")', "1,234,567.89", ["1234567.89", "1,234,567.891"], ":,.2f adds thousands separators and rounds to 2 decimals."),
           Q("Which format gives 25.0% from 0.25?", [":.1%", ":.1f", ":,"], 0, "The % format multiplies by 100 and adds the sign.")],
          "Work out the value of each of the four <<things>> (units times rate), the total, and each one's share of the total. Print each line like `<<n1>>: <value> (<share>)` with the value to 2 decimals with commas and the share to 1 decimal percent, then the total line. It should print:\n\n<<OUT>>",
          "v1 = <<q1>> * <<p1>>\nv2 = <<q2>> * <<p2>>\nv3 = <<q3>> * <<p3>>\nv4 = <<q4>> * <<p4>>\n# total, then print the four lines with value and share, then the total\n",
          'v1 = <<q1>> * <<p1>>\nv2 = <<q2>> * <<p2>>\nv3 = <<q3>> * <<p3>>\nv4 = <<q4>> * <<p4>>\ntotal = v1 + v2 + v3 + v4\nprint(f"<<n1>>: {v1:,.2f} ({v1 / total:.1%})")\nprint(f"<<n2>>: {v2:,.2f} ({v2 / total:.1%})")\nprint(f"<<n3>>: {v3:,.2f} ({v3 / total:.1%})")\nprint(f"<<n4>>: {v4:,.2f} ({v4 / total:.1%})")\nprint(f"Total: {total:,.2f}")\n',
          checks=[("var", "total")], hints=["total = v1 + v2 + v3 + v4", "f\"{v1 / total:.1%}\" gives the share."], emoji="📊")

    c.add("math_functions", "Mathematical Functions", "The math module", "use the math module",
          [T("The scenario", "Packing needs rounding **up** (a part-full crate still needs a crate). Distances need square roots. The built-in operators are not enough, but Python's **math** module has what you need."),
           T("Importing", "A **module** is a toolbox of ready-made code. Bring it in with `import`:\n\n```python\nimport math\n\nprint(math.sqrt(16))        # 4.0\nprint(math.ceil(4.1))       # 5, rounds up\nprint(math.floor(4.9))      # 4, rounds down\nprint(math.pi)              # 3.141592653589793\nprint(math.hypot(3, 4))     # 5.0, the straight-line distance\nprint(math.isclose(0.1 + 0.2, 0.3))   # True\n```"),
           T("Handy ones", "- `math.ceil` and `math.floor`: round up and down\n- `math.sqrt`, `math.pow`, `math.hypot`\n- `math.log`, `math.log10`, `math.exp`\n- `math.factorial(5)` is 120\n- `math.isclose(a, b)`: the right way to compare floats\n\nCall them with the module name and a dot."),
           P("import math\nprint(math.ceil(2.1), math.floor(2.9))", "3 2", ["2 2", "3 3"], "ceil goes up to 3, floor goes down to 2."),
           Q("Why use math.ceil to count crates?", ["A part-full crate still needs a whole crate", "It makes numbers smaller", "It converts to text"], 0, "Rounding up gives the number of containers needed.")],
          "Use the math module for four jobs and print each: the number of <<bw>> needed for <<q1>> if each holds <<bsz>> (rounded **up**), the area of a circle of radius 3 (rounded to 2 places), the straight-line distance from the origin to the point (<<sx>>, <<sy>>) rounded to 2 places, and whether `0.1 + 0.2` is close to `0.3`. It should print:\n\n<<OUT>>",
          "import math\n# four print lines, as in the task\n",
          'import math\n\nprint(math.ceil(<<q1>> / <<bsz>>))\nprint(round(math.pi * 3 ** 2, 2))\nprint(round(math.hypot(<<sx>>, <<sy>>), 2))\nprint(math.isclose(0.1 + 0.2, 0.3))\n',
          checks=[{"type": "source_count", "pattern": r"^import math", "min": 1, "label": "Imports math"}], hints=["math.ceil(a / b) rounds a division up.", "math.hypot(x, y) is the distance from the origin."], emoji="📐")

    c.add("computational_programs", "Writing Computational Programs", "Chapter 6 project", "combine functions and maths into a program",
          [T("The scenario", "Chapter six ends with a small computing program for the <<system>>: how many <<bw>> are needed, how much did the count change, and a one-line summary a manager can read at a glance."),
           T("Plan, then code", "1. **Decompose**: which numbers does the manager want?\n2. **Name** each calculation as a small function\n3. **Test** each function by hand on easy numbers\n4. **Combine** them in a short script that prints the answers\n\nSmall functions that return values are the building blocks of every computing program."),
           T("Checklist", "- Functions **return**, scripts **print**\n- Rounding happens at the **end**, for display\n- `math.ceil` for counts of containers\n- Percent change is `(new - old) / old * 100`")],
          "Write three functions and use them:\n\n- `batches_needed(units, size)` returns how many batches are needed, rounded **up**\n- `percent_change(old, new)` returns the change as a percentage\n- `describe_change(old, new)` returns text like `+8.3%`, one decimal place with a sign\n\nThen print the batches needed for <<q1>> in groups of <<bsz>>, and the change from <<q1>> to <<q1>> + <<d>>. It should print:\n\n<<OUT>>",
          "import math\n\n# batches_needed(units, size), percent_change(old, new), describe_change(old, new)\n# print batches_needed(<<q1>>, <<bsz>>) and describe_change(<<q1>>, <<q1>> + <<d>>)\n",
          'import math\n\n\ndef batches_needed(units, size):\n    """Return how many batches are needed, counting a part batch as a whole one."""\n    return math.ceil(units / size)\n\n\ndef percent_change(old, new):\n    """Return the change from old to new as a percentage of old."""\n    return (new - old) / old * 100\n\n\ndef describe_change(old, new):\n    """Return the change as signed text with one decimal place."""\n    return f"{percent_change(old, new):+.1f}%"\n\n\nprint(batches_needed(<<q1>>, <<bsz>>))\nprint(describe_change(<<q1>>, <<q1>> + <<d>>))\n',
          checks=[("ftest", "batches_needed", [[[q1, bsz], -(-q1 // bsz)], [[10, 5], 2], [[11, 5], 3]]), ("ftest", "percent_change", [[[100, 150], 50.0], [[200, 100], -50.0]]), ("ftest", "describe_change", [[[100, 150], "+50.0%"]])],
          hints=["math.ceil(units / size) rounds the division up.", "f\"{value:+.1f}%\" gives the sign and one decimal."], emoji="🖥️")
