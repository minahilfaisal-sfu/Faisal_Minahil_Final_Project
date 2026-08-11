# D-SymBIA Project - Assumptions & Future Work

## Assumption Log

### Phase 1 - Data & KPI Engineering

1. **`usage_fraction`**: The KPI guideline specifies a random `usage_fraction` (0.4–1.0) per scenario-location representing how much of a zone's area is actually cultivated. No such column exists in the scenario datasets, so we assume **`usage_fraction = 1.0`**, i.e., the full location area is available for cultivation, evenly split across the crop-systems placed at that location.
    - All footprint- and yield-derived KPIs (`total_footprint_m2`, `total_yield_kg`, `yield_per_m2`, `co2_uptake_kg`, `market_value_cad`) are computed at full-area scale rather than the partially-discounted scale the original spec implied.

2. **Summer-only compatibility**: The compatibility KPI is calculated using summer seasonal values only, per the proposal's KPI guideline. `locations.csv` also includes spring/autumn/winter DLI, temperature, humidity, and radiation ranges that are not currently incorporated. A scenario with high summer compatibility might not fare as well across the rest of the year.

3. **Humidity excluded from `compatibility_pct`**: Humidity ranges exist for all four seasons but are not part of the compatibility formula as defined in the KPI guideline, so they're excluded from that specific KPI.

4. **Per-placement vs. bundle KPI calculation**: I will need to update the client proposal description of scenario components that states scenarios as an "unordered bundle," with compatibility and yield computed "in aggregate across the bundle, not per exact placement." to actually be ordered and in pairs/groups. That was a revision error on my part in the proposal as the actual existing data is in pairs/groups.
    - The `scenario_crop_locations.csv` pairs each `crop_system_id` to a specific `location_id`, so placement data exists at the row level. This structure (compatibility/yield computed per crop-at-location, then aggregated to the scenario) should be used since the more granular data gives a more accurate result.

5. **Incompatible crops yield 30%, not 0%**: Crops that fail the compatibility check are assumed to still produce 30% of their potential yield (representing survival in suboptimal conditions) rather than 0%, so comparisons aren't too heavily skewed by scenarios producing nothing.

6. **Resource loops are scenario-level, not location-level**: Circular technologies are treated as serving the whole building/scenario, consistent with `scenario_resource_loops.csv` having no specific `location_id` column.

### Phase 2 - Modelling

7. **k = 4 for K-Means**: Neither the elbow curve nor the silhouette score gives one unambiguous answer (silhouette technically peaks near k=2, and keeps slowly climbing out to k≈40). We chose k=4 by balancing the subtle elbow bend against the practical need for a small number of human-interpretable categories that an architect or designer can use, instead of having >40 categories. A very large k would mostly just have small groups of 7-8 scenarios rather than representing the real underlying groupings.

8. **Cross-validated accuracy vs. test accuracy**: After tuning the Problem B Decision Tree with `GridSearchCV` params, the best cross-validated accuracy was **58.67%**, while accuracy on the test set came out higher, at **73.33%**. 
    - With only 300 scenarios (225 in the training split and 75 in the test split), this could be because of noise, not that the model isn't working correctly. We'll use the test-set's accuracy as our final number, though it might be somewhat inaccurate. The accuracy can be improved with a larger, real-world decision dataset for scenarios instead of it being generated via the script, and the model can train better, in order to improve accuracy and recall.

---

## Possible Future Work / Limitations

Items to revisit given more time:

- Use all four seasons for KPI calculation/visualization (e.g. a `season_compatibility_score` grouped by season) to give more accurate, year-round scores and expose seasonal trade-offs per scenario.
    - We can also add this option to select seasons in a streamlit app, where users can see KPI updates per season for their location and crop selections.
- Incorporate humidity into `compatibility_pct` because the seasonal humidity columns exist, and visualize the resulting trade-offs.
- Validate the `usage_fraction = 1.0` assumption against real client scenario data, rather than assuming a constant value and equal split per BIA system.
- Investigate why Cluster 0 has strong precision but weak recall (0.89 vs 0.44) in the Decision Tree classifier.
    - we could try adjusting class weights, in-depth fine-tuning with more paramters, or resampling/having a larger non-synthetic dataset.
- Re-check cluster count/stability for improvement: silhouette scores stay below 0.30 at k=4, meaning boundaries between cluster categories are soft. This can be because KPIs are mostly interlinked with each other, without being distinct. However, additional engineered features (e.g. seasonal KPIs) might help separate clusters more cleanly.
- KPI revision: I mention in the proposal that the KPI formulas are AI-drafted guidelines, open to revision. So we can recheck these formulas according to the real data, or derive new KPIs that may be more valuable to architects and designers in understanding scenario trade-offs. Further research would be required for this.
