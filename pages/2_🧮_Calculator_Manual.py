import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# Add a tile to the sources of the lime
st.markdown("<h2 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Lime and Soil Data</h2>", unsafe_allow_html=True)



# Lets make some empty dictionary to save data
# This is used to loop through the data in dynamic columns. You can use pandas dataframe directly too. 

quarries = {}
initial ={}
gten  = {}
lfifty = {}
CCE = {}
Price ={}


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

st.markdown("<h5 style='text-align: center; color: blue;'>" "</h5>", unsafe_allow_html=True)

# Lets loop through the columns
if percent_weight =="Lab Results (Weight)":
    f_container = st.container() # the reason for using container is to give a nice looking style to the title of samples
    samp_cont1, samp_cont2 = f_container.columns([1, 3])
    samp_cont1.markdown("<h5 style='text-align: center; color: blue;'>" "</h5>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white; background-color: #0033A0;'>Lime Data</h4>", unsafe_allow_html=True)
    samp_cont1.markdown("<h5 style='text-align: center; color: white; background-color: #0033A0;'># Samples</h5>", unsafe_allow_html=True)
    ncol = samp_cont1.number_input("# Sample", 1, 5, 2, label_visibility='collapsed')
    cols = st.columns(ncol)
    for i, x in enumerate(cols):
        quarries[i]= x.text_input('**Lime Source:**', value = f'Sample {i+1}',key = f"q_{i}_name")
        initial[i] = x.number_input('**Initial Amount (g)**: ', value = 100.00, key = f"q_{i}_initial", format="%.2f")
        gten[i] = x.number_input('**Amount > #10 (g)**: ', value = 10.00, key = f"q_{i}_10", format="%.2f")
        lfifty[i] = x.number_input('**Amount < #50 (g):**', value = 60.00, key = f"q_{i}_50", format="%.2f")
        CCE[i] = x.number_input("**Culcium Carbonate Equivalent (CCE):** ", value = 90.0, key = f'cce{i}', format="%.1f")
        Price[i] = x.number_input("**Price ($/ton)**", value = 20.0, key = f'price{i}', format="%.1f")
# lest add soil data too
    st.markdown("<h4 style='text-align: center; color: white; background-color: #0033A0;'>Soil Data </h4>", unsafe_allow_html=True)
    s_container = st.container()
    c1, c2, c3= s_container.columns(3)
    wph = c1.slider('**Soil Water pH:**', min_value=4.0, max_value=8.0, value=5.8, step=0.1, key='wph', format="%.1f")
    bph = c2.slider('**Buffer pH (Sikora-2):**', min_value=4.0, max_value=8.0, value=6.5, step=0.1, key='bph', format="%.1f")
    tph= c3.slider('**Target pH**', min_value=4.0, max_value=8.0, value=6.5, step=0.1, key='tph', format="%.1f")
    # soilW = c4.slider('**Soil Weight (g):**',min_value=8.0, max_value=14.0, value=12.0, step=0.1, key='sw', format="%.1f")

    # This datafram is dynamic and therefore making the charts easy to plot
    df = pd.DataFrame({"Quarry": [i for i in quarries.values()],
        "initial": [i  for i in initial.values()], 
        "gten":[i for i in gten.values()],
        "lten": [i-j for i, j in zip(initial.values(), gten.values())],
        "lfifty": [i for i in lfifty.values()],
        'cce': [i for i in CCE.values()],
        'price': [i for i in Price.values()]
    })
    # adding  columns with new calculations
    df["Zero%_eff"] = (df.gten/df.initial)*100
    df['Fifty%_eff'] = ((((df.lten-df.lfifty)))/df.initial)*100
    df['Hund%_eff'] = (df.lfifty/df.initial)*100
    df["RNV"] = df.cce/100.00*((((df.lten-df.lfifty)/2.0)+df.lfifty)/df.initial)*100

    #Calculating Recommend lime amount and cost
    SWPH = wph
    BPH = bph
    TPH = tph
    SW  = 12
    RNV = df.RNV
    part1 = -1.1 *(TPH-SWPH)*(BPH-7.55)
    part2  = (BPH -(1.1*SWPH)+1.47)
    part3 = 13.75/SW
    ELR = part1/part2*part3
    cffa = [(3.62 - (0.734*ELR)) if ELR <=3 else 1.42][0]
    pure_lime = cffa*ELR 
    df['Bulk_Rec'] = pure_lime/df.RNV*100 if TPH>SWPH else df.RNV *0
    df['Cost'] = df.Bulk_Rec * df.price
    st.session_state['df'] = df


