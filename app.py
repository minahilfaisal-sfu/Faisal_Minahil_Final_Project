"""
D-SymBIA Scenario Builder and Prediction Tool

Pick ONE location, then any number of crops and resource ("flow") loops for
it. A decision tree predicts which of the 4 performance-trade-off clusters
(discovered via K-Means in the project notebook) the scenario falls into,
purely from design choices.

Command: streamlit run app.py
Needs these files in the same folder:
  - crops_systems.csv, locations.csv, resource_loops.csv (reference tables,
    used only to populate the dropdowns)
  - scenario_model.pkl (the fitted DecisionTreeClassifier + its feature_cols
    + its test accuracy, exported from the notebook's modelling section at the
    end of the notebook)
"""

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="D-SymBIA Scenario Builder and Prediction Tool", layout="wide")

# Cluster id -> performance category from the notebook
CLUSTER_CATEGORIES = {0: "powerhouse", 1: "modest", 2: "circular", 3: "water_light"}

# Styling (display name / description / color).
CLUSTER_METADATA = {
    "powerhouse": dict(
        name="High-Yield Powerhouse",
        description="Big food output and market value, but only mid-range circularity.",
        color="red",
    ),
    "modest": dict(
        name="Modest / Low-Intensity",
        description="Small footprint, low commitment - modest yield, resource use and circularity.",
        color="gray",
    ),
    "circular": dict(
        name="Circular / Resource-Efficient",
        description="Prioritizes closed-loop water & energy recovery over raw yield.",
        color="green",
    ),
    "water_light": dict(
        name="Water-Circular, Energy-Light",
        description="Strong water recovery, little to no energy offset.",
        color="blue",
    ),
}

# ----------------------- Data loading -----------------------
@st.cache_data(show_spinner="Loading D-SymBIA database files...")
def load_data():
    crops = pd.read_csv("crops_systems.csv")
    locations = pd.read_csv("locations.csv")
    resources = pd.read_csv("resource_loops.csv")

    # for the selection dropdowns
    # crops eg: Leafy Greens - Butterhead (Raised Beds)
    crops["display_name"] = (
        crops["crop_name"] + " - " + crops["cultivar"] + " (" + crops["bia_system"] + ")"
    )
    # location eg: Zone 1 - East (Vertical, 531 m²)
    locations["display_name"] = (
        "Zone " + locations["id"].astype(str) + " - " + locations["direction"]
        + " (" + locations["orientation"] + ", " + locations["area"].astype(str) + " m²)"
    )
    # resource eg: Vermicomposting - Compost (Amendment)
    resources["display_name"] = (
        resources["tech"] + " - " + resources["output_type"] + " (" + resources["category"] + ")"
    )

    return {"crops": crops, "locations": locations, "resources": resources}

# ----------------------- Model loading -----------------------
@st.cache_resource(show_spinner="Loading the trained model...")
def get_model():
    bundle = joblib.load("scenario_model.pkl")
    clf = bundle["clf"]
    feature_cols = bundle["feature_cols"]
    importances = pd.Series(clf.feature_importances_, index=feature_cols).sort_values(ascending=False)

    return {
        "clf": clf,
        "feature_cols": feature_cols,
        "feature_importances": importances,
        "test_accuracy": bundle["test_accuracy"],
    }


def design_features_for_selection(placements, resource_categories, feature_cols):
    place_df = pd.DataFrame(placements)  # columns: bia_system, direction
    place_dummies = pd.get_dummies(place_df[["bia_system", "direction"]], prefix=["bia", "dir"])
    crop_feats = place_dummies.mean().to_dict() if len(place_df) else {}

    res_df = pd.DataFrame({"category": resource_categories})
    res_dummies = pd.get_dummies(res_df[["category"]], prefix="res")
    res_feats = res_dummies.mean().to_dict() if len(res_df) else {}

    feats = {**crop_feats, **res_feats}
    return {col: feats.get(col, 0.0) for col in feature_cols if col.startswith(("bia_", "dir_", "res_"))}


