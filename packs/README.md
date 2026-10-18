# Industry packs

One JSON file per industry. `validate.py` loads every `*.json` here (files starting with `_` are ignored)
and reports anything missing. Easiest start: copy `retail.json`.

| Field | What it is |
|---|---|
| `key`, `order`, `label`, `icon`, `accent`, `tagline` | Identity and card in the picker. `accent` is a hex colour. |
| `biz`, `system`, `role` | The company, the program the learner builds, and their job title. |
| `thing`, `things` | What one record is called ("product", "cargo load"). |
| `records` | Exactly 4 rows of `[name, quantity, rate]`. Quantity is a whole number, rate may be a decimal. Total = quantity x rate. |
| `qty_unit`, `rate_unit` | Words after the numbers: "in stock", "per pack". |
| `rp`, `rs`, `tp`, `ts` | Prefix and suffix for a rate and for a total: `$` and "", or "" and " Mbps". |
| `level`, `msg_le`, `msg_gt` | The rule number, the message when quantity is at or below it, and otherwise. The word before `:` is used in the final exam. |
| `missing`, `missing_msg` | An item the business does not have, and the message for it. |
| `delivery`, `delivery_note`, `stock_noun` | The number added in the debugging lesson, where it came from, and the word used in its output line. |
| `total_label`, `vw`, `alert_name` | The grand-total label, a word for module names, and the name of the rule module. |
| `opening`, `rule`, `scene` | Story text for lessons 1, 5 and 12. |
| `v` | The 13 variable and function names learners type. Use the trade's own words. |
| `cls` | The class in lesson 14: its name, attribute names, value method, and one `action` (below). |
| `probe` | The monitored device used in chapter 2: `name, tag, id, unit, reading` (negative where sensible), `target, readings` (5 numbers), `raw_label, text_reading, pos` (x, y), `pos_label, batch_word, batch_size`. |
| `py_uses` | Three short sentences: what Python is used for in this industry (lesson 1). |
| `world` | Optional. Name of the built-in 3D world to use: retail, pharmacy, logistics, farm, networking, support or ai. Default `retail`. |
| `glossary` | `[term, meaning, code name]` rows shown in the Guide tab. |

`cls.action.kind` is one of:

- `add`: `name(amount)` adds to the quantity and returns it
- `take`: `name(amount)` subtracts, and raises `ValueError(err)` if there is not enough
- `check`: `name()` returns whether quantity `cmp` (`>` or `<=`) the level

Text can use tokens such as `<<n1>>` (first record name), `<<q1>>`, `<<p1>>`, `<<level>>`, `<<biz>>`, `<<vq>>`.
Use only the same tokens the built-in packs use.
