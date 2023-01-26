import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


# Add a tile to the sources of the lime
st.markdown("<h2 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Lime and Soil Data</h2>", unsafe_allow_html=True)



# Lets make some empty dictionary to save data
# This is used to loop through the data in dynamic columns. You can use pandas dataframe directly too. 

quarries = {}
initial ={}
l8  = {}
l20 = {}
l60 = {}
wetw = {}
dryw = {}
recton = {}
lime_cost = {}
delivery_cost = {}
spreading_cost ={}
CCE = {}


# What kinda data does the user have? Here, I am setting a condition if the data is in percentage or weight
percent_weight = option_menu(None, ["Lab Results (Weight)", "Lab Results (Percentage)"], 
    icons=[], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffe6e6"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#ff0000"},
    }
)

# st.markdown("<h5 style='text-align: center; color: blue;'>" "</h5>", unsafe_allow_html=True)

# Lets loop through the columns
if percent_weight =="Lab Results (Weight)":
    f_container = st.container() # the reason for using container is to give a nice looking style to the title of samples
    samp_cont1, samp_cont2 = f_container.columns([1, 3])
    # samp_cont1.markdown("<h5 style='text-align: center; color: blue;'>" "</h5>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white; background-color: #0033A0;'>Lime Data</h4>", unsafe_allow_html=True)
    samp_cont1.markdown("<h5 style='text-align: center; color: white; background-color: #0033A0;'># Samples</h5>", unsafe_allow_html=True)
    ncol = samp_cont1.number_input("# Sample", 1, 5, 1, label_visibility='collapsed')
    cols = st.columns(ncol)
    step = 1e-1
    for i, x in enumerate(cols):
        st.session_state[f'Sample {i+1}'] = f'Sample {i+1}'
        quarries[i]= x.text_input('**Lime Source:**', placeholder = st.session_state[f'Sample {i+1}'], key = f"q_{i}_name")
        initial[i] = x.number_input('**Initial Amount (g)**: ', value = 550.00, step = step ,key = f"q_{i}_initial", format="%.2f")
        l8[i] = x.number_input('**Amount < #8 (g)**: ', value = 430.00, step = step ,key = f"q_{i}_8", format="%.2f")
        l20[i] = x.number_input('**Amount < #20 (g):**', value = 370.00, step = step ,key = f"q_{i}_20", format="%.2f")
        l60[i] = x.number_input('**Amount < #60 (g):**', value = 300.00, step = step ,key = f"q_{i}_60", format="%.2f")
        CCE[i] = x.number_input("**TNP/CCE:** ", value = 90.0, step = step ,key = f'cce{i}', format="%.1f")
        wetw[i] = x.number_input("**Wet Weight (g):** ", value = 600.0, step = step ,key = f'wetw{i}', format="%.1f")
        dryw[i] = x.number_input("**Dry weight (g):** ", value = 560.0, step = step ,key = f'dryw{i}', format="%.1f")
        recton[i] = x.number_input("**Recommend Amount (t/a):** ", value = 2.0, step = step ,key = f'recton{i}', format="%.1f")
        lime_cost[i] = x.number_input("**Lime ($/ton)**", value =5.0, step = step ,key = f'lime_p{i}', format="%.1f")
        delivery_cost[i] = x.number_input("**Delivery ($/ton)**", value =5.0, step = step ,key = f'delivery_p{i}', format="%.1f")
        spreading_cost[i] = x.number_input("**Spreading ($/ton)**", value =5.0, step = step ,key = f'spreading_p{i}', format="%.1f")
