import json
import os
from typing import List

import networkx as nx
import nltk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from annotated_text import annotated_text, parameters
from streamlit_extras import add_vertical_space as avs
from streamlit_extras.badges import badge

from scripts.similarity.get_score import *
from scripts.utils import get_filenames_from_dir
from scripts.utils.logger import init_logging_config

# 设置页面配置
st.set_page_config(
    page_title="ResumeRefiner",
    page_icon="Assets/img/favicon.ico",
    initial_sidebar_state="auto",
)

init_logging_config()
cwd = find_path("Resume-Matcher")
config_path = os.path.join(cwd, "scripts", "similarity")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

parameters.SHOW_LABEL_SEPARATOR = False
parameters.BORDER_RADIUS = 3
parameters.PADDING = "0.5 0.25rem"


def create_star_graph(nodes_and_weights, title):
    # 创建一个空图
    G = nx.Graph()

    # 添加中心节点
    central_node = "resume"
    G.add_node(central_node)

    # 向图中添加节点和边及权重
    for node, weight in nodes_and_weights:
        G.add_node(node)
        G.add_edge(central_node, node, weight=weight * 100)

    # 获取节点的布局位置
    pos = nx.spring_layout(G)

    # 创建边的轨迹
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # 创建节点的轨迹
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="Rainbow",
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title="节点连接数",
                xanchor="left",
                titleside="right",
            ),
            line_width=2,
        ),
    )

    # 按连接数给节点着色
    node_adjacencies = []
    node_text = []
    for node in G.nodes():
        adjacencies = list(G.adj[node])
        node_adjacencies.append(len(adjacencies))
        node_text.append(f"{node}<br># 连接数: {len(adjacencies)}")

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # 创建图形
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    # 显示图形
    st.plotly_chart(fig)


def create_annotated_text(
    input_string: str, word_list: List[str], annotation: str, color_code: str
):
    # 对输入字符串进行分词
    tokens = nltk.word_tokenize(input_string)

    # 将列表转换为集合以便快速查找
    word_set = set(word_list)

    # 初始化一个空列表来保存注释文本
    annotated_text = []

    for token in tokens:
        # 检查 token 是否在集合中
        if token in word_set:
            # 如果在，添加包含 token、注释和颜色代码的元组
            annotated_text.append((token, annotation, color_code))
        else:
            # 如果不在，直接添加 token
            annotated_text.append(token)

    return annotated_text


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def tokenize_string(input_string):
    tokens = nltk.word_tokenize(input_string)
    return tokens


# 显示主标题和子标题
st.title("简历优化助手")
with st.sidebar:
    st.image("Assets/img/header_image.png")
    st.subheader(
        "Datawhale AI 夏令营 第四期 浪潮信息源大模型应用开发——AI简历助手"
    )
    st.markdown(
        "访问网站 [www.resumematcher.fyi](https://www.resumematcher.fyi/)"
    )

    st.markdown(
        "在 [GitHub](https://github.com/srbhr/resume-matcher) 给 Resume Matcher 点个 ⭐"
    )

    badge(type="github", name="srbhr/Resume-Matcher")
    st.markdown("关注我以获取最新动态。")
    badge(type="twitter", name="_srbhr_")
    st.markdown(
        "如果您喜欢这个项目并希望进一步支持开发，请考虑 👇"
    )
    badge(type="buymeacoffee", name="srbhr")

st.divider()
avs.add_vertical_space(1)

resume_names = get_filenames_from_dir("Data/Processed/Resumes")


st.markdown(
    f"##### 共有 {len(resume_names)} 份简历。请选择以下菜单中的一份："
)
output = st.selectbox(f"", resume_names)


avs.add_vertical_space(5)

# st.write("你选择了 ", output, " 打印简历")
selected_file = read_json("Data/Processed/Resumes/" + output)