# Lab results based on percentage
if percent_weight == "Lab Results (Percentage)":
    f_container = st.container()
    samp_cont1, samp_cont2 = f_container.columns([1, 3])
    samp_cont1.markdown("<h5 style='text-align: center; color: blue;'>" "</h5>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: white; background-color: #0033A0;'>Lime Data</h4>", unsafe_allow_html=True)
    samp_cont1.markdown("<h5 style='text-align: center; color: white; background-color: #0033A0;'># Samples</h5>", unsafe_allow_html=True)
    ncol = samp_cont1.number_input("# Sample", 1, 5, 2, key = 'first', label_visibility='collapsed')
    cols = st.columns(ncol)
    for i, x in enumerate(cols):
        quarries[i]= x.text_input('**Lime Source:**', value = f'Sample {i+1}', key = f"q_{i}_name")
        gten[i] = x.number_input('**% > #10:**', value = 10.00, key = f"q_{i}_10", format="%.2f")
        lfifty[i] = x.number_input('**% < #50:**', value = 60.00, key = f"q_{i}_50", format="%.2f")
        CCE[i] = x.number_input("**Culcium Carbonate Equivalent (CCE):**", value = 90.0, key = f'cce{i}', format="%.1f")
        Price[i] = x.number_input("**Price ($/ton):**", value = 20.0, key = f'price{i}', format="%.1f")

    st.markdown("<h4 style='text-align: center; color: white; background-color: #0033A0;'>Soil Data </h4>", unsafe_allow_html=True)
    s_container = st.container()
    c1, c2, c3= s_container.columns(3)
    wph = c1.slider('**Soil Water pH:**', min_value=4.0, max_value=8.0, value=5.8, step=0.1, key='wph', format="%.1f")
    bph = c2.slider('**Buffer pH (Sikora-2):**', min_value=4.0, max_value=8.0, value=6.5, step=0.1, key='bph', format="%.1f")
    tph= c3.slider('**Target pH**', min_value=4.0, max_value=8.0, value=6.5, step=0.1, key='tph', format="%.1f")
    # soilW = c4.slider('**Soil Weight (g):**',min_value=8.0, max_value=14.0, value=12.0, step=0.1, key='sw', format="%.1f")

    # This datafram is dynamic and therefore making the charts easy to plot
    df = pd.DataFrame({"Quarry": [i for i in quarries.values()],
        "gten":[i for i in gten.values()],
        "lten": [i-j for i, j in zip([100 for i in gten.values()], gten.values())],
        "lfifty": [i for i in lfifty.values()],
        'cce': [i for i in CCE.values()],
        'price': [i for i in Price.values()]
    })

    # adding  columns with new calculations
    df["Zero%_eff"] = df.gten
    df['Fifty%_eff'] = (df.lten-df.lfifty)
    df['Hund%_eff'] = df.lfifty
    df["RNV"] = df.cce/100.00*(((df.lten-df.lfifty)/2.0)+df.lfifty)
    SWPH =wph
    BPH = bph
    TPH = tph
    SW  = 12
    RNV = df.RNV
    part1 = -1.1 *(TPH-SWPH)*(BPH-7.55)
    part2  = (BPH -(1.1*SWPH)+1.47)
    part3 = 13.75/SW
    ELR = part1/part2*part3 #Equation LR
    cffa = [(3.62 - (0.734*ELR)) if ELR <=3 else 1.42][0]
    pure_lime = cffa*ELR 

    # if TPH> SWPH:
    #     if 3<(-1.1*(TPH-SWPH)*(BPH-7.55)/(BPH-(1.1*SWPH)+1.47)*13.75/SW):
    #         df['Bulk_Rec'] = 1.42*(-1.1*(TPH-SWPH)*(BPH-7.55)/(BPH-(1.1*SWPH)+1.47)*13.75/SW)/RNV
    #     else:
    #         df['Bulk_Rec'] = (3.62-(0.734*(-1.1*(TPH-SWPH)*(BPH-7.55)/(BPH-(1.1*SWPH)+1.47)*13.75/SW)))*(-1.1*(TPH-SWPH)*(BPH-7.55)/(BPH-(1.1*SWPH)+1.47)*13.75/SW)/(RNV/100)
    # else:
    #     df['Bulk_Rec'] = 0
    df['Bulk_Rec'] = pure_lime/df.RNV*100 if TPH > SWPH else df.RNV * 0
    df['Cost'] = df.Bulk_Rec * df.price
    st.session_state['df'] = df # this is used in downnloads
@st.cache
def graph_h():
    if df.shape[0]>5:
        eff_h = 5+(df.shape[0]-5)*0.45
        others = 2+(df.shape[0]-2)*0.15
        rotation = 0
        data_labels = 'edge'
        return eff_h, others, rotation, data_labels
    else:
        return 5,  2, 0, 'edge'
eff_h, others, rotation, data_labels= graph_h()

# check if pallete is in session_sate.
if "pallete" not in st.session_state:
    pallete = "Dark2"
else:
    pallete = st.session_state['pallete']

