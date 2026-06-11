import streamlit as st
import plotly.graph_objects as go                                            #plotly.graph_objects是plotly库下的具体的模块，不是函数，下面要写的并且带有（）的才是函数
import numpy as np

st.set_page_config(page_title="医学生职业心理韧性测评", layout="centered",)           #config配置；   page_title是标签页显示的字；  layout整体布局的wide宽布局，centered窄布局
st.title("🩺 医学生职业心理韧性测评")                                                #title最大，header大，subheader中，caption小
st.markdown("**遵义医科大学 · 心理健康测评系统**")
st.markdown("---")

cdrisc_questions = [
    "我能适应变化",
    "我有亲密的朋友关系",
    "有时候命运能帮忙",
    "我有自己的目标",
    "经历困难后我会更强",
    "我能看到事情幽默的一面",
    "面对困难我会尽力解决",
    "我能应对大多数情况",
    "遇到困难我不会放弃",
    "我能达到自己的目标",
]

career_questions = [
    "面对繁重的医学课程，我能保持积极心态",
    "遇到医患矛盾时，我能理性处理",
    "实习中遇到挫折，我不会轻易放弃学医",
    "我相信自己能成为一名好医生",
    "面对医学考试压力，我能有效应对",
]

all_questions = cdrisc_questions + career_questions
options = ["从不", "偶尔", "经常", "总是"]
scores_map = {"从不": 0, "偶尔": 1, "经常": 2, "总是": 3}

if "answers" not in st.session_state:
    st.session_state.answers = ["从不"] * 15

if "submitted" not in st.session_state:
    st.session_state.submitted = False

def calc_score(answers):
    total = sum(scores_map[a] for a in answers)
    cdrisc = sum(scores_map[a] for a in answers[:10])
    career = sum(scores_map[a] for a in answers[10:])
    return total, cdrisc, career

def get_level(total):
    if total >= 35:
        return "🟢 韧性极强", "你的心理韧性非常优秀，能很好地应对医学道路上的各种挑战。"
    elif total >= 25:
        return "🔵 韧性良好", "你有较好的心理韧性，大多数压力都能应对。"
    elif total >= 15:
        return "🟡 韧性一般", "你的韧性中等，部分压力下可能会感到吃力，建议多关注自我调节。"
    else:
        return "🔴 韧性偏弱", "你目前承受压力的能力较弱，建议主动寻求心理支持。"

if not st.session_state.submitted:
    st.subheader("请根据你的真实感受选择（共15题）")

    for i, q in enumerate(all_questions):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{i+1}. {q}**")
        with col2:
            st.session_state.answers[i] = st.radio("", options, key=f"q{i}", index=0, label_visibility="collapsed")

    if st.button("提交测评", type="primary"):
        st.session_state.submitted = True
        st.experimental_rerun()
else:
    total, cdrisc, career = calc_score(st.session_state.answers)
    level, suggestion = get_level(total)

    st.markdown("## 📊 测评结果")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.metric("总分", f"{total} / 45", level.split(" ")[0])
        st.metric("心理韧性(CD-RISC)", f"{cdrisc} / 30", "")
        st.metric("职业韧性", f"{career} / 15", "")

    with col2:
        st.info(suggestion)

    categories = ["适应力", "目标感", "抗压力", "乐观性", "坚持力", "支持力"]
    cdrisc_breakdown = [
        scores_map[st.session_state.answers[0]] + scores_map[st.session_state.answers[1]],
        scores_map[st.session_state.answers[3]] + scores_map[st.session_state.answers[9]],
        scores_map[st.session_state.answers[4]] + scores_map[st.session_state.answers[8]],
        scores_map[st.session_state.answers[5]],
        scores_map[st.session_state.answers[6]] + scores_map[st.session_state.answers[7]],
        scores_map[st.session_state.answers[1]] + scores_map[st.session_state.answers[2]],
    ]

    fig = go.Figure(data=go.Scatterpolar(
        r=cdrisc_breakdown + [cdrisc_breakdown[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='你的韧性画像'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 6])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("**📌 温馨提示:本测评仅供参考，不构成医学诊断。如感到持续困扰，请咨询遵义医科大学心理健康中心。**")

    if st.button("重新测评"):
        st.session_state.answers = ["从不"] * 15
        st.session_state.submitted = False
        st.experimental_rerun()




#plotly加交互数据分析






