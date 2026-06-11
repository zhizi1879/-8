#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import streamlit as st
import plotly.graph_objects as go         #plotly.graph_objects是子模块不是函数，函数是（）并且在库之后的
import numpy as np
import time
from datetime import datetime

st.set_page_config(page_title="规培生正念解压站", layout="centered")
# ========== 欢迎首页（新增）==========
if "show_home" not in st.session_state:
    st.session_state.show_home = True
if "page" not in st.session_state:
    st.session_state.page = "📋 情绪识别小助手"

if st.session_state.show_home:
    st.markdown("""
    <div style='text-align:center;padding:50px 20px 30px;'>
        <div style='font-size:4em;margin-bottom:15px;'>🧘‍♀️</div>
        <h1 style='font-size:2em;margin-bottom:8px;color:#1e1b4b;'>规培生正念解压站</h1>
        <p style='font-size:1.05em;color:#6b7280;margin-bottom:10px;'>遵义医科大学 · 规培生心理支持系统</p>
        <p style='font-size:0.95em;color:#9ca3af;margin-bottom:40px;'>累了就来坐坐，这里没有考核 🌿</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    modules = [
        ("📋", "情绪识别小助手", "PHQ-9 + GAD-7 专业测评\n2分钟了解你的情绪状态", "📋 情绪识别小助手"),
        ("🧘", "规培间隙的放松", "呼吸法 · 身体扫描 · 正念倾听\n给自己3分钟", "🧘 规培间隙的放松"),
        ("📝", "工作情绪存档", "记录每日心情\n用数据看见情绪变化", "📝 工作情绪存档"),
        ("🌳", "医护吐槽安全屋", "完全匿名树洞\n说出来会好受一点", "🌳 医护吐槽安全屋"),
        ("📚", "情绪急救科普册", "规培生必知心理知识\n3分钟能改变什么", "📚 情绪急救科普册"),
        ("🏆", "抗压升级日志", "打卡 · 徽章 · 等级\n见证你的每一步成长", "🏆 抗压升级日志"),
    ]

    for i, (icon, title, desc, page_name) in enumerate(modules):
        with col1 if i < 2 else (col2 if i < 4 else col3):
            if st.button(f"{icon}  {title}", key=f"home_btn_{i}"):
                st.session_state.page = page_name
                st.session_state.show_home = False
                st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center;padding:10px 0 30px;color:#9ca3af;font-size:0.85em;'>
        💡 本系统仅供减压参考，不构成医学建议 · 持续困扰请咨询心理健康中心 28643572
    </div>
    """, unsafe_allow_html=True)

else:
    page = st.radio("", ["📋 情绪识别小助手", "🧘 规培间隙的放松", "📝 工作情绪存档", "🌳 医护吐槽安全屋", "📚 情绪急救科普册", "🏆 抗压升级日志"], horizontal=True)

    # 新增:返回首页按钮（放在导航下方）
    st.markdown("")
    if st.button("🏠 返回首页", key="btn_back_home", use_container_width=False):
        st.session_state.show_home = True
        st.rerun()



st.title("🧘 规培生正念解压站")
st.markdown("**遵义医科大学 · 规培生心理支持系统**")
st.markdown("---")

# ========== 全局初始化 ==========
if "check_in_days" not in st.session_state:
    st.session_state.check_in_days = 0
if "total_sessions" not in st.session_state:
    st.session_state.total_sessions = 0
if "badges" not in st.session_state:
    st.session_state.badges = []
if "mindfulness_done" not in st.session_state:
    st.session_state.mindfulness_done = False
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []
if "tree_hole_messages" not in st.session_state:
    st.session_state.tree_hole_messages = []

# ========== 音频链接（纯音乐/白噪音）==========
BREATH_AUDIO = "https://assets.mixkit.co/active_storage/sfx/2018/2018-preview.mp3"
BODY_AUDIO  = "https://assets.mixkit.co/active_storage/sfx/2021/2021-preview.mp3"
LISTEN_AUDIO = "https://assets.mixkit.co/active_storage/sfx/2023/2023-preview.mp3"

