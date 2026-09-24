# Sample data and limitations

`sample_orders.csv` contains 2,330 synthetic rows supplied with the original project. Its original generation code, random seed, and calibration are unavailable. Reproduction here means rerunning calculations against the **included CSV**, not regenerating identical source rows. None of its dates, categories, order totals or trajectories should be reported as observed business history.

| Column | Meaning in this example | Caveat |
| --- | --- | --- |
| `order_id` | Unique synthetic order key | No customer identity or repeat-customer linkage. |
| `month` | Synthetic YYYY-MM bucket | Not a recorded Chitaro Mart sales month. |
| `customer_familiarity` | Constructed `new` or `familiar` label | The file does not establish how familiarity was measured. `new` is not proof of a first purchase. |
| `acquisition_channel` | Constructed source label: `tiktok_creator`, `search`, `referral`, or `repeat_purchase` | `repeat_purchase` describes order behavior rather than an acquisition channel. These labels cannot establish attributable creator exposure. |
| `units` | Positive integer units on that synthetic order | Not the 16,000+ real business-wide units. |

The original dataset contains some rows labeled both `new` and `repeat_purchase`. Because there is no operational definition or customer history, the two fields must **not** be combined to assert first-time buyers or mutually exclusive acquisition paths. The analysis reports source labels exactly as provided and makes no causal or unique-customer claims.

Missing information includes customer ID, campaign exposure, marketing spend, order value, returns, margin, inventory, suppliers, delivery performance, location, weather events and actual closure timing. Do not use this dataset to calculate conversion, retention, return on ad spend, effect of strategy, weather losses or business closure risk.
