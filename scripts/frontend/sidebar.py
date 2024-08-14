import streamlit as st
from streamlit_extras.badges import badge


def show_header():
    st.title(":blue[AI简历助手]")


def show_sidebar():
    with st.sidebar:
        st.image("Assets/img/header_image.png")
        st.subheader(
            "Datawhale AI 夏令营 第四期 浪潮信息源大模型应用开发——AI简历助手"
        )

        st.markdown(
            "基于 [Resume Matcher](https://github.com/srbhr/resume-matcher) 项目迭代开发"
        )

        st.html(
            "<h1 align='center'><a style='text-decoration: none;' href='https://github.com/YYForReal/ResumeRefiner'>ResumeRefiner⭐</a></h1>"
        )

        st.markdown("当前项目地址👇")
        badge(type="github", name="YYForReal/ResumeRefiner")

        st.markdown(
            "队伍: AI学习小分队"
        )

