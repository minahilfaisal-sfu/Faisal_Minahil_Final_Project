## D-SymBIA Project Status

### Done — Phase 1 (EDA & KPI Engineering)
- [x] Loaded and documented all 5 source tables (crops, locations, resource loops, scenario-crop-locations, scenario-resource-loops)
- [x] Logged known data quality issue (missing fields in `resource_loops.csv` row 16 — not blocking)
- [x] Data referencial integrity checks (no bad IDs, no duplicates)
- [x] Scenario complexity profiling (locations/crops/loops per scenario)
- [x] Resolved `usage_fraction` gap (assumed 1.0, documented)
- [x] Built `scenario_kpi_df` with exactly 300 rows × 12 KPIs
- [x] KPI distributions + skewness check (flagged KPIs for log-transform in Phase 2)
- [x] Correlation heatmap
- [x] Assumptions Log (usage_fraction, summer-only compatibility, humidity exclusion, data gaps)

### In progress
- [ ] Log transform flagged KPI before clustering and classification
- [ ] Further explore KPIs and their trends (if needed)
- [ ] Fix assumptions and future work md to make it easier to read and follow + add further assumptions made in phase 2.

### Not started — Phase 2 (Modeling)
- [ ] **Problem A (Unsupervised - Clustering):** Given a set of scenarios, each with engineered performance KPIs (yield, resource intensity, circularity), discover natural performance categories, which are basically clusters of scenarios that share similar trade-off profiles. This aims to allow users to quickly see "high-yield/resource-heavy" vs. "modest-yield/circular" groupings rather than reading a flat table of multiple scenarios.
- [ ] **Problem B (Supervised - Classification):** Given only a scenario's design choices (which crops, which location types, which resource loop categories), i.e., information available before a full scenario is generated and its KPIs computed, we want to predict which performance category it potentially belongs to, so that a user can see the categorization within the generation step itself, while making choices, instead of making decisions, then viewing the evaluation at the end of the generation and exploration step.

### Not started — Documentation & Deliverables
- [ ] Limitations
- [ ] 5-minute recorded presentation
- [ ] Streamlit app for scenario comparison and visualizations (Optional)