# ========== 导航 ==========
page = st.radio("", ["📋 情绪识别小助手", "🧘 规培间隙的放松", "📝 工作情绪存档", "🌳 医护吐槽安全屋", "📚 情绪急救科普册", "🏆 抗压升级日志"], horizontal=True)

# ========================
# 页面1:心理测评
# ========================
if page == "📋 情绪识别小助手":
    phq9_questions = [
        "做事时提不起劲或没有兴趣",
        "感到心情低落、沮丧或绝望",
        "入睡困难、睡不安稳或睡眠过多",
        "感觉疲倦或没有活力",
        "食欲不振或吃太多",
        "觉得自己很糟——或觉得自己很失败，或让自己或家人失望",
        "对事物专注有困难，例如阅读报纸或看电视时",
        "动作或说话速度缓慢到别人已经注意到？或正好相反——失神或坐立不安",
        "有不如死掉或用某种方式伤害自己的念头",
    ]
    gad7_questions = [
        "感觉紧张、焦虑或急切",
        "不能够停止或控制担忧",
        "对各种各样的事情担忧过多",
        "很难放松下来",
        "由于不安而无法静坐",
        "变得容易烦恼或急躁",
        "感到似乎将有可怕的事情发生而害怕",
    ]
    all_questions = phq9_questions + gad7_questions
    options = ["完全不会", "好几天", "一半以上的天数", "几乎每天"]
    scores_map = {"完全不会": 0, "好几天": 1, "一半以上的天数": 2, "几乎每天": 3}

    if "answers" not in st.session_state:
        st.session_state.answers = ["完全不会"] * 16
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    def calc_score(answers):
        phq9 = sum(scores_map[a] for a in answers[:9])
        gad7 = sum(scores_map[a] for a in answers[9:])
        total = phq9 + gad7
        return total, phq9, gad7

    def get_level(phq9, gad7):
        if phq9 <= 4:
            phq9_level = "🟢 情绪正常"
            phq9_tip = "你的情绪状态良好，继续保持正念练习！"
        elif phq9 <= 9:
            phq9_level = "🟡 轻度情绪困扰"
            phq9_tip = "有一些情绪波动，建议每天做3分钟正念呼吸。"
        elif phq9 <= 14:
            phq9_level = "🟠 中度情绪困扰"
            phq9_tip = "情绪压力较大，建议主动找心理老师聊聊。"
        else:
            phq9_level = "🔴 重度情绪困扰"
            phq9_tip = "你正在经历较大的情绪困难，请尽快联系心理健康中心:28643572"

        if gad7 <= 4:
            gad7_level = "🟢 焦虑正常"
        elif gad7 <= 9:
            gad7_level = "🟡 轻度焦虑"
        elif gad7 <= 14:
            gad7_level = "🟠 中度焦虑"
        else:
            gad7_level = "🔴 重度焦虑"

        return phq9_level, phq9_tip, gad7_level

    if not st.session_state.submitted:
        st.subheader("最近两周，以下情况出现的频率是？")
        for i, q in enumerate(all_questions):
            col1, col2 = st.columns([3, 1])
            with col1:
                label = "PHQ-9" if i < 9 else "GAD-7"
                st.markdown(f"**{label} {i+1 if i < 9 else i-8}.** {q}")
            with col2:
                st.session_state.answers[i] = st.radio("", options, key=f"q{i}", index=0, label_visibility="collapsed")
        if st.button("提交测评", type="primary", key="btn_submit"):
            st.session_state.submitted = True
            st.rerun()
    else:
        total, phq9, gad7 = calc_score(st.session_state.answers)
        phq9_level, phq9_tip, gad7_level = get_level(phq9, gad7)

        st.markdown("## 📊 情绪监测结果")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric("抑郁评分 (PHQ-9)", f"{phq9} / 27", phq9_level.split(" ")[0])
            st.metric("焦虑评分 (GAD-7)", f"{gad7} / 21", gad7_level.split(" ")[0])
            st.metric("综合评分", f"{total} / 48", "")
        with col2:
            st.info(phq9_tip)

        # 仪表盘
        fig = go.Figure(go.Indicator(mode="gauge+number", value=phq9, domain={'x': [0, 0.5], 'y': [0, 1]},
            title={'text': f"PHQ-9 抑郁 {phq9}/27"},
            gauge={'axis': {'range': [0, 27]}, 'bar': {'color': "#6366f1"},
                'steps': [{'range': [0, 4], 'color': "#dcfce7"}, {'range': [5, 9], 'color': "#fef08a"},
                          {'range': [10, 14], 'color': "#fed7aa"}, {'range': [15, 27], 'color': "#fecaca"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.8, 'value': 10}}))
        fig.add_trace(go.Indicator(mode="gauge+number", value=gad7, domain={'x': [0.5, 1], 'y': [0, 1]},
            title={'text': f"GAD-7 焦虑 {gad7}/21"},
            gauge={'axis': {'range': [0, 21]}, 'bar': {'color': "#8b5cf6"},
                'steps': [{'range': [0, 4], 'color': "#dcfce7"}, {'range': [5, 9], 'color': "#fef08a"},
                          {'range': [10, 14], 'color': "#fed7aa"}, {'range': [15, 21], 'color': "#fecaca"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.8, 'value': 10}}))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

        if st.button("🔄 重新测评", key="btn_retest"):
            st.session_state.answers = ["完全不会"] * 16
            st.session_state.submitted = False
            st.rerun()

# ========================
# 页面2:正念练习（纯音乐版）
# ========================
elif page == "🧘 规培间隙的放松":
    st.subheader("选择一个练习，给自己几分钟 🌿")

    exercise = st.selectbox(
        "",
        ["🫁 4-7-8 呼吸法（2分钟，值夜班前推荐）",
         "🧘 身体扫描（3分钟，下班后推荐）",
         "👂 正念倾听（2分钟，通勤时推荐）"]
    )

    audio_url = ""
    if "呼吸" in exercise:
        audio_url = BREATH_AUDIO
    elif "身体扫描" in exercise:
        audio_url = BODY_AUDIO
    else:
        audio_url = LISTEN_AUDIO

    if st.button("🎧 开始练习", type="primary", key="btn_mindfulness"):
        st.session_state.mindfulness_done = True
        st.session_state.total_sessions += 1

        st.audio(audio_url)

        placeholder = st.empty()

        if "4-7-8" in exercise:
            steps = [
                ("准备好了吗？深呼吸一次...", 3),
                ("🫁 吸气... 1... 2... 3... 4...", 4),
                ("屏住呼吸... 1... 2... 3... 4... 5... 6... 7...", 7),
                ("💨 慢慢呼气... 1... 2... 3... 4... 5... 6... 7... 8...", 8),
                ("🫁 吸气... 1... 2... 3... 4...", 4),
                ("屏住... 1... 2... 3... 4... 5... 6... 7...", 7),
                ("💨 呼气... 1... 2... 3... 4... 5... 6... 7... 8...", 8),
                ("🫁 吸气... 1... 2... 3... 4...", 4),
                ("屏住... 1... 2... 3... 4... 5... 6... 7...", 7),
                ("💨 呼气... 1... 2... 3... 4... 5... 6... 7... 8...", 8),
            ]
            for text, sec in steps:
                placeholder.markdown(f"## {text}")
                time.sleep(sec)
            placeholder.markdown("## ✅ 练习完成！感觉好点了吗？")

        elif "身体扫描" in exercise:
            body_parts = [
                ("头顶", "感受头顶的温度... 放松...", 3),
                ("额头", "额头舒展开... 放下紧张...", 3),
                ("眼睛", "眼球放松... 不要用力看...", 3),
                ("下巴", "下巴松开... 嘴巴微微张开...", 3),
                ("脖子", "脖子变软... 肩膀下沉...", 4),
                ("肩膀", "肩膀放下来... 不要耸肩...", 4),
                ("手臂", "手臂变沉... 完全放松...", 4),
                ("胸口", "胸口打开... 呼吸顺畅...", 4),
                ("腹部", "腹部起伏... 跟着呼吸...", 4),
                ("双腿", "双腿变重... 完全支撑...", 4),
                ("脚底", "脚底踏实... 感受地面...", 4),
            ]
            for part, text, sec in body_parts:
                placeholder.markdown(f"### 感受你的 **{part}**... {text}")
                time.sleep(sec)
            placeholder.markdown("## ✅ 扫描完成！")

        elif "正念倾听" in exercise:
            steps = [
                ("找一个安静的地方...", 2),
                ("闭上眼睛...", 2),
                ("注意你听到的第一个声音...", 3),
                ("不要评判，只是听...", 3),
                ("感受声音的远近、大小...", 3),
                ("回到自己的呼吸...", 3),
            ]
            for text, sec in steps:
                placeholder.markdown(f"# {text}")
                time.sleep(sec)
            placeholder.markdown("## ✅ 倾听完成！")

        st.rerun()

# ========================
# 页面3:情绪日记
# ========================
elif page == "📝 工作情绪存档":
    st.subheader("记录今天的心情 📊")

    mood_options = ["😊 很好", "🙂 还行", "😐 一般", "😔 不太好", "😢 很差"]
    mood_scores = [5, 4, 3, 2, 1]

    col1, col2 = st.columns([2, 1])
    with col1:
        mood_text = st.radio("今天心情如何？", mood_options, horizontal=True)
    with col2:
        if st.button("💾 记录", type="primary", key="btn_mood"):
            mood_score = mood_scores[mood_options.index(mood_text)]
            st.session_state.mood_history.append({
                "date": datetime.now().strftime("%m-%d %H:%M"),
                "mood": mood_text,
                "score": mood_score
            })
            st.rerun()

    if st.session_state.mood_history:
        st.markdown("---")
        st.markdown("### 📈 情绪趋势")
        dates = [h["date"] for h in st.session_state.mood_history]
        scores = [h["score"] for h in st.session_state.mood_history]

        fig = go.Figure(data=go.Scatter(
            x=dates, y=scores, mode='lines+markers',
            line=dict(color='#6366f1', width=3),
            marker=dict(size=10)
        ))
        fig.update_layout(
            title="近期情绪变化",
            xaxis_title="时间",
            yaxis_title="心情分数",
            yaxis=dict(range=[0, 6], tickvals=[1, 2, 3, 4, 5],
                       ticktext=["😢 很差", "😔 不好", "😐 一般", "🙂 还行", "😊 很好"])
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### 📋 历史记录")
        for h in reversed(st.session_state.mood_history[-10:]):
            st.markdown(f"- **{h['date']}** {h['mood']}")
    else:
        st.info("还没有记录，快记下今天的心情吧！")

# ========================
# 页面4:匿名树洞
# ========================
elif page == "🌳 医护吐槽安全屋":
    st.subheader("说出来，会好受一点 🕳️")
    st.markdown("*完全匿名，没有人知道你是谁*")

    col1, col2 = st.columns([3, 1])
    with col1:
        new_msg = st.text_area("写下你想说的话...", height=150, placeholder="在这里，你可以说任何话...")
    with col2:
        if st.button("🕳️ 投入树洞", type="primary", key="btn_treehole"):
            if new_msg.strip():
                st.session_state.tree_hole_messages.append({
                    "text": new_msg.strip(),
                    "time": datetime.now().strftime("%m-%d %H:%M")
                })
                st.rerun()

    st.markdown("---")
    st.markdown("### 💬 树洞留言墙")
    if st.session_state.tree_hole_messages:
        for msg in reversed(st.session_state.tree_hole_messages):
            st.markdown(f"""
            <div style="background:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:10px;">
                <p>{msg['text']}</p>
                <small style="color:#888;">{msg['time']} · 匿名</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("*树洞还是空的，来写第一条吧...*")

    st.markdown("---")
    st.markdown("**📌 温馨提示:如果你正在经历严重心理困扰，请拨打24小时心理援助热线:28643572**")

# ========================
# 页面5:心理科普
# ========================
elif page == "📚 情绪急救科普册":
    st.subheader("规培生必知的心理知识 📖")

    tips = [
        {
            "title": "🧠 什么是正念？",
            "content": "正念是一种「有意识地、不加评判地关注当下」的心理状态。不是放空大脑，而是觉察此刻的感受，不逃避、不纠结。"
        },
        {
            "title": "😰 规培生为什么容易焦虑？",
            "content": "长期高压、睡眠不足、角色转换（学生→医生）、医患关系复杂，这些都是焦虑的温床。你不是脆弱，是环境太难了。"
        },
        {
            "title": "💡 3分钟能做什么？",
            "content": "研究表明，每天3分钟正念呼吸，坚持8周，焦虑水平可降低20%。你不需要1小时，只需要3分钟。"
        },
        {
            "title": "🎯 心理韧性不是天生的",
            "content": "心理韧性像肌肉，可以锻炼。每次你扛过一次压力，韧性就强一点。你现在觉得难，说明你在成长。"
        },
        {
            "title": "🚫 这些信号要注意",
            "content": "连续2周失眠、对什么都没兴趣、经常想哭、不想去医院——如果有这些情况，请主动找心理老师聊聊，这不丢人。"
        },
        {
            "title": "🤝 求助不是软弱",
            "content": "医生也会生病，规培生也会累。承认自己需要帮助，恰恰是一种专业素养。你照顾了所有人，也该照顾自己。"
        },
    ]

    for tip in tips:
        with st.expander(tip["title"]):
            st.markdown(tip["content"])

# ========================
# 页面6:成就系统
# ========================
elif page == "🏆 抗压升级日志":
    st.subheader("你的正念之旅 🏅")

    sessions = st.session_state.total_sessions
    if sessions >= 30:
        rank = "💎 正念大师"
    elif sessions >= 14:
        rank = "🥇 坚持达人"
    elif sessions >= 7:
        rank = "🥈 初级修行者"
    else:
        rank = "🌱 正念新手"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("累计练习", f"{sessions} 次", "")
    with col2:
        st.metric("当前等级", rank, "")
    with col3:
        st.metric("连续打卡", f"{st.session_state.check_in_days} 天", "")

    st.markdown("---")
    st.markdown("### 🎖 徽章墙")
    if st.session_state.badges:
        for badge in st.session_state.badges:
            st.markdown(f"- {badge}")
    else:
        st.markdown("*还没有徽章，快去练习吧！*")

    st.markdown("---")
    if st.button("✅ 今日打卡", type="primary", key="btn_checkin"):
        st.session_state.check_in_days += 1
        st.session_state.total_sessions += 1
        if st.session_state.check_in_days >= 7 and "🔥 连续7天" not in st.session_state.badges:
            st.session_state.badges.append("🔥 连续7天")
        if st.session_state.total_sessions >= 10 and "⭐ 10次练习" not in st.session_state.badges:
            st.session_state.badges.append("⭐ 10次练习")
        if st.session_state.total_sessions >= 30 and "💎 正念大师" not in st.session_state.badges:
            st.session_state.badges.append("💎 正念大师")
        st.rerun()

    st.markdown("---")
    st.markdown("**📌 本系统仅供减压参考，不构成医学建议。持续困扰请咨询心理健康中心。**")