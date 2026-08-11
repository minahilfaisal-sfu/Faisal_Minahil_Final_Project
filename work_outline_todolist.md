## D-SymBIA Project Status

### Done — Phase 1 (EDA & KPI Engineering)
- [x] Loaded and documented all 5 source tables (crops, locations, resource loops, scenario-crop-locations, scenario-resource-loops)
- [x] Logged known data quality issue (missing fields in `resource_loops.csv` row 16 — not blocking)
- [x] Data referential integrity checks (no bad IDs, no duplicates)
- [x] Scenario complexity profiling (locations/crops/loops per scenario)
- [x] Resolved `usage_fraction` gap (assumed 1.0, documented)
- [x] Built `scenario_kpi_df` with exactly 300 rows × 12 KPIs
- [x] KPI distributions + skewness check (flagged KPIs for log-transform in Phase 2)
- [x] Correlation heatmap
- [x] Fixed row-count discrepancy in documentation table (1,143 / 770, matching actual `.shape` output)
- [x] Fixed duplicate EDA section header
- [x] Fixed typos flagged in review (compatability, log-tranforming, absorbtion, etc.)

### Done — Phase 2 (Modelling)
- [x] **Problem A (Unsupervised - Clustering):** Log-transformed + scaled KPIs, elbow/silhouette analysis justifying k=4, K-Means clustering, PCA 2D visualization with cluster centers, interpretable category labels, profile bar charts.
- [x] **Problem B (Supervised - Classification):** Pre-KPI design-choice feature engineering (deliberately excluding KPI-derived columns to avoid circularity), Decision Tree with GridSearchCV tuning, ~73% test accuracy, confusion matrix + feature importance chart.

### Done — Documentation
- [x] Assumptions Log: consolidated as its own notebook section (Phase 1 + Phase 2 items) and expanded in `assumptions_and_future_work.md`
- [x] Limitations section added to notebook
- [x] Executive Summary added to notebook (plain-language, stakeholder-facing)

### In progress / Not started
- [ ] Links section added to notebook
- [ ] Record the 5-minute video presentation and add the link to the notebook's Links section
- [ ] (Optional, +10% bonus) Build Streamlit app for scenario comparison and visualizations, add link to notebook's Links section
- [ ] Final read-through of notebook end-to-end after re-running all cells, to confirm no errors post-edits