avs.add_vertical_space(2)
st.markdown("#### 解析后的简历数据")
st.caption(
    "这段文本是从你的简历中解析出来的。这是被 ATS 解析后的样子。"
)
st.caption("利用这个信息了解如何使你的简历更适合 ATS。")
avs.add_vertical_space(3)
# st.json(selected_file)
st.write(selected_file["clean_data"])

avs.add_vertical_space(3)
st.write("现在让我们看看从简历中提取的关键词。")

annotated_text(
    create_annotated_text(
        selected_file["clean_data"],
        selected_file["extracted_keywords"],
        "KW",
        "#0B666A",
    )
)

avs.add_vertical_space(5)
st.write("现在让我们看看从简历中提取的实体。")

# 调用函数并传入数据
create_star_graph(selected_file["keyterms"], "简历中的实体")

df2 = pd.DataFrame(selected_file["keyterms"], columns=["关键词", "值"])

# 创建字典
keyword_dict = {}
for keyword, value in selected_file["keyterms"]:
    keyword_dict[keyword] = value * 100

fig = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=["关键词", "值"], font=dict(size=12), fill_color="#070A52"
            ),
            cells=dict(
                values=[list(keyword_dict.keys()), list(keyword_dict.values())],
                line_color="darkslategray",
                fill_color="#6DA9E4",
            ),
        )
    ]
)
st.plotly_chart(fig)

st.divider()

fig = px.treemap(
    df2,
    path=["关键词"],
    values="值",
    color_continuous_scale="Rainbow",
    title="从简历中提取的关键词/主题",
)
st.write(fig)

avs.add_vertical_space(5)

job_descriptions = get_filenames_from_dir("Data/Processed/JobDescription")


st.markdown(
    f"##### 共有 {len(job_descriptions)} 份职位描述。请选择以下菜单中的一份："
)
output = st.selectbox("", job_descriptions)


avs.add_vertical_space(5)

selected_jd = read_json("Data/Processed/JobDescription/" + output)

avs.add_vertical_space(2)
st.markdown("#### 职位描述")
st.caption(
    "目前我正在从 PDF 中解析它，但未来会从 txt 或直接粘贴。"
)
avs.add_vertical_space(3)
# st.json(selected_file)
st.write(selected_jd["clean_data"])

st.markdown("#### 职位描述和简历中的常见词汇已被高亮显示。")

annotated_text(
    create_annotated_text(
        selected_file["clean_data"], selected_jd["extracted_keywords"], "JD", "#F24C3D"
    )
)

st.write("现在让我们看看从职位描述中提取的实体。")

# 调用函数并传入数据
create_star_graph(selected_jd["keyterms"], "职位描述中的实体")

df2 = pd.DataFrame(selected_jd["keyterms"], columns=["关键词", "值"])

# 创建字典
keyword_dict = {}
for keyword, value in selected_jd["keyterms"]:
    keyword_dict[keyword] = value * 100

fig = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=["关键词", "值"], font=dict(size=12), fill_color="#070A52"
            ),
            cells=dict(
                values=[list(keyword_dict.keys()), list(keyword_dict.values())],
                line_color="darkslategray",
                fill_color="#6DA9E4",
            ),
        )
    ]
)
st.plotly_chart(fig)

st.divider()

fig = px.treemap(
    df2,
    path=["关键词"],
    values="值",
    color_continuous_scale="Rainbow",
    title="从选定的职位描述中提取的关键词/主题",
)
st.write(fig)

avs.add_vertical_space(3)

resume_string = " ".join(selected_file["extracted_keywords"])
jd_string = " ".join(selected_jd["extracted_keywords"])
result = get_score(resume_string, jd_string)
similarity_score = round(result[0].score * 100, 2)
score_color = "green"
if similarity_score < 60:
    score_color = "red"
elif 60 <= similarity_score < 75:
    score_color = "orange"
st.markdown(
    f"简历与职位描述的相似度评分为 "
    f'<span style="color:{score_color};font-size:24px; font-weight:Bold">{similarity_score}</span>',
    unsafe_allow_html=True,
)

# 返回顶部
st.markdown("[:arrow_up: 返回顶部](#简历优化助手)")