# # lest add soil data too
#     st.markdown("<h4 style='text-align: center; color: white; background-color: #0033A0;'>Soil Data </h4>", unsafe_allow_html=True)
#     s_container = st.container()
#     c1, c2, c3= s_container.columns(3)
#     wph = c1.slider('**Soil Water pH:**', min_value=4.0, max_value=8.0, value=5.9, step=0.1, key='wph', format="%.1f")
#     bph = c2.slider('**Buffer pH (Sikora-2):**', min_value=4.0, max_value=8.0, value=6.8, step=0.1, key='bph', format="%.1f")
#     tph= c3.slider('**Target pH**', min_value=4.0, max_value=8.0, value=6.4, step=0.1, key='tph', format="%.1f")
#     # soilW = c4.slider('**Soil Weight (g):**',min_value=8.0, max_value=14.0, value=12.0, step=0.1, key='sw', format="%.1f")

    # This datafram is dynamic and therefore making the charts easy to plot
    df = pd.DataFrame({"Quarry": [i for i in quarries.values()],
        "initial": [i  for i in initial.values()], 
        "l8":[i for i in l8.values()],
        "l20": [i for i in l20.values()],
        "l60": [i for i in l60.values()],
        'cce': [i for i in CCE.values()],
        'wetw': [i for i in wetw.values()],
        'dryw': [i for i in dryw.values()],
        'recton': [i for i in recton.values()],
        'price': [i+j+k for i,j,k in zip(lime_cost.values(), delivery_cost.values() ,spreading_cost.values())]
    })
    # adding  columns with new calculations
    df["Zero%_eff"] = ((df.initial-df.l8)/df.initial)*100
    df['twenty%_eff'] = ((((df.l8-df.l20)))/df.initial)*100
    df['fifty%_eff'] = ((df.l20-df.l60)/df.initial)*100
    df['Hund%_eff'] = (df.l60/df.initial)*100
    df['FI'] = (0.2*((df.l8)/df.initial-(df.l20)/df.initial)+0.6*((df.l20)/df.initial-(df.l60)/df.initial)+df.l60/df.initial)*100
    df['%_dry'] = 100-((df.wetw-df.dryw)/df.wetw*100)
    df['%_ENP'] = df.FI/100*df.cce
    df['t_ENP'] = 2000*(df['%_ENP']/100)*(df['%_dry']/100)
    df['Bulk_Rec'] = 2000/df.t_ENP*df.recton
    df['Cost'] = df.Bulk_Rec * df.price
    st.session_state['df_oh'] = df


# Lab results based on percentage
if percent_weight == "Lab Results (Percentage)":
    f_container = st.container()
    samp_cont1, samp_cont2 = f_container.columns([1, 3])
    # samp_cont1.markdown("<h5 style='text-align: center; color: blue;'>" "</h5>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white; background-color: #0033A0;'>Lime Data</h4>", unsafe_allow_html=True)
    samp_cont1.markdown("<h5 style='text-align: center; color: white; background-color: #0033A0;'># Samples</h5>", unsafe_allow_html=True)
    ncol = samp_cont1.number_input("# Sample", 1, 5, 1, key = 'first', label_visibility='collapsed')
    cols = st.columns(ncol)
    step = 1e-1
    for i, x in enumerate(cols):
        st.session_state[f'Sample {i+1}'] = f'Sample {i+1}'
        quarries[i]= x.text_input('**Lime Source:**', placeholder = st.session_state[f'Sample {i+1}'], key = f"q_{i}_name")
        l8[i] = x.number_input('**% < #8 (g)**: ', value = 80.00, step = step ,key = f"q_{i}_8", format="%.2f")
        l20[i] = x.number_input('**% < #20 (g):**', value = 50.00, step = step ,key = f"q_{i}_20", format="%.2f")
        l60[i] = x.number_input('**% < #60 (g):**', value = 40.00, step = step ,key = f"q_{i}_60", format="%.2f")
        CCE[i] = x.number_input("**TNP/CCE:** ", value = 90.0, step = step ,key = f'cce{i}', format="%.1f")
        wetw[i] = x.number_input("**Wet Weight (g):** ", value = 600.0, step = step ,key = f'wetw{i}', format="%.1f")
        dryw[i] = x.number_input("**Dry weight (g):** ", value = 560.0, step = step ,key = f'dryw{i}', format="%.1f")
        recton[i] = x.number_input("**Recommend Amount (t/a):** ", value = 2.0, step = step ,key = f'recton{i}', format="%.1f")
        lime_cost[i] = x.number_input("**Lime ($/ton)**", value =5.0, step = step ,key = f'lime_p{i}', format="%.1f")
        delivery_cost[i] = x.number_input("**Delivery ($/ton)**", value =5.0, step = step ,key = f'delivery_p{i}', format="%.1f")
        spreading_cost[i] = x.number_input("**Spreading ($/ton)**", value =5.0, step = step ,key = f'spreading_p{i}', format="%.1f")
