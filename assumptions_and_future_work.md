### Assumption Log:

- **`usage_fraction`**: The KPI guideline specifies a random `usage_fraction` (0.4–1.0) per scenario-location representing how much of a zone's area is actually cultivated. However, as no such column exists in the scenario datasets, we will assume that **`usage_fraction = 1.0`**, i.e., the full location area is available for cultivation and that full area is evenly split across the crop-systems placed at that location.

- The compatibility KPI is calculated using summer seasonal values only, according to the proposal's KPI guideline. Location data also includes spring/autumn/winter DLI, temperature, humidity, and radiation ranges that are not currently incorporated into the KPI calculation. A possible issue with this is that a scenario with high compatability in the summers might not fair well in the rest of the seasons.

**Possible future work:**
- As seasonal data exists in the datasets, we can use all 4 for calculation / visualization of KPIs by grouping by season, and giving them a `season_compatibility_score` or similar to achieve more accurate scores and trade-off data for analysis.
- As the humidity columns exist for all 4 seasons, we can also take humidity into consideration when calculating the `compatibility_pct` KPI, and provide visualizations of trade-offs per scenario per season.