def predict_selection_category(model, data, selected_crop_ids, selected_location_id, selected_loop_ids):
    crops, locations, resources = data["crops"], data["locations"], data["resources"]
    feature_cols = model["feature_cols"]

    sel_crops = crops[crops["crop_system_id"].isin(selected_crop_ids)]
    loc = locations[locations["id"] == selected_location_id].iloc[0]
    sel_loops = resources[resources["resource_loop_id"].isin(selected_loop_ids)]

    placements = [{"bia_system": c, "direction": loc["direction"]} for c in sel_crops["bia_system"]]
    feats = design_features_for_selection(placements, sel_loops["category"].tolist(), feature_cols)
    feats["n_crops"] = sel_crops["crop_system_id"].nunique()
    feats["n_locations"] = 1
    feats["total_area_m2"] = loc["area"]
    feats["n_resource_loops"] = len(sel_loops)

    X = pd.DataFrame([feats]).reindex(columns=feature_cols, fill_value=0.0)
    clf = model["clf"]
    pred_cluster = clf.predict(X)[0]
    proba = dict(zip(clf.classes_, clf.predict_proba(X)[0]))

    return {"cluster": pred_cluster, "category": CLUSTER_CATEGORIES[pred_cluster], "proba_by_cluster": proba}

# ----------------------- App UI ----------------------- 
data = load_data()
crops, locations, resources = data["crops"], data["locations"], data["resources"]
model = get_model()

st.title("D-SymBIA Scenario Builder and Prediction Tool")
st.write(
    "Pick one location, then any crops and flow (resource) systems for it. "
    "A decision tree predicts which performance-trade-off category the scenario falls into."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Location")
    location_selection = st.selectbox(
        "Building zone",
        options=locations["id"].tolist(),
        format_func=lambda i: locations.loc[locations["id"] == i, "display_name"].iloc[0],
        index=None,
        placeholder="Choose a location...",
        label_visibility="collapsed",
        key="location_select",
    )

with col2:
    st.subheader("Crops")
    crop_selection = st.multiselect(
        "Crop systems",
        options=crops["crop_system_id"].tolist(),
        format_func=lambda i: crops.loc[crops["crop_system_id"] == i, "display_name"].iloc[0],
        label_visibility="collapsed",
        key="crop_select",
    )

with col3:
    st.subheader("Flow Systems")
    loop_selection = st.multiselect(
        "Resource loops",
        options=resources["resource_loop_id"].tolist(),
        format_func=lambda i: resources.loc[resources["resource_loop_id"] == i, "display_name"].iloc[0],
        label_visibility="collapsed",
        key="loop_select",
    )

st.divider()

if location_selection is None or not crop_selection:
    st.info("Choose a location and at least one crop to see the predicted performance category.")
    st.stop()

result = predict_selection_category(model, data, crop_selection, location_selection, loop_selection)
category = CLUSTER_METADATA[result["category"]]
confidence = result["proba_by_cluster"][result["cluster"]]

st.subheader("Predicted performance category")

card_col, chart_col = st.columns([1.3, 1])

with card_col:
    with st.container(border=True):
        st.markdown(f"##### :{category['color']}[{category['name']}]")
        st.write(category["description"])
        st.metric("Confidence", f"{confidence:.1%}")

with chart_col:
    proba_df = pd.DataFrame(
        [
            {"Category": CLUSTER_METADATA[CLUSTER_CATEGORIES[c]]["name"], "Probability": p}
            for c, p in result["proba_by_cluster"].items()
        ]
    ).sort_values("Probability", ascending=True)
    st.bar_chart(proba_df.set_index("Category"), horizontal=True)

if len(loop_selection) == 0:
    st.write("No flow systems selected. This scenario currently has no circular-recovery tech.")

with st.expander("What's driving this prediction?"):
    st.write(
        "Top design-choice features by importance across the trained decision tree "
        f"(test accuracy on the notebook's test scenarios: {model['test_accuracy']:.0%})."
    )
    st.bar_chart(model["feature_importances"])
