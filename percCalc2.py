import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

APP_TITLE = "CHE Improvement Calculator for 5~9"
APP_SUBTITLE = "This tool shows the graph of the data and the amount of improvement needed in percentage."

LABELS = ["Screentime", "Exercise Time", "Sleeptime"]

FIXED_VALUES = [2, 2, 11]

TEXT_1_LOW = "You are using less than the screentime limitations. Keep it up!"
TEXT_2_HIGH = "You are exercising more than the minimum. Keep it up!"
TEXT_3_HIGH = "You are sleeping more than the minimum. Keep it up!"

st.set_page_config(page_title=APP_TITLE, layout="wide")

st.title(APP_TITLE)
st.markdown(APP_SUBTITLE)
st.divider()

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Input sleeptime, ")
    user_inputs = []
    for i, label in enumerate(LABELS):
        val = st.number_input(f"{label} input current time", min_value=0.0, value=0.0, step=1.0, key=f"input_{i}")
        user_inputs.append(val)

with col2:
    st.subheader("Comparison Graph")
    x = np.arange(len(LABELS))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7, 4.5))
    rects1 = ax.bar(x - width/2, FIXED_VALUES, width, label='Needed time', color='#FF6B2B')
    rects2 = ax.bar(x + width/2, user_inputs, width, label='Current time', color='#707B8C')

    ax.set_ylabel('Values')
    ax.set_xticks(x)
    ax.set_xticklabels(LABELS)
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    plt.tight_layout()
    st.pyplot(fig)

st.divider()

st.subheader("Percentage difference")

res_cols = st.columns(len(LABELS))

for i in range(len(LABELS)):
    with res_cols[i]:
        st.info(f"**{LABELS[i]}**")
        fixed = FIXED_VALUES[i]
        user = user_inputs[i]
        
        if fixed != 0:
            raw_diff_pct = ((user - fixed) / fixed) * 100
        else:
            raw_diff_pct = 0
        
        if i == 0:
            if user < fixed:
                st.success("Screenime decrease needed: **0%**")
                st.caption(TEXT_1_LOW)
            else:
                if fixed == 0 and user > 0:
                    st.warning("Screenime decrease needed: **100%**")
                    st.caption(f"You are over screentime limitations.")
                else:
                    st.warning(f"Screenime decrease needed: **{raw_diff_pct:.1f}%**")
                    st.caption(f"You are {raw_diff_pct:.1f}% over screentime limitations.")
                
        elif i == 1:
            if user > fixed:
                st.success("Exercise time increase needed: **0%**")
                st.caption(TEXT_2_HIGH)  
            else:
                lack_pct = -raw_diff_pct
                st.warning(f"Exercise time increase needed: **{lack_pct:.1f}%**")
                st.caption(f"You are {lack_pct:.1f}% under minimum exercise time.")
                
        elif i == 2:
            if user > fixed:
                st.success("Sleeptime encrease needed: **0%**")
                st.caption(TEXT_3_HIGH)  
            else:
                lack_pct = -raw_diff_pct
                st.warning(f"Sleeptime increase needed: **{lack_pct:.1f}%**")
                st.caption(f"You are {lack_pct:.1f}% away from minimum sleeptime.")