# # lest add soil data too
#     st.markdown("<h4 style='text-align: center; color: white; background-color: #0033A0;'>Soil Data </h4>", unsafe_allow_html=True)
#     s_container = st.container()
#     c1, c2, c3= s_container.columns(3)
#     wph = c1.slider('**Soil Water pH:**', min_value=4.0, max_value=8.0, value=5.9, step=0.1, key='wph', format="%.1f")
#     bph = c2.slider('**Buffer pH (Sikora-2):**', min_value=4.0, max_value=8.0, value=6.8, step=0.1, key='bph', format="%.1f")
#     tph= c3.slider('**Target pH**', min_value=4.0, max_value=8.0, value=6.4, step=0.1, key='tph', format="%.1f")
#     # soilW = c4.slider('**Soil Weight (g):**',min_value=8.0, max_value=14.0, value=12.0, step=0.1, key='sw', format="%.1f")

    # This datafram is dynamic and therefore making the charts easy to plot
    df = pd.DataFrame({"Quarry": [i for i in quarries.values()],
        # "initial": [i  for i in initial.values()], 
        "l8":[i for i in l8.values()],
        "l20": [i for i in l20.values()],
        "l60": [i for i in l60.values()],
        'cce': [i for i in CCE.values()],
        'wetw': [i for i in wetw.values()],
        'dryw': [i for i in dryw.values()],
        'recton': [i for i in recton.values()],
        'price': [i+j+k for i,j,k in zip(lime_cost.values(), delivery_cost.values() ,spreading_cost.values())]
    })
    # adding  columns with new calculations
    df["Zero%_eff"] = (100-df.l8)
    df['twenty%_eff'] = (df.l8-df.l20)
    df['fifty%_eff'] = (df.l20-df.l60)
    df['Hund%_eff'] = (df.l60)
    df['FI'] = (0.2*(df.l8-df.l20)+0.6*(df.l20-df.l60)+df.l60)
    df['%_dry'] = 100-((df.wetw-df.dryw)/df.wetw)
    df['%_ENP'] = df.FI/100*df.cce
    df['t_ENP'] = 2000*(df['%_ENP']/100)*(df['%_dry']/100)
    df['Bulk_Rec'] = 2000/df.t_ENP*df.recton
    df['Cost'] = df.Bulk_Rec * df.price
    st.session_state['df_oh'] = df

st.markdown("___")
@st.cache
def graph_h():
    if df.shape[0]>1:
        eff_h = 8+(df.shape[0]-8)*0.46
        others = 2+(df.shape[0]-2)*0.15
        rotation = 0
        data_labels = 'edge'
        return eff_h, others, rotation, data_labels
    else:
        return 5.7,  1, 0, 'edge'
eff_h, others, rotation, data_labels= graph_h()

# check if pallete is in session_sate.
if "pallete" not in st.session_state:
    pallete = "Dark2"
else:
    pallete = st.session_state['pallete']
tab1, tab2= st.tabs(["**Lime Quality**", "**Lime Amount and Cost**"])


# Draw the graphs
with tab1:
    st.markdown("<h5 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Lime Quality</h5>", unsafe_allow_html=True)
    st.write("___")
    fig,(ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize = (7, eff_h), sharex=True, gridspec_kw={'hspace':0.19})
    Fplot = sns.barplot(x = "Zero%_eff", y = 'Quarry', data=df, ax=ax1, palette=pallete)
    ax1.set_ylabel(None)
    ax1.set_xlabel(None)
    ax1.axes.xaxis.set_visible(False)
    ax1.text(0.45, -0.13, s="#8 Seive", transform = ax1.transAxes)
    ax1.text(0.95, 0.18+eff_h*0.012, "RNV (0%)", rotation =270, transform= ax1.transAxes, fontsize=8)
    ax1.bar_label(Fplot.containers[0], fmt="%.2f", rotation =0)
    ax1.set_title("Lime Fineness (%)", fontsize = 18)

    Splot = sns.barplot(x = "twenty%_eff", y = 'Quarry', data=df, ax=ax2, palette=pallete)
    ax2.set_ylabel(None)
    ax2.set_xlabel(None)
    ax2.axes.xaxis.set_visible(False)
    ax2.text(0.45, -0.13, s="#20 Seive", transform = ax2.transAxes)
    ax2.text(0.95, 0.18+eff_h*0.012, "RNV (20%)", rotation =270, transform= ax2.transAxes, fontsize=8)
    ax2.bar_label(Splot.containers[0], fmt="%.2f", rotation =0)


    Tplot =sns.barplot(x = "fifty%_eff", y = 'Quarry', data=df, ax=ax3, palette=pallete)
    ax3.set_ylabel(None)
    ax3.set_xlabel(None)
    ax3.axes.xaxis.set_visible(False)
    ax3.text(0.45, -0.13, s="#60 Seive", transform = ax3.transAxes)
    ax3.text(0.95, 0.18+eff_h*0.012, "RNV (50%)", rotation =270, transform= ax3.transAxes, fontsize=8)
    ax3.bar_label(Tplot.containers[0], fmt="%.2f", rotation = 0)


    Frplot = sns.barplot(x = 'Hund%_eff', y = 'Quarry', data=df, ax=ax4, palette=pallete)
    ax4.set_xlim((0, 100))
    ax4.set_ylabel(None)
    ax4.set_xlabel(None)
    ax4.text(0.95, 0.08+eff_h*0.011, "RNV (100%)", rotation =270, transform= ax4.transAxes, fontsize=8)
    ax4.bar_label(Frplot.containers[0],fmt="%.2f", rotation = 0)
    ax4.set_xlabel("", fontsize = 14)
    ax4.axes.xaxis.set_visible(False)
    ax4.set_xticklabels([])

    rect = plt.Rectangle(
        # (lower-left corner), width, height
        (0.1232, 0.11), 0.776, 0.77, fill=False, color="k", lw=1, 
        zorder=1000, transform=fig.transFigure, figure=fig
    )
    fig.patches.extend([rect]);

    # FI graph 
    fig1, ax5= plt.subplots(figsize = (7,others))
    ax5.set_ylabel(None)
    ax5.set_title("Fineness Index (FI (%))", fontsize = 18)

    FiPlot = sns.barplot(x='FI', y = 'Quarry', data=df, ax=ax5, palette=pallete)
    ax5.set_xlim((0, 100))
    ax5.bar_label(FiPlot.containers[0], fmt="%.2f", rotation=0)
    ax5.set_ylabel(None)
    ax5.set_xlabel("", fontsize = 14)
    ax5.axes.xaxis.set_visible(False)
    ax5.set_xticklabels([])

    # plot for RNV_______________
    fig2, ax5= plt.subplots(figsize = (7,others))
    ax5.set_xlabel('RNV (%)')
    ax5.set_ylabel(None)
    ax5.set_title("Effective Neutralizaing Power (ENP (%))", fontsize = 18)

    SiPlot = sns.barplot(x='%_ENP', y = 'Quarry', data=df, ax=ax5, palette=pallete)
    ax5.set_xlim((0, 100))
    ax5.bar_label(SiPlot.containers[0], fmt="%.2f", rotation=0)
    ax5.set_ylabel(None)
    ax5.set_xlabel("", fontsize = 14)
    ax5.axes.xaxis.set_visible(False)
    ax5.set_xticklabels([])
    st.pyplot(fig)
    st.pyplot(fig1)
    st.pyplot(fig2)

