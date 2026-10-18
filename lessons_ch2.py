"""Chapter 2: Variables and data types (21 lessons)."""
from curriculum import P, Q, T


def build(c):
    c.set_chapter("Variables and data types")
    VL = c.ctx["VL"]

    c.add("memory_problem", "The Memory Problem", "Memory", "store values in variables",
          [T("The scenario", "In chapter one every number was typed again and again, and the program forgot it the moment a line ended. <<biz>> needs the <<system>> to **remember** the first <<thing>>: its name, how many there are, and the rate."),
           T("What is a variable?", "A **variable** is a name attached to a value, like a label on a box. The `=` sign puts a value in the box.\n\n```python\ncity = \"Lima\"\nvisitors = 120\nticket = 8.5\nprint(city, visitors, ticket)\n```\n\nNow `visitors` stands for `120` anywhere below. Use the name instead of typing the number again. Read `=` as **\"gets the value\"**, not as \"equals\"."),
           T("Why it matters", "Imagine the price of an item changes. With a variable you change **one line**. Without it you hunt through the whole program. Variables are what turn a pile of prints into a real program."),
           P("price = 4.5\nprint(price * 2)", "9.0", ["4.52", "price * 2"], "`price` is replaced by 4.5 wherever it appears, so the maths is 4.5 * 2 = 9.0."),
           Q("What does `price = 4.5` do?", ["Stores 4.5 under the name price", "Prints 4.5", "Checks whether price is 4.5"], 0, "A single `=` stores a value under a name. It does not print and it does not compare.")],
          "Store the first <<thing>> in three variables, using exactly these names, then print them on one line:\n\n- `<<vn>>` is the text `\"<<n1>>\"`\n- `<<vq>>` is <<q1>>\n- `<<vr>>` is <<p1>>\n\nYou should see:\n\n<<OUT>>",
          "# Store the first <<thing>> in three variables\n# Then print them on one line\n",
          '<<vn>> = "<<n1>>"\n<<vq>> = <<q1>>\n<<vr>> = <<p1>>\nprint(<<vn>>, <<vq>>, <<vr>>)\n',
          checks=[("var", c.ctx["vn"], True), ("var", c.ctx["vq"], True), ("var", c.ctx["vr"], True)],
          hints=["A text value needs quotes. A number does not.", "Write the name, then =, then the value. For example: <<vq>> = <<q1>>"], emoji="🧠")

    c.add("changing_states", "Changing States", "State", "update a variable over time",
          [T("The scenario", "Stock is never still. A delivery arrives, customers take things, and the count changes all day. The <<system>> has to track a number **as it changes**, and a variable is exactly the place to do it."),
           T("Variables can change", "You can give a variable a new value whenever you like. The old value is replaced.\n\n```python\ncount = 10\ncount = count + 5     # now 15\nprint(count)\n```\n\nPython works out the right side first (10 + 5), then stores the result back under the name."),
           T("Shortcuts", "Updating a variable is so common that it has shortcuts:\n\n```python\ncount += 5    # same as count = count + 5\ncount -= 2    # same as count = count - 2\ncount *= 2    # same as count = count * 2\n```\n\nThe value a variable holds at a given moment is its **state**. A program is mostly a story about how state changes."),
           P("count = 5\ncount += 2\ncount -= 1\nprint(count)", "6", ["7", "5"], "Start at 5, add 2 to get 7, subtract 1 to get 6."),
           Q("After `x = 3` then `x = x * 2`, what is x?", ["6", "3", "32"], 0, "Python calculates `x * 2` using the current value (3), then stores 6 back in `x`.")],
          "Track the count of <<n1>> through the day. Follow the comments in the starter and print the count after each step. It should print:\n\n<<OUT>>",
          'on_hand = <<q1>>\nprint("Start:", on_hand)\n# Add the delivery of <<d>>, then print "After <<delivery_note>>:" and the new count\n# Then 5 go out: subtract 5 and print "After 5 go out:" and the new count\n',
          'on_hand = <<q1>>\nprint("Start:", on_hand)\non_hand += <<d>>\nprint("After <<delivery_note>>:", on_hand)\non_hand -= 5\nprint("After 5 go out:", on_hand)\n',
          checks=[("var", "on_hand")], hints=["Use on_hand += <<d>> to add the delivery.", "Print after each change, so the output shows every step."], emoji="🔄")

    c.add("memory_wipe", "Memory Wipe", "Reset", "reset values and delete variables",
          [T("The scenario", "At the end of every shift the tally is cleared, and the notes you used along the way are thrown out. If a program never clears its old state, tomorrow's report starts with today's numbers. That is a bug waiting to happen."),
           T("Resetting", "To reset a variable, give it its starting value again:\n\n```python\nshift_total = 0\n```\n\nThe old value is gone. This is the everyday way to \"wipe\" a counter."),
           T("Deleting", "`del` removes a variable completely, so the name no longer exists.\n\n```python\nnote = \"temporary\"\ndel note\nprint(note)     # NameError: name 'note' is not defined\n```\n\nBe careful: using a name after `del` is a **NameError**. Use it for temporary values you really are finished with."),
           P("x = 5\ndel x\nprint(x)", "!NameError", ["5", "None"], "After `del x` the name `x` is gone, so using it is a NameError."),
           Q("What is the difference between `x = 0` and `del x`?", ["x = 0 resets the value, del x removes the name", "They are the same", "del x sets x to 0"], 0, "A reset keeps the name and changes the value. `del` removes the name itself.")],
          "It is the end of the shift. Add the end-of-shift steps from the comments, and print the total after the reset. It should print:\n\n<<OUT>>",
          'shift_total = <<q1>> * <<p1>>\nscratch_note = "temporary figures"\nprint("Shift total:", shift_total)\n# End of the shift:\n# 1) reset shift_total to zero\n# 2) delete scratch_note with del\n# 3) print "Total after reset:" and shift_total\n',
          'shift_total = <<q1>> * <<p1>>\nscratch_note = "temporary figures"\nprint("Shift total:", shift_total)\nshift_total = 0\ndel scratch_note\nprint("Total after reset:", shift_total)\n',
          checks=[("var", "shift_total"), ("absent", "scratch_note")], hints=["Reset a variable by giving it its starting value: shift_total = 0", "The syntax is del name, with no brackets and no quotes."], emoji="🧹")

    c.add("payload_math", "Payload Math", "Payload", "use // and % to split a quantity",
          [T("The scenario", "The <<system>> has <<q1>> <<qty_unit>> to handle, and they are handled in groups called <<bw>>, **<<bsz>> at a time**. How many full <<bw>> is that, and how many are left over? Two special operators answer both questions instantly."),
           T("Whole parts and remainders", "- `//` is **floor division**: how many whole times one number fits into another\n- `%` is the **remainder**: what is left over\n\n```python\nprint(17 // 5)    # 3 whole groups of 5\nprint(17 % 5)     # 2 left over\n```\n\nTogether they split any quantity into **full groups plus leftovers**."),
           T("Worked example", "17 items packed in boxes of 5:\n\n```python\nitems = 17\nbox_size = 5\nfull_boxes = items // box_size     # 3\nleft_over = items % box_size       # 2\n```\n\nCheck: 3 * 5 + 2 = 17. This check always works, so use it to test your own answers."),
           P("print(17 // 5, 17 % 5)", "3 2", ["3.4 2", "2 3"], "5 fits into 17 three whole times (15), leaving 2."),
           Q("<<q1>> // <<bsz>> and <<q1>> % <<bsz>> together tell you...", ["How many full <<bw>> and how many are left", "The average and the total", "The biggest and smallest"], 0, "Floor division gives the full groups and the remainder gives what does not fit.")],
          "The <<vq>> and <<vr>> variables are still set from the last lessons. Work out the payload:\n\n- `full_batches` is how many full <<bw>> of <<bsz>> fit in <<vq>>\n- `left_over` is what remains\n- `<<vt>>` is <<vq>> times <<vr>> (the value)\n\nPrint all three as shown:\n\n<<OUT>>",
          "# Groups called <<bw>> hold <<bsz>> each\n# Work out full_batches, left_over and <<vt>>, then print them\n",
          'full_batches = <<vq>> // <<bsz>>\nleft_over = <<vq>> % <<bsz>>\n<<vt>> = <<vq>> * <<vr>>\nprint("Full <<bw>>:", full_batches)\nprint("Left over:", left_over)\nprint("<<total_label>>:", <<vt>>)\n',
          checks=[("var", "full_batches"), ("var", "left_over"), ("var", c.ctx["vt"])],
          hints=["full_batches = <<vq>> // <<bsz>>", "Use % for what is left over."], emoji="🚚")

    c.add("negative_numbers", "Negative Numbers", "Below zero", "work with negative numbers",
          [T("The scenario", "The <<sn>> reports **<<sread>> <<sunit>>**. Below zero is perfectly normal for some readings, and the maths has to cope. The question for the <<system>> is how far the reading is from its target of <<starget>> <<sunit>>."),
           T("Negative numbers", "Put a minus sign in front of a number to make it negative. All the normal operators work.\n\n```python\ntemp = -4\nprint(temp + 10)      # 6\nprint(-4 - 3)         # -7\nprint(-4 - -3)        # -1\n```\n\nSubtracting a negative is the same as adding."),
           T("The gap and abs()", "The **gap** between two values is `a - b`. It is negative when `a` is the smaller one. `abs()` removes the sign, giving the plain **distance**:\n\n```python\ngap = -18.5 - -18.0    # -0.5\nprint(abs(gap))        # 0.5\n```"),
           P("print(abs(-7) + (-3))", "4", ["10", "-10"], "abs(-7) is 7, and 7 + (-3) is 4."),
           Q("What is -4 - -2 ?", ["-2", "-6", "2"], 0, "Subtracting -2 is the same as adding 2, so -4 + 2 = -2.")],
          "Store the probe's reading and its target, then work out the gap and the distance. It should print:\n\n<<OUT>>\n\nThe reading is <<sread>> and the target is <<starget>>.",
          "# Store reading and target_reading, then work out the gap\n",
          'reading = <<sread>>\ntarget_reading = <<starget>>\ngap = reading - target_reading\nprint("Gap:", gap)\nprint("Distance from target:", abs(gap))\n',
          checks=[("var", "reading", True), ("var", "target_reading", True), ("var", "gap")],
          hints=["The gap is reading minus target_reading. It can come out negative.", "abs(gap) gives the distance with the sign removed."], emoji="➖")

    c.add("strings_snake_case", "Strings & Snake Case", "Names", "write text values and snake_case names",
          [T("The scenario", "A colleague's code works but is hard to read: every variable name is written differently. Teams agree on **one style** so that anyone can read anyone's code. For Python variables that style is called snake_case."),
           T("Strings", "Text values are called **strings**. Use single or double quotes, but close with the same kind.\n\n```python\nname = \"Ada\"\nplace = 'Lima'\nprint(name + \" in \" + place)\nprint(len(name))     # 3 characters\n```\n\nJoin strings with `+`. Repeat them with `*`."),
           T("snake_case", "Variable names in Python are written in lowercase, with words joined by underscores:\n\n- `units_in_stock` is snake_case: good\n- `unitsInStock` is camelCase: not the Python way\n- `UnitsInStock` is PascalCase: kept for classes\n\nA name should say what the value **is**, so that no comment is needed."),
           P('name = "Ada"\nprint(name * 2)', "AdaAda", ["Ada 2", "Ada Ada"], "Multiplying a string repeats it. There is no space added."),
           Q("Which name follows the Python style?", ["reading_unit", "ReadingUnit", "readingUnit"], 0, "Python variables use lowercase words joined with underscores.")],
          "The three variable names below are in the wrong style. Rename each one to snake_case everywhere it appears: `sensor_name`, `sensor_id` and `reading_unit`. The output must not change:\n\n<<OUT>>",
          'SensorName = "<<sn>>"\nsensorID = <<sid>>\nreadingUnit = "<<sunit>>"\nprint(SensorName, sensorID, readingUnit)\n',
          'sensor_name = "<<sn>>"\nsensor_id = <<sid>>\nreading_unit = "<<sunit>>"\nprint(sensor_name, sensor_id, reading_unit)\n',
          checks=[("var", "sensor_name"), ("var", "sensor_id"), ("var", "reading_unit"), ("absent", "SensorName"), ("absent", "sensorID"), ("absent", "readingUnit")],
          hints=["Rename the name in the assignment **and** in the print line.", "Lowercase letters, with an underscore between words."], emoji="🐍")

    c.add("naming_standard", "The Naming Standard", "Naming rules", "follow Python's naming rules",
          [T("The scenario", "Python is strict about names. Some names are not allowed at all, and some are allowed but cause trouble later. The <<system>> team keeps a short naming standard so that nobody has to guess."),
           T("The rules (Python enforces these)", "- Letters, digits and underscores only\n- Cannot **start** with a digit\n- No spaces\n- Cannot be a **keyword** like `class`, `if`, `for`, `print` is fine but `class` is not\n- Upper and lower case are **different**: `Total` and `total` are two names"),
           T("The conventions (your team enforces these)", "- Use **snake_case** for variables\n- Make names meaningful: `price_per_pack`, not `p`\n- Write **constants**, values that never change, in `UPPER_CASE`:\n\n```python\nMAX_PORTS = 24\n```\n\nPython will not stop you changing a constant, but the capitals tell every reader: leave this alone."),
           Q("Which is a valid variable name?", ["site_2", "2nd_site", "site name"], 0, "Names cannot start with a digit or contain spaces. `site_2` is fine."),
           P("max_ports = 24\nMAX_PORTS = 48\nprint(max_ports)", "24", ["48", "!NameError"], "Names are case sensitive, so `max_ports` and `MAX_PORTS` are two separate variables.")],
          "Three names break Python's rules. Python reports one at a time, so fix, run, repeat. Rename them to `second_site`, `site_name` and `business_name`, then add the constant described in the last comment.\n\nIt should print:\n\n<<OUT>>",
          '2nd_site = "<<n2>>"\nsite name = "<<n1>>"\nclass = "<<biz>>"\n# The rule number never changes: store <<level>> in a constant called <<VL>>\nprint(site_name, second_site, business_name, <<VL>>)\n',
          'second_site = "<<n2>>"\nsite_name = "<<n1>>"\nbusiness_name = "<<biz>>"\n# The rule number never changes: store <<level>> in a constant called <<VL>>\n<<VL>> = <<level>>\nprint(site_name, second_site, business_name, <<VL>>)\n',
          checks=[("var", "second_site"), ("var", "site_name"), ("var", "business_name"), ("var", VL)],
          hints=["2nd_site starts with a digit. site name has a space. class is a keyword.", "Add the line <<VL>> = <<level>> before the print."], emoji="📛")

    c.add("firmware_formatting", "Firmware Formatting", "Label formatting", "clean and format text with string methods",
          [T("The scenario", "Labels arrive from the field in all shapes: extra spaces, no capitals, no padding. The <<system>> must turn the raw label of the <<sn>> into something clean that every report can use."),
           T("Methods", "A **method** is a function that belongs to a value. You call it with a dot.\n\n```python\nlabel = \"  freezer a \"\nprint(label.strip())    # removes outer spaces\nprint(label.title())    # Capitalises Each Word\nprint(label.upper())    # ALL CAPITALS\nprint(len(label))       # number of characters\n```\n\nMethods can be **chained**: `label.strip().title()` strips first, then titles."),
           T("Padding numbers", "IDs often need a fixed width. `zfill` pads a text with leading zeros:\n\n```python\nprint(str(101).zfill(5))    # 00101\n```\n\nNote `str()` first: `zfill` works on text, not numbers."),
           P('print("  hello world ".strip().title())', "Hello World", ["  Hello World ", "hello world"], "strip() removes the outer spaces, then title() capitalises each word."),
           Q("What does \" hi \".strip() return?", ["\"hi\" without the outer spaces", "\"HI\"", "3"], 0, "strip() removes spaces from both ends and leaves the middle alone.")],
          "Clean up the raw label and build the tag. It should print:\n\n<<OUT>>\n\nThe tag is <<stag>>, a dash, then the id padded with zeros to 5 digits.",
          'raw_label = "<<sraw>>"\nsensor_id = <<sid>>\n# clean_label: remove the outer spaces and capitalise every word\n# tag: "<<stag>>-" followed by the id padded to 5 digits\n# print "Clean label:", "Tag:" and "Length:" (the length of clean_label)\n',
          'raw_label = "<<sraw>>"\nsensor_id = <<sid>>\nclean_label = raw_label.strip().title()\ntag = "<<stag>>-" + str(sensor_id).zfill(5)\nprint("Clean label:", clean_label)\nprint("Tag:", tag)\nprint("Length:", len(clean_label))\n',
          checks=[("var", "clean_label"), ("var", "tag")], hints=["raw_label.strip().title() does both cleanings in one line.", "zfill needs text, so wrap the id in str() first."], emoji="🏷️")

    c.add("sensor_data_types", "Sensor Data Types", "Data types", "know int, float, str and bool",
          [T("The scenario", "Every reading from the <<sn>> has a **type**, and the type decides what you can do with it. Wrong types are behind most beginner bugs. Today you meet the four basic ones."),
           T("The four basic types", "- `int`: whole numbers, like `<<sid>>`\n- `float`: numbers with a decimal point, like `<<sread>>`\n- `str`: text, like `\"<<sn>>\"`\n- `bool`: only `True` or `False`, with capital first letters\n\n```python\nprint(type(5))        # <class 'int'>\nprint(type(5.0))      # <class 'float'>\nprint(type(\"5\"))      # <class 'str'>\nprint(type(True))     # <class 'bool'>\n```"),
           T("Same look, different type", "`5`, `5.0` and `\"5\"` look alike and are three different things. `\"True\"` in quotes is **text**, not a bool. Use `type()` to find out what you are really holding."),
           P("print(type(4.0))", "<class 'float'>", ["<class 'int'>", "4.0"], "A number with a decimal point is a float, even when it is a whole value like 4.0."),
           Q("Which of these is a bool?", ["True", "\"True\"", "1"], 0, "`True` without quotes is a bool. In quotes it is just text.")],
          "The four variables below have the wrong types, because they were typed in as text. Fix them so `sensor_id` is an int, `reading` is a float, `sensor_name` is text and `is_online` is a bool. Then print the type of each. It should print:\n\n<<OUT>>",
          'sensor_id = "<<sid>>"\nreading = "<<sread>>"\nsensor_name = "<<sn>>"\nis_online = "True"\nprint(type(sensor_id))\nprint(type(reading))\nprint(type(sensor_name))\nprint(type(is_online))\n',
          'sensor_id = <<sid>>\nreading = <<sread>>\nsensor_name = "<<sn>>"\nis_online = True\nprint(type(sensor_id))\nprint(type(reading))\nprint(type(sensor_name))\nprint(type(is_online))\n',
          checks=[("var", "sensor_id", True), ("var", "reading", True), ("var", "sensor_name", True), ("var", "is_online", True)],
          hints=["Remove the quotes from numbers.", "True has no quotes and a capital T."], emoji="🧬")

    c.add("identifying_sensors", "Identifying Sensors", "Identify types", "identify a value's type with type() and isinstance()",
          [T("The scenario", "A raw feed from the field delivers four unlabelled values. Before the <<system>> can use them, you must work out what each one is. This is a task you will do on real data your whole career."),
           T("Asking Python", "`type(x)` gives the full type. For a cleaner answer use `.__name__`:\n\n```python\nprint(type(5).__name__)         # int\nprint(type(\"5\").__name__)       # str\n```\n\n`isinstance(x, int)` answers True or False:\n\n```python\nprint(isinstance(5, int))       # True\n```"),
           T("A famous quirk", "In Python a `bool` is secretly a kind of `int`: `True` behaves like 1 and `False` like 0. So `isinstance(True, int)` is `True`. When it matters, check for `bool` first."),
           P("print(isinstance(True, int))", "True", ["False", "!TypeError"], "bool is built on top of int in Python, so True counts as an int."),
           Q("What type is \"<<sid>>\" (with quotes)?", ["str", "int", "float"], 0, "Anything inside quotes is text, even if it only contains digits.")],
          "Print the type name of each feed value, one per line, then print whether `feed_d` is an int. It should print:\n\n<<OUT>>",
          'feed_a = <<sid>>\nfeed_b = "<<stext>>"\nfeed_c = <<sread>>\nfeed_d = True\n# print the type name of feed_a, feed_b, feed_c and feed_d (one per line)\n# then print isinstance(feed_d, int)\n',
          'feed_a = <<sid>>\nfeed_b = "<<stext>>"\nfeed_c = <<sread>>\nfeed_d = True\nprint(type(feed_a).__name__)\nprint(type(feed_b).__name__)\nprint(type(feed_c).__name__)\nprint(type(feed_d).__name__)\nprint(isinstance(feed_d, int))\n',
          hints=["print(type(feed_a).__name__) gives just the name.", "The last line is print(isinstance(feed_d, int))."], emoji="🔎")

    c.add("dynamic_logs", "Dynamic Logs (F-Strings)", "Log lines", "build log lines with f-strings",
          [T("The scenario", "Operators scan the log all day, so every line must be **clear and consistent**. Gluing text and numbers with commas gets messy. Python has a neater tool for building messages: the f-string."),
           T("F-strings", "Put an `f` before the opening quote, and write variables inside curly braces:\n\n```python\nname = \"Ada\"\nscore = 91.456\nprint(f\"{name} scored {score}\")\n```\n\nAnything Python can calculate works inside the braces:\n\n```python\nprint(f\"Double: {score * 2}\")\n```"),
           T("Formatting numbers", "After a colon you can control how a number looks:\n\n```python\nprint(f\"{score:.1f}\")    # 91.5   (1 decimal place)\nprint(f\"{score:.2f}\")    # 91.46\nprint(f\"{score:+.2f}\")   # +91.46  (always show the sign)\n```"),
           P('x = 3.14159\nprint(f"{x:.2f}")', "3.14", ["3.1", "3.15"], "`.2f` rounds to 2 decimal places, so 3.14159 becomes 3.14."),
           Q("Which line builds the message correctly?", ["print(f\"Count: {n}\")", "print(\"f Count: {n}\")", "print(f\"Count: n\")"], 0, "The `f` goes before the quote, and the variable goes inside braces.")],
          "The variables are ready. Write three f-string log lines. It should print:\n\n<<OUT>>\n\nThe second line shows the reading with 2 decimals, and the third shows the gap to the target with its sign.",
          'tag = "<<stag>>"\nsensor_id = <<sid>>\nsensor_name = "<<sn>>"\nreading = <<sread>>\ntarget_reading = <<starget>>\nunit = "<<sunit>>"\n# Line 1: [tag-sensor_id] sensor_name: reading unit\n# Line 2: Reading (2 dp): reading with 2 decimals, then unit\n# Line 3: Gap to target: reading minus target_reading, with sign and 2 decimals, then unit\n',
          'tag = "<<stag>>"\nsensor_id = <<sid>>\nsensor_name = "<<sn>>"\nreading = <<sread>>\ntarget_reading = <<starget>>\nunit = "<<sunit>>"\nprint(f"[{tag}-{sensor_id}] {sensor_name}: {reading} {unit}")\nprint(f"Reading (2 dp): {reading:.2f} {unit}")\nprint(f"Gap to target: {reading - target_reading:+.2f} {unit}")\n',
          checks=[("ast", "JoinedStr", "an f-string")], hints=["The square brackets in line 1 are plain text. Only names go in braces.", "{reading:.2f} formats a number to 2 decimals. {value:+.2f} adds the sign."], emoji="🧾")

    c.add("empty_slots", "Empty Slots (NoneType)", "Nothing yet", "use None for \"no value yet\"",
          [T("The scenario", "The <<system>> keeps the last alert it raised. At the start of the day there **is no alert yet**. Writing 0 or an empty text for \"nothing\" would be a lie, because 0 is a real number. Python has a special value for \"no value\"."),
           T("None", "`None` means \"nothing here\". It has its own type, `NoneType`, and it is not 0 and not an empty string.\n\n```python\nlast_alert = None\nprint(last_alert)            # None\nprint(last_alert is None)    # True\n```\n\nCheck for it with `is None`, not with `==`."),
           T("Filling it in later", "A variable that starts as `None` can be given a real value later:\n\n```python\nlast_alert = \"Door open\"\nprint(last_alert is None)    # False\n```\n\n`None` is the honest way to say \"not known yet\"."),
           P("x = None\nprint(x is None, type(x).__name__)", "True NoneType", ["False NoneType", "None NoneType"], "x holds None, so `x is None` is True, and its type is called NoneType."),
           Q("Which is the best starting value for \"no alert yet\"?", ["None", "0", "\"\""], 0, "0 and an empty string are real values. None says clearly that there is no value.")],
          "Start with no alert, check it, then raise an alert and check again. It should print:\n\n<<OUT>>",
          "# Start with no alert and print it, then print whether it is None\n# Then set the alert to \"<<sn>> out of range\", print it, and print whether it is None\n",
          'last_alert = None\nprint(last_alert)\nprint(last_alert is None)\nlast_alert = "<<sn>> out of range"\nprint(last_alert)\nprint(last_alert is None)\n',
          checks=[("var", "last_alert", True)], hints=["last_alert = None starts it empty (no quotes).", "print(last_alert is None) shows True or False."], emoji="🕳️")

    c.add("waiting_game", "The Waiting Game", "Order of events", "use a value only after it exists",
          [T("The scenario", "Probes answer **when they are ready**, not when you ask. The program must wait for the value before it calculates with it. Today's code asks for the reading a moment too early."),
           T("Top to bottom", "Python runs line by line. A variable must be given a value **above** the line that uses it. Using a name that does not exist yet is a `NameError`. Using a placeholder `None` in maths is a `TypeError`:\n\n```python\nreading = None\nprint(reading + 1.5)      # TypeError: None + float\n```"),
           T("The fix is order", "Put the line that **fills in** the value before the line that **uses** it:\n\n```python\nreading = None            # waiting\nreading = 4.5             # the probe answers\nprint(reading + 1.5)      # now it works\n```\n\nWhen a crash mentions `None`, look at the order of your lines first."),
           P("x = None\nprint(x + 1)", "!TypeError", ["1", "None"], "None is not a number, so adding to it is a TypeError."),
           Q("What error does `None + 1.5` raise?", ["TypeError", "NameError", "ZeroDivisionError"], 0, "None and a float are the wrong kinds of things to add, which is a TypeError.")],
          "The code asks for the reading before the probe has answered. Reorder the lines so it works. It should print:\n\n<<OUT>>",
          'latest_reading = None\nprint("Waiting for <<sn>>...")\nadjusted = latest_reading + 1.5\nlatest_reading = <<sread>>\nprint(f"Adjusted reading: {adjusted}")\n',
          'latest_reading = None\nprint("Waiting for <<sn>>...")\nlatest_reading = <<sread>>\nadjusted = latest_reading + 1.5\nprint(f"Adjusted reading: {adjusted}")\n',
          checks=[("var", "adjusted")], hints=["Which two lines are in the wrong order?", "The value must arrive before it is used in adjusted."], emoji="⏳")

    c.add("shape_shifting", "Shape-Shifting Data", "Converting types", "convert between types",
          [T("The scenario", "The log file gives you everything as text: the id as text, the reading as text. To calculate, the <<system>> must turn each into the right type. This is called **type conversion** and it is a daily chore in data work."),
           T("The converters", "- `int(\"12\")` gives 12\n- `float(\"3.5\")` gives 3.5\n- `str(12)` gives \"12\"\n- `int(3.9)` gives **3**: it cuts off the decimals, it does not round\n- `bool(0)` is False, and any other number is True\n\n```python\nprint(int(\"12\") + 1)    # 13\nprint(float(\"3.5\") * 2) # 7.0\n```"),
           T("When conversion fails", "Python converts only what makes sense. `int(\"abc\")` raises a **ValueError**: the type is right (text) but the value cannot become a number. In a later chapter you will learn to handle that gracefully."),
           P('print(int(3.9), float("2"))', "3 2.0", ["4 2.0", "3.9 2"], "int() chops off the decimals, so 3.9 becomes 3. float(\"2\") gives 2.0."),
           Q("What does int(-2.7) give?", ["-2", "-3", "2"], 0, "int() drops the decimals towards zero, so -2.7 becomes -2.")],
          "The raw values arrived as text. Convert them, then print each with its type name. It should print:\n\n<<OUT>>\n\nThe last line is the reading with its decimals cut off.",
          'raw_reading = "<<stext>>"\nraw_id = "<<sid>>"\n# reading: a float made from raw_reading\n# sensor_id: an int made from raw_id\n# print reading and its type name, then sensor_id and its type name\n# finally print int(reading)\n',
          'raw_reading = "<<stext>>"\nraw_id = "<<sid>>"\nreading = float(raw_reading)\nsensor_id = int(raw_id)\nprint(reading, type(reading).__name__)\nprint(sensor_id, type(sensor_id).__name__)\nprint(int(reading))\n',
          checks=[("var", "reading", True), ("var", "sensor_id", True)], hints=["float(raw_reading) converts text to a decimal.", "type(x).__name__ gives the type's name."], emoji="🎭")

    c.add("flexibility_trap", "The Flexibility Trap", "Dynamic typing", "avoid changing a variable's type by accident",
          [T("The scenario", "Python lets a variable hold a number now and text a moment later. That flexibility is convenient and dangerous. A teammate reused the `threshold` variable for a label, and the maths below it quietly broke."),
           T("Dynamic typing", "Python does not fix a variable's type. The **value** has a type, and the name can move to a different value any time:\n\n```python\nx = 5\nx = \"five\"\n```\n\nThis is called **dynamic typing**. The danger is that the code far below still thinks `x` is a number."),
           T("Silent or loud", "Sometimes the result is a loud TypeError. Sometimes it is silently wrong: `\"5\" * 2` is `\"55\"`, not 10, and no error appears. The cure is simple: one variable, one meaning. Use a new name for the label."),
           P('x = 5\nx = "5"\nprint(x * 2)', "55", ["10", "!TypeError"], "x is now text, and text times 2 repeats it: \"55\". No error, but the wrong answer."),
           Q("What is the best fix when a number variable needs a text label too?", ["Use a second variable for the label", "Change the type and hope", "Delete the number"], 0, "Keep each variable to one meaning. A separate name costs nothing.")],
          "The `threshold` variable was changed to text, which breaks the maths. Keep `threshold` as a **number**, store the label in a new variable called `threshold_label`, and print the label as a last extra line. It should print:\n\n<<OUT>>",
          'threshold = <<level>>\nprint("Threshold:", threshold)\nthreshold = "<<level>> units"\nprint("Double:", threshold * 2)\nprint("Plus ten:", threshold + 10)\n',
          'threshold = <<level>>\nprint("Threshold:", threshold)\nthreshold_label = "<<level>> units"\nprint("Double:", threshold * 2)\nprint("Plus ten:", threshold + 10)\nprint("Label:", threshold_label)\n',
          checks=[("var", "threshold", True), ("var", "threshold_label")], hints=["Do not overwrite threshold with text.", "Give the text its own variable name."], emoji="🪤")

    c.add("legacy_plus", "Legacy Systems (+)", "Legacy data", "know what + does with numbers and with text",
          [T("The scenario", "An old system exports every value as text: <<q1>> units and a delivery of <<d>>. Someone in finance adds them with `+` and gets a strange result. The humble `+` does **two different jobs**."),
           T("One symbol, two jobs", "- on **numbers**, `+` adds\n- on **strings**, `+` joins them end to end\n\n```python\nprint(2 + 3)           # 5\nprint(\"2\" + \"3\")       # 23\n```\n\nAnd `*` on a string repeats it:\n\n```python\nprint(\"-\" * 10)        # ----------\n```"),
           T("Which job do you want?", "Python decides by looking at the **types**. If you want a sum, convert text to numbers first. If you want a label, convert numbers to text first. Never rely on the data to be the type you hope for."),
           P('print("ab" * 3, 2 + 3)', "ababab 5", ["ab3 5", "ababab 23"], "Multiplying text repeats it three times. 2 + 3 on numbers is 5."),
           Q("What is \"24\" + \"20\" ?", ["\"2420\"", "44", "An error"], 0, "Both are text, so + joins them: \"2420\".")],
          "Both legacy values are text. Print a divider, show both ways of using `+`, and print the divider again. It should print:\n\n<<OUT>>",
          'legacy_units = "<<q1>>"\nlegacy_delivery = "<<d>>"\n# print a divider: 20 "=" characters (multiply text by a number)\n# print "Joined as text:" and the two values joined with +\n# print "Added as numbers:" and the two values added after converting them\n# print the divider again\n',
          'legacy_units = "<<q1>>"\nlegacy_delivery = "<<d>>"\nprint("=" * 20)\nprint("Joined as text:", legacy_units + legacy_delivery)\nprint("Added as numbers:", int(legacy_units) + int(legacy_delivery))\nprint("=" * 20)\n',
          hints=["print(\"=\" * 20) draws the divider.", "int() both values before adding them."], emoji="🏚️")

    c.add("spatial_coordinates", "Spatial Coordinates", "Positions", "group values into a tuple and unpack it",
          [T("The scenario", "The <<sn>> sits at a known <<spos>>: two numbers that belong together. Keeping them in two loose variables invites mistakes. Python can bundle them into one value."),
           T("Tuples", "A **tuple** is a fixed group of values in round brackets:\n\n```python\nposition = (12, 4)\nprint(position[0])    # 12  (first item, counting from 0)\nprint(position[1])    # 4\n```\n\nA tuple **cannot be changed** after it is made. `position[0] = 5` is a TypeError. That is a feature: it keeps coordinates safe."),
           T("Unpacking and swapping", "You can pull a tuple apart into separate variables in one line:\n\n```python\nx, y = position\n```\n\nAnd swapping two variables needs no helper:\n\n```python\nx, y = y, x\n```"),
           P("p = (4, 9)\nx, y = p\nprint(y, x)", "9 4", ["4 9", "!ValueError"], "x gets 4 and y gets 9, and print shows y first, then x."),
           Q("Can you change one item of a tuple after it is made?", ["No, tuples are fixed", "Yes, with an index", "Only if it holds numbers"], 0, "Tuples are immutable. You make a new tuple instead.")],
          "Unpack the position into `x` and `y`, print it, swap the two values, and print again. It should print:\n\n<<OUT>>",
          "# <<spos>> of the <<sn>>\nposition = (<<sx>>, <<sy>>)\n# unpack it into x and y, then print \"Position:\" and x and y\n# swap the two values with one line, then print \"Swapped:\" and x and y\n",
          'position = (<<sx>>, <<sy>>)\nx, y = position\nprint("Position:", x, y)\nx, y = y, x\nprint("Swapped:", x, y)\n',
          checks=[("var", "position", True)], hints=["x, y = position unpacks both at once.", "x, y = y, x swaps them."], emoji="📍")

    c.add("clean_code", "Clean Code", "Clean code", "rename and tidy code without changing what it does",
          [T("The scenario", "Six months from now, you will open this file and not remember what `c` was. Code is read far more often than it is written. A teammate left you a working but cryptic snippet, and your job is to make it readable without changing its output."),
           T("What clean code looks like", "- **Names say what a value is**: `<<vt>>`, not `c`\n- **Constants** for fixed rules: `<<VL>>`, not a bare number\n- **Spaces** around operators: `a = b * c`, not `a=b*c`\n- **Comments** that explain why, kept short\n\nWhen you rename, the output must stay **exactly the same**. Renaming is risky, so always run before and after."),
           T("Why it pays", "Teams spend most of their time reading code. Clean code is faster to review, easier to debug, and much kinder to the next person, who may be you."),
           Q("Which name is best for the total value of the stock?", ["<<vt>>", "c", "x1"], 0, "A name that says what the value is removes the need for a comment.")],
          "Make this snippet readable **without changing its output**:\n\n- Rename `a`, `b`, `c` to `<<vq>>`, `<<vr>>` and `<<vt>>`\n- Rename `d` to the constant `<<VL>>`\n- Add spaces around `=` and `*`, and one comment of your own\n\nIt must still print:\n\n<<OUT>>",
          'a=<<q1>>\nb=<<p1>>\nc=a*b\nd=<<level>>\nprint(c,d)\n',
          '# Value of the first <<thing>>, and the rule number\n<<vq>> = <<q1>>\n<<vr>> = <<p1>>\n<<vt>> = <<vq>> * <<vr>>\n<<VL>> = <<level>>\nprint(<<vt>>, <<VL>>)\n',
          checks=[("var", c.ctx["vt"]), ("var", VL), ("absent", "a"), ("absent", "b"), ("absent", "c"), ("absent", "d"), ("comments", 1)],
          hints=["Rename a to <<vq>>, b to <<vr>> and c to <<vt>> in every line they appear.", "Constants use UPPER_CASE: <<VL>>."], emoji="✨")

    c.add("log_diagnostics", "Log Diagnostics", "Log reading", "search and slice text",
          [T("The scenario", "When a probe misbehaves, the first thing engineers do is read its **log**: lines of text with a timestamp, a level and a message. Python can count, search and cut text far faster than a person scrolling."),
           T("Multi-line text", "Three quote marks in a row make a string that can span lines:\n\n```python\nlog = \"\"\"08:00 INFO ok\n08:05 WARN hot\"\"\"\n```\n\nUseful tools:\n\n- `log.count(\"WARN\")` how many times a word appears\n- `log[:5]` the first 5 characters (slicing)\n- `log.find(\"WARN\")` the position where it first appears\n- `len(log)` the number of characters"),
           T("Slicing", "`text[start:end]` takes a piece. The start is included and the end is not, and counting begins at 0:\n\n```python\nword = \"python\"\nprint(word[0:3])   # pyt\nprint(word[:2])    # py\nprint(word[2:])    # thon\n```"),
           P('s = "banana"\nprint(s.count("an"), s[:3])', "2 ban", ["3 ban", "2 nan"], "\"an\" appears twice in banana, and s[:3] is the first three letters, ban."),
           Q("What does text[:5] give?", ["The first 5 characters", "Everything except the first 5", "The last 5 characters"], 0, "Leaving the start empty means \"from the beginning\", and the end 5 is not included.")],
          "Read the log with Python. It should print:\n\n<<OUT>>",
          'log = """08:00 INFO <<stag>> online\n08:05 WARN <<stag>> reading high\n08:10 ERROR <<stag>> no signal\n08:15 WARN <<stag>> reading high"""\n# print: Warnings: (count of WARN)\n# print: Errors: (count of ERROR)\n# print: First timestamp: (the first 5 characters)\n# print: First ERROR starts at character: (its position)\n',
          'log = """08:00 INFO <<stag>> online\n08:05 WARN <<stag>> reading high\n08:10 ERROR <<stag>> no signal\n08:15 WARN <<stag>> reading high"""\nprint("Warnings:", log.count("WARN"))\nprint("Errors:", log.count("ERROR"))\nprint("First timestamp:", log[:5])\nprint("First ERROR starts at character:", log.find("ERROR"))\n',
          hints=["log.count(\"WARN\") counts a word.", "log[:5] takes the first five characters."], emoji="📜")

    c.add("telemetry_averages", "Telemetry Averages", "Averages", "summarise readings with sum, min, max and round",
          [T("The scenario", "One reading tells you little. Five readings tell you a **trend**. The <<system>> will report the average, the lowest, the highest and the spread of the <<sn>>. Python has built-in helpers for all of it."),
           T("A first look at lists", "A **list** holds many values in square brackets. (You will learn it fully in a later chapter.)\n\n```python\nreadings = [4.0, 6.5, 5.5]\n```\n\nThree functions summarise a list in one call:\n\n- `sum(readings)` adds everything\n- `len(readings)` counts the items\n- `min(readings)` and `max(readings)` find the smallest and largest"),
           T("Average and rounding", "The **average** is the sum divided by the count. `round(x, 2)` rounds to 2 decimal places:\n\n```python\naverage = sum(readings) / len(readings)\nprint(round(average, 2))\n```\n\nThe **spread** is the highest minus the lowest."),
           P("print(min(4, 9, 2), max(4, 9, 2))", "2 9", ["4 9", "2 2"], "min picks the smallest of the three, max the largest."),
           Q("How do you get the average of a list?", ["sum(readings) / len(readings)", "max(readings) / 2", "len(readings) / sum(readings)"], 0, "Total divided by how many there are.")],
          "Summarise the five readings. It should print:\n\n<<OUT>>",
          "readings = <<sreads>>\n# average: the sum divided by the count\n# print Average (rounded to 2 decimals), Lowest, Highest and Spread (highest minus lowest)\n",
          'readings = <<sreads>>\naverage = sum(readings) / len(readings)\nprint("Average:", round(average, 2))\nprint("Lowest:", min(readings))\nprint("Highest:", max(readings))\nprint("Spread:", max(readings) - min(readings))\n',
          checks=[("var", "average")], hints=["average = sum(readings) / len(readings)", "Spread is max(readings) - min(readings)."], emoji="📈")

    c.add("diagnostics_report", "System Diagnostics Report", "Chapter 2 project", "combine variables, types and formatting into a report",
          [T("The scenario", "Chapter two ends with a real deliverable: the **diagnostics report** that the <<system>> prints every morning. It uses everything you learned: variables, types, formatting, None, comparisons of values and f-strings."),
           T("Plan the report", "A report is a list of lines, each answering one question:\n\n- Which probe, and is it online?\n- What was the last reading, and how far from target?\n- What is the average of the recent readings?\n- Has an alert been raised?\n- What does the core record say?\n\nWrite one `print` for each, using f-strings. Run often."),
           T("Make it tidy", "Use `\"=\" * 34` for the top and bottom rules, one decimal place for readings, and a signed gap. Consistent formatting is what makes a report feel trustworthy."),
           Q("Why use f-strings for a report line?", ["They mix text and values cleanly and format numbers", "They run faster than everything else", "They are the only way to print numbers"], 0, "F-strings keep the text and the values together in one readable line.")],
          "Print the diagnostics report. All the data is set up for you, so only the printing is left. It must look exactly like this:\n\n<<OUT>>",
          'sensor_name = "<<sn>>"\nsensor_id = <<sid>>\nis_online = True\nreading = <<sread>>\ntarget_reading = <<starget>>\nunit = "<<sunit>>"\nreadings = <<sreads>>\naverage = sum(readings) / len(readings)\nlast_alert = None\n# Write the report below, one print per line, using f-strings\n',
          'sensor_name = "<<sn>>"\nsensor_id = <<sid>>\nis_online = True\nreading = <<sread>>\ntarget_reading = <<starget>>\nunit = "<<sunit>>"\nreadings = <<sreads>>\naverage = sum(readings) / len(readings)\nlast_alert = None\nprint("=" * 34)\nprint("<<system>> DIAGNOSTICS: <<biz>>")\nprint("=" * 34)\nprint(f"Probe: {sensor_name} (#{sensor_id}) online={is_online}")\nprint(f"Last reading: {reading:.1f} {unit}")\nprint(f"Target: {target_reading} {unit}, gap {reading - target_reading:+.1f}")\nprint(f"Average of {len(readings)} readings: {average:.2f}")\nprint(f"Alert: {last_alert}")\nprint(f"Core record: {<<vn>>}, {<<vq>>} <<qty_unit>>, worth {<<vt>>}")\nprint("=" * 34)\n',
          checks=[("prints", 9), ("ast", "JoinedStr", "f-strings")],
          hints=["The two rules at the top and bottom are print(\"=\" * 34).", "{reading:.1f} shows one decimal. {reading - target_reading:+.1f} shows the gap with its sign.", "The core record line uses the variables from lessons one and four."], emoji="📋")
