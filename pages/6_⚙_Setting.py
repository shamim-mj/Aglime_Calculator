import streamlit as st

color_cont1, color_cont2 = st.columns([1, 2])
color_cont1.markdown("<h5 style='text-align: center; color: white; background-color: #0033A0;'>Choose color palette</h5>", unsafe_allow_html=True)

pallete = color_cont1.selectbox("pallete", ["Dark2","Accent", "Accent_r", "autumn", "Blues", "Blues_r", "bright", "BuGn", 
    "BuGn_r", "BuPu", "BuPu_r", "binary", "binary_r", "bone", "bone_r", "bwr", "colorblind",  "cool", "coolwarm", "copper", "cubehelix", "dark",
    "Dark2_r", "deep","GnBu", "GnBu_r", "gnuplot" ,"gnuplot2","Greens", "Greens_r", "Greys", "Greys_r" ,"gray", "hot", "hot_r" ,"jet_r","nipy_spectral", "muted",
    "OrRd", "OrRd_r","ocean", "ocean_r" ,"Oranges", "Oranges_r", "PRGn", "PRGn_r", "pink", "pink_r" ,"Paired", "Paired_r","pastel", "Pastel1", "Pastel1_r",
    "Pastel2", "Pastel2_r", "PiYG", "PiYG_r",  "PuBu", "PuBuGn", "PuBuGn_r", "PuBu_r", "PuOr", "PuOr_r", "PuRd", "PuRd_r",
    "Purples", "Purples_r","rainbow","rainbow_r" ,"RdBu", "RdBu_r", "RdGy", "RdGy_r", "RdPu", "RdPu_r", "RdYlBu", "RdYlGn", "Reds", "Reds_r", "Set1", "Set1_r",
    "Set2", "Set2_r", "Set3", "Set3_r", "Spectral", "Spectral_r" , "seismic", "seismic_r" ,"spring","spring_r", "summer","summer_r", "YlGn", "YlGnBu", "YlOrBr", "YlOrRd",
    "prism", "terrain", "terrain_r","winter", "winter_r"], label_visibility ='collapsed')

st.session_state['pallete'] = pallete