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

quarries = {}
initial ={}
l8  = {}
l30 = {}
l60 = {}
#wetw = {}
#dryw = {}
recton = {}
lime_cost = {}
delivery_cost = {}
spreading_cost ={}
CCE = {}


# Add a tile to the sources of the lime
st.markdown("<h2 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Lime and Soil Data</h2>", unsafe_allow_html=True)
percent_weight = option_menu(None, ["Manual Analysis", "Reported Analysis"], 
    icons=[], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffe6e6"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#ff0000"},
    }
)

if percent_weight == "Manual Analysis":
    f_container = st.container()
    samp_cont1, samp_cont2 = f_container.columns([1, 3])
    samp_cont1.markdown("<h5 style='text-align: center; color: white; background-color: #0033A0;'># Samples</h5>", unsafe_allow_html=True)
    ncol = samp_cont1.number_input("# Sample", 1, 5, 1, label_visibility='collapsed')
    cols = st.columns(ncol)
    step = 1e-1
    for i, x in enumerate(cols):
        st.session_state[f'Sample {i+1}'] = f'Sample {i+1}'
        quarries[i]= x.text_input('**Lime Source:**', placeholder = st.session_state[f'Sample {i+1}'], key = f"q_{i}_name")
        #initial[i] = x.number_input('**Initial Amount (g)**: ', value = 550.00, step = step ,key = f"q_{i}_initial", format="%.2f")
        l8[i] = x.number_input('**% < #8 (g)**: ', value = 85.00, step = step ,key = f"q_{i}_8", format="%.2f")
        l30[i] = x.number_input('**% < #30 (g):**', value = 35.00, step = step ,key = f"q_{i}_20", format="%.2f")
        l60[i] = x.number_input('**% < #60 (g):**', value = 22.00, step = step ,key = f"q_{i}_60", format="%.2f")
        #CCE[i] = x.number_input("**OYAR (t/a):** ", value = 1.5, step = step ,key = f'cce{i}', format="%.1f")
        #wetw[i] = x.number_input("**Wet Weight (g):** ", value = 600.0, step = step ,key = f'wetw{i}', format="%.1f")
        CCE[i] = x.number_input("**CCE (%):** ", value = 90.0, step = step ,key = f'CCE{i}', format="%.1f")
        recton[i] = x.number_input("**Recommend Amount (t/a):** ", value = 2.0, step = step ,key = f'recton{i}', format="%.1f")
        lime_cost[i] = x.number_input("**Lime ($/ton)**", value =5.0, step = step ,key = f'lime_p{i}', format="%.1f")
        delivery_cost[i] = x.number_input("**Delivery ($/ton)**", value =5.0, step = step ,key = f'delivery_p{i}', format="%.1f")
        spreading_cost[i] = x.number_input("**Spreading ($/ton)**", value =5.0, step = step ,key = f'spreading_p{i}', format="%.1f")
    p = 0.01
    df = pd.DataFrame({"Quarry": [i for i in quarries.values()],
        "L8": [100 - i for i in l8.values()],
        "ll8": [i for i in l8.values()],
        "l8":[i-j for i, j in zip(l8.values(), l30.values())],
        "l30": [i-j for i,j in zip(l30.values(), l60.values())],
        "l60": [i for i in l60.values()],
        'cce': [i/100 for i in CCE.values()],
        #'wetw': [i for i in wetw.values()],
        #'dryw': [i for i in dryw.values()],
        'recton': [i for i in recton.values()],
        'price': [i+j+k for i,j,k in zip(lime_cost.values(), delivery_cost.values() ,spreading_cost.values())]
    })
    df['TFEV'] = (1-df.ll8*p)*5 + (df.l8*p)*20 + (df.l30*p)*50+ df.l60*p*100
    df['ENV'] = df.TFEV*df.cce
    df['OYAR'] = 46.35/df.ENV
    df['Bulk_Rec'] = df.OYAR*df.recton
    df['Cost'] = df.Bulk_Rec * df.price
    st.session_state['df_IL'] = df
    #st.write(df)

    dfn = df.copy()
    st.markdown("___")
    @st.cache
    def graph_h():
        if dfn.shape[0]>1:
            eff_h = 8+(dfn.shape[0]-8)*0.46
            others = 2+(dfn.shape[0]-2)*0.15
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
    tab1, tab2, tab3 = st.tabs(["**Lime Quality**", "**Lime Amount and Cost**", "Note"])


    # Draw the graphs
    with tab1:
        st.markdown("<h5 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Lime Quality</h5>", unsafe_allow_html=True)
        st.write("___")
        fig,(ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize = (7, eff_h), sharex=True, gridspec_kw={'hspace':0.19})
        Fplot = sns.barplot(x = "L8", y = 'Quarry', data=dfn, ax=ax1, palette=pallete)
        ax1.set_ylabel(None)
        ax1.set_xlabel(None)
        ax1.set_xlim([0, 100])
        ax1.axes.xaxis.set_visible(False)
        ax1.text(0.45, -0.13, s="#8 Seive", transform = ax1.transAxes)
        ax1.text(0.95, 0.18+eff_h*0.012, "RNV (0%)", rotation =270, transform= ax1.transAxes, fontsize=9)
        ax1.bar_label(Fplot.containers[0], fmt="%.2f", rotation =0)
        ax1.set_title("Lime Fineness (%)", fontsize = 18)

        Splot = sns.barplot(x = "l8", y = 'Quarry', data=dfn, ax=ax2, palette=pallete)
        ax2.set_ylabel(None)
        ax2.set_xlabel(None)
        ax2.set_xlim([0, 100])
        ax2.axes.xaxis.set_visible(False)
        ax2.text(0.45, -0.13, s="#30 Seive", transform = ax2.transAxes)
        ax2.text(0.95, 0.18+eff_h*0.012, "RNV (30%)", rotation =270, transform= ax2.transAxes, fontsize=9)
        ax2.bar_label(Splot.containers[0], fmt="%.2f", rotation =0)


        Tplot =sns.barplot(x = "l30", y = 'Quarry', data=dfn, ax=ax3, palette=pallete)
        ax3.set_ylabel(None)
        ax3.set_xlabel(None)
        ax3.set_xlim([0, 100])
        ax3.axes.xaxis.set_visible(False)
        ax3.text(0.45, -0.13, s="#60 Seive", transform = ax3.transAxes)
        ax3.text(0.95, 0.18+eff_h*0.012, "RNV (60%)", rotation =270, transform= ax3.transAxes, fontsize=9)
        ax3.bar_label(Tplot.containers[0], fmt="%.2f", rotation = 0)


        Frplot = sns.barplot(x = 'l60', y = 'Quarry', data=dfn, ax=ax4, palette=pallete)
        ax4.set_xlim((0, max(df['l60'])+max(dfn['l60']*0.1)))
        ax4.set_ylabel(None)
        ax4.set_xlabel(None)
        ax4.set_xlim([0, 100])
        ax4.text(0.95, 0.08+eff_h*0.011, "RNV (100%)", rotation =270, transform= ax4.transAxes, fontsize=9)
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

        FiPlot = sns.barplot(x='TFEV', y = 'Quarry', data=dfn, ax=ax5, palette=pallete)
        ax5.set_xlim((0, max(dfn['TFEV'])+max(dfn['TFEV']*0.1)))
        ax5.bar_label(FiPlot.containers[0], fmt="%.2f", rotation=0)
        ax5.set_ylabel(None)
        ax5.set_xlabel("", fontsize = 14)
        ax5.axes.xaxis.set_visible(False)
        ax5.set_xticklabels([])

        # plot for RNV_______________
        fig2, ax5= plt.subplots(figsize = (7,others))
        ax5.set_xlabel('RNV (%)')
        ax5.set_ylabel(None)
        ax5.set_title("Relative Neutralizaing Value (RNV (%))", fontsize = 18)

        SiPlot = sns.barplot(x='ENV', y = 'Quarry', data=dfn, ax=ax5, palette=pallete)
        ax5.set_xlim((0, max(dfn.ENV)+max(dfn.ENV)*0.1))
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

        FiPlot = sns.barplot(x='Bulk_Rec', y = 'Quarry', data=dfn, ax=ax6, palette=pallete)
        ax6.bar_label(FiPlot.containers[0], fmt="%.2f", rotation = rotation, label_type=data_labels)
        ax6.set_ylabel(None)
        ax6.set_xlim([0, max(dfn['Bulk_Rec'])+max(dfn['Bulk_Rec'])*0.1]) # This syntax max the x axis length dynamic. Without it the data lable makes a problem
        ax6.set_xlabel("", fontsize = 14)
        ax6.axes.xaxis.set_visible(False)
        ax6.set_xticklabels([])
            
            # Plot for Cost of  Lime

        fig3, ax7 = plt.subplots(figsize =(7,others) )
        ax7.set_ylabel(None)
        ax7.set_title(f"Total Cost of Lime Application\n ($\$/acre$)", fontsize = 18)

        SiPlot = sns.barplot(x='Cost', y = 'Quarry', data=dfn, ax=ax7, palette=pallete)
        ax7.bar_label(SiPlot.containers[0], fmt="%.2f", rotation = rotation, label_type=data_labels)
        ax7.set_ylabel(None)
        ax7.set_xlabel(None)
        ax7.set_xlim([0, max(dfn.Cost)+max(dfn.Cost)*0.1])
        ax7.axes.xaxis.set_visible(False)
        ax7.set_xticklabels([])
        st.pyplot(fig2)
        st.pyplot(fig3)
    with tab3:
        st.markdown("""
        <div style = "text-align:justify;">
        The results of this analysis are based on Illinois Voluntary Limestone Program PRODUCER INFORMATION (2021 Edition). You can read more about it 
        <a href ="https://www2.illinois.gov/sites/agr/About/Documents/Limestone/2021LimestoneBook.pdf">here</a>.
        </div>
        """, unsafe_allow_html = True)




if percent_weight == "Reported Analysis":

    col1, _,_=st.columns(3)
    col1.markdown("<h5 style='background-color: white; font-size:35px; text-align: center; color: 	white;'>""</h5>", unsafe_allow_html=True)

    col1.markdown("<h4 style='background-color: #0033A0; font-size:25px; text-align: left; color:white;'>Select Lime Sources</h4>", unsafe_allow_html=True)
    @st.cache
    def read_Data():
        df = pd.read_csv("IL_Lime_Data.csv")
        df.set_index('Quarry2', inplace=True)
        return df
    df = read_Data()

    mcb  = st.multiselect("Select the lime sources: ",df.index.unique(), default= 'Alliance Materials Siers' ,key='select_box', label_visibility='collapsed')

    dfn = df.loc[[i for i in mcb], :]

    st.markdown("___")
    @st.cache
    def graph_h():
        if dfn.shape[0]>1:
            eff_h = 8+(dfn.shape[0]-8)*0.46
            others = 2+(dfn.shape[0]-2)*0.15
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
    tab1, tab2, tab3 = st.tabs(["**Lime Quality**", "**Lime Amount and Cost**", "Note"])


    # Draw the graphs
    with tab1:
        st.markdown("<h5 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Lime Quality</h5>", unsafe_allow_html=True)
        st.write("___")
        fig,(ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize = (7, eff_h), sharex=True, gridspec_kw={'hspace':0.19})
        Fplot = sns.barplot(x = "> #8", y = 'Quarry', data=dfn, ax=ax1, palette=pallete)
        ax1.set_ylabel(None)
        ax1.set_xlabel(None)
        ax1.axes.xaxis.set_visible(False)
        ax1.text(0.45, -0.13, s="#8 Seive", transform = ax1.transAxes)
        ax1.text(0.95, 0.18+eff_h*0.012, "RNV (0%)", rotation =270, transform= ax1.transAxes, fontsize=9)
        ax1.bar_label(Fplot.containers[0], fmt="%.2f", rotation =0)
        ax1.set_title("Lime Fineness (%)", fontsize = 18)

        Splot = sns.barplot(x = "#8 >lime< #30", y = 'Quarry', data=dfn, ax=ax2, palette=pallete)
        ax2.set_ylabel(None)
        ax2.set_xlabel(None)
        ax2.axes.xaxis.set_visible(False)
        ax2.text(0.45, -0.13, s="#30 Seive", transform = ax2.transAxes)
        ax2.text(0.95, 0.18+eff_h*0.012, "RNV (30%)", rotation =270, transform= ax2.transAxes, fontsize=9)
        ax2.bar_label(Splot.containers[0], fmt="%.2f", rotation =0)


        Tplot =sns.barplot(x = "#30> lime < #60", y = 'Quarry', data=dfn, ax=ax3, palette=pallete)
        ax3.set_ylabel(None)
        ax3.set_xlabel(None)
        ax3.axes.xaxis.set_visible(False)
        ax3.text(0.45, -0.13, s="#60 Seive", transform = ax3.transAxes)
        ax3.text(0.95, 0.18+eff_h*0.012, "RNV (60%)", rotation =270, transform= ax3.transAxes, fontsize=9)
        ax3.bar_label(Tplot.containers[0], fmt="%.2f", rotation = 0)


        Frplot = sns.barplot(x = '<#60', y = 'Quarry', data=dfn, ax=ax4, palette=pallete)
        ax4.set_xlim((0, max(df['<#60'])+max(dfn['<#60']*0.1)))
        ax4.set_ylabel(None)
        ax4.set_xlabel(None)
        ax4.text(0.95, 0.08+eff_h*0.011, "RNV (100%)", rotation =270, transform= ax4.transAxes, fontsize=9)
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

        FiPlot = sns.barplot(x='Total Finess Eff. Value', y = 'Quarry', data=dfn, ax=ax5, palette=pallete)
        ax5.set_xlim((0, max(dfn['Total Finess Eff. Value'])+max(dfn['Total Finess Eff. Value']*0.1)))
        ax5.bar_label(FiPlot.containers[0], fmt="%.2f", rotation=0)
        ax5.set_ylabel(None)
        ax5.set_xlabel("", fontsize = 14)
        ax5.axes.xaxis.set_visible(False)
        ax5.set_xticklabels([])

        # plot for RNV_______________
        fig2, ax5= plt.subplots(figsize = (7,others))
        ax5.set_xlabel('RNV (%)')
        ax5.set_ylabel(None)
        ax5.set_title("Relative Neutralizaing Value (RNV (%))", fontsize = 18)

        SiPlot = sns.barplot(x='RNV', y = 'Quarry', data=dfn, ax=ax5, palette=pallete)
        ax5.set_xlim((0, max(dfn.RNV)+max(dfn.RNV)*0.1))
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

        FiPlot = sns.barplot(x='Recommend Amount', y = 'Quarry', data=dfn, ax=ax6, palette=pallete)
        ax6.bar_label(FiPlot.containers[0], fmt="%.2f", rotation = rotation, label_type=data_labels)
        ax6.set_ylabel(None)
        ax6.set_xlim([0, max(dfn['Recommend Amount'])+max(dfn['Recommend Amount'])*0.1]) # This syntax max the x axis length dynamic. Without it the data lable makes a problem
        ax6.set_xlabel("", fontsize = 14)
        ax6.axes.xaxis.set_visible(False)
        ax6.set_xticklabels([])
            
            # Plot for Cost of  Lime

        fig3, ax7 = plt.subplots(figsize =(7,others) )
        ax7.set_ylabel(None)
        ax7.set_title(f"Total Cost of Lime Application\n ($\$/acre$)", fontsize = 18)

        SiPlot = sns.barplot(x='Cost', y = 'Quarry', data=dfn, ax=ax7, palette=pallete)
        ax7.bar_label(SiPlot.containers[0], fmt="%.2f", rotation = rotation, label_type=data_labels)
        ax7.set_ylabel(None)
        ax7.set_xlabel(None)
        ax7.set_xlim([0, max(dfn.Cost)+max(dfn.Cost)*0.1])
        ax7.axes.xaxis.set_visible(False)
        ax7.set_xticklabels([])
        st.pyplot(fig2)
        st.pyplot(fig3)
    with tab3:
        st.markdown("""
        <div style = "text-align:justify;">
        The results of this analysis are based on Illinois Voluntary Limestone Program PRODUCER INFORMATION (2021 Edition). You can read more about it 
        <a href ="https://www2.illinois.gov/sites/agr/About/Documents/Limestone/2021LimestoneBook.pdf">here</a>.
        </div>
        """, unsafe_allow_html = True)