# Draw the graphs
fig,(ax1, ax2, ax3) = plt.subplots(3, 1, figsize = (7, eff_h), sharex=True, gridspec_kw={'hspace':0.15})
Fplot = sns.barplot(x = "Zero%_eff", y = 'Quarry', data=df, ax=ax1, palette=pallete)
ax1.set_ylabel(None)
ax1.set_xlabel(None)
ax1.axes.xaxis.set_visible(False)
ax1.text(0.45, -0.11, s="#10 Seive", transform = ax1.transAxes)
ax1.text(0.95, 0.18+eff_h*0.012, "RNV (0%)", rotation =270, transform= ax1.transAxes)
ax1.bar_label(Fplot.containers[0], fmt="%.2f", rotation =0)
ax1.set_title("Lime Fineness (%)", fontsize = 18)


Splot =sns.barplot(x = "Fifty%_eff", y = 'Quarry', data=df, ax=ax2, palette=pallete)
ax2.set_ylabel(None)
ax2.set_xlabel(None)
ax2.axes.xaxis.set_visible(False)
ax2.text(0.45, -0.11, s="#50 Seive", transform = ax2.transAxes)
ax2.text(0.95, 0.18+eff_h*0.012, "RNV (50%)", rotation =270, transform= ax2.transAxes)
ax2.bar_label(Splot.containers[0], fmt="%.2f", rotation = 0)


Tplot = sns.barplot(x = "Hund%_eff", y = 'Quarry', data=df, ax=ax3, palette=pallete)
ax3.set_xlim((0, 100))
ax3.set_ylabel(None)
ax3.set_xlabel(None)
ax3.text(0.95, 0.18+eff_h*0.012, "RNV (100%)", rotation =270, transform= ax3.transAxes)
ax3.bar_label(Tplot.containers[0],fmt="%.2f", rotation = 0)
ax3.set_xlabel("", fontsize = 14)
ax3.axes.xaxis.set_visible(False)
ax3.set_xticklabels([])

rect = plt.Rectangle(
    # (lower-left corner), width, height
    (0.1232, 0.11), 0.776, 0.77, fill=False, color="k", lw=1, 
    zorder=1000, transform=fig.transFigure, figure=fig
)
fig.patches.extend([rect]);

# plot for RNV_______________

fig1, ax4= plt.subplots(figsize = (7,others))
ax4.set_xlabel('RNV (%)')
ax4.set_ylabel(None)
ax4.set_title("Relative Neutralizaing Value (RNV (%))", fontsize = 18)

FrPlot = sns.barplot(x='RNV', y = 'Quarry', data=df, ax=ax4, palette=pallete)
ax4.set_xlim((0, 100))
ax4.bar_label(FrPlot.containers[0], fmt="%.2f", rotation=0)
ax4.set_ylabel(None)
ax4.set_xlabel("", fontsize = 14)
ax4.axes.xaxis.set_visible(False)
ax4.set_xticklabels([])
st.pyplot(fig)
st.pyplot(fig1)


# Plot for Bulk Recommendation of  Lime
st.markdown("<h3 style='text-align: center; color: blue;'>" "</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: blue;'>" "</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: blue;'>" "</h3>", unsafe_allow_html=True)

st.markdown("<h5 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Lime Recommendation and Application Cost</h5>", unsafe_allow_html=True)

# Here I also want to give an option 
st.markdown("<h3 style='text-align: center; color: blue;'>""</h3>", unsafe_allow_html=True)
fig2, ax5 = plt.subplots(figsize =(7,others) )
ax5.set_ylabel(None)
ax5.set_title(f"Adjusted Lime Recommendation ($Tons\ Acre^{-1}$)\nto raise soil water pH of {round(SWPH, 1)} to a target pH of {round(TPH,1)}", fontsize = 14)

FiPlot = sns.barplot(x='Bulk_Rec', y = 'Quarry', data=df, ax=ax5, palette=pallete)
ax5.bar_label(FiPlot.containers[0], fmt="%.2f", rotation = rotation, label_type=data_labels)
ax5.set_ylabel(None)
ax5.set_xlim([0, max(df.Bulk_Rec)+max(df.Bulk_Rec)*0.1]) # This syntax max the x axis length dynamic. Without it the data lable makes a problem
ax5.set_xlabel("", fontsize = 14)
ax5.axes.xaxis.set_visible(False)
ax5.set_xticklabels([])
    
    # Plot for Cost of  Lime

fig3, ax6 = plt.subplots(figsize =(7,others) )
ax6.set_ylabel(None)
ax6.set_title(f"Total Cost of Lime Application ($\$\ Acre^{-1}$)\nto raise soil water pH of {round(SWPH, 1)} to a target pH of {round(TPH,1)}", fontsize = 14)

SiPlot = sns.barplot(x='Cost', y = 'Quarry', data=df, ax=ax6, palette=pallete)
ax6.bar_label(SiPlot.containers[0], fmt="%.2f", rotation = rotation, label_type=data_labels)
ax6.set_ylabel(None)
ax6.set_xlabel(None)
ax6.set_xlim([0, max(df.Cost)+max(df.Cost)*0.1])
ax6.axes.xaxis.set_visible(False)
ax6.set_xticklabels([])
st.pyplot(fig2)
st.pyplot(fig3)