# Plot for Bulk Recommendation of  Lime
# st.markdown("<h3 style='text-align: center; color: blue;'>" "</h3>", unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: blue;'>" "</h3>", unsafe_allow_html=True)
with tab2:
    st.markdown("<h5 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Lime Recommendation and Application Cost</h5>", unsafe_allow_html=True)
    st.markdown("___")
    # Here I also want to give an option 
    st.markdown("<h3 style='text-align: center; color: blue;'>""</h3>", unsafe_allow_html=True)
    fig2, ax6 = plt.subplots(figsize =(7,others) )
    ax6.set_ylabel(None)
    ax6.set_title(f"Adjusted Lime Recommendation\n ($ton/acre$)", fontsize = 18)

    FiPlot = sns.barplot(x='Bulk_Rec', y = 'Quarry', data=df, ax=ax6, palette=pallete)
    ax6.bar_label(FiPlot.containers[0], fmt="%.2f", rotation = rotation, label_type=data_labels)
    ax6.set_ylabel(None)
    ax6.set_xlim([0, max(df.Bulk_Rec)+max(df.Bulk_Rec)*0.1]) # This syntax max the x axis length dynamic. Without it the data lable makes a problem
    ax6.set_xlabel("", fontsize = 14)
    ax6.axes.xaxis.set_visible(False)
    ax6.set_xticklabels([])
        
        # Plot for Cost of  Lime

    fig3, ax7 = plt.subplots(figsize =(7,others) )
    ax7.set_ylabel(None)
    ax7.set_title(f"Total Cost of Lime Application\n ($\$/acre$)", fontsize = 18)

    SiPlot = sns.barplot(x='Cost', y = 'Quarry', data=df, ax=ax7, palette=pallete)
    ax7.bar_label(SiPlot.containers[0], fmt="%.2f", rotation = rotation, label_type=data_labels)
    ax7.set_ylabel(None)
    ax7.set_xlabel(None)
    ax7.set_xlim([0, max(df.Cost)+max(df.Cost)*0.1])
    ax7.axes.xaxis.set_visible(False)
    ax7.set_xticklabels([])
    st.pyplot(fig2)
    st.pyplot(fig3)
# with tab3:
#     st.markdown("<h5 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Calculated data</h5>", unsafe_allow_html=True)
#     st.markdown("___")
#     df = st.session_state['df_oh']
#     AgGrid(round(df.loc[:,['Quarry','FI', "%_ENP", "t_ENP", "Bulk_Rec", "Cost"]], 2),  columns_auto_size_mode='FIT_ALL_COLUMNS_TO_VIEW', theme='alpine')
