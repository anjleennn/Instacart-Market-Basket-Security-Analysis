import streamlit as st
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt

# --- 1. SETUP & PATH ---
st.set_page_config(page_title="Instacart Intelligence", layout="wide")

# This checks GitHub's folder first, then your local laptop folder
if os.path.exists('rules_output.csv'):
    path = 'rules_output.csv'
else:
    path = r'C:\Users\AnjleenK\Documents\rules_output.csv'

# --- 2. DATA LOADING ---
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

try:
    rules = load_data(path)
    
    # --- 3. CLEANING ---
    all_products = []
    for val in rules['antecedents']:
        clean_name = str(val).replace("frozenset({", "").replace("})", "").replace("'", "")
        if clean_name not in all_products:
            all_products.append(clean_name)
    all_products = sorted(all_products)

    # --- 4. DASHBOARD UI ---
    st.title("🛒 Instacart Recommendation & Anomaly Engine")
    st.sidebar.header("🔍 Product Recommender")
    selected_item = st.sidebar.selectbox("Select an item:", all_products)

    if selected_item:
        recs = rules[rules['antecedents'].str.contains(selected_item, na=False)].sort_values('lift', ascending=False)
        st.subheader(f"Because you bought: {selected_item}")
        cols = st.columns(3)
        for i, row in recs.head(3).iterrows():
            with cols[i % 3]:
                clean_res = str(row['consequents']).replace("frozenset({", "").replace("})", "").replace("'", "")
                st.metric(label="Recommended", value=clean_res)

    # --- 5. GRAPH ---
    st.header("🕸️ Association Network")
    fig, ax = plt.subplots(figsize=(10, 6))
    G = nx.DiGraph()
    for i, row in rules.head(15).iterrows():
        ant = str(row['antecedents']).replace("frozenset({", "").replace("})", "").replace("'", "")
        con = str(row['consequents']).replace("frozenset({", "").replace("})", "").replace("'", "")
        G.add_edge(ant, con)
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', ax=ax)
    st.pyplot(fig)

# --- 6. THE ERROR HANDLER (This was the syntax error!) ---
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Check if rules_output.csv exists in your Documents folder.")