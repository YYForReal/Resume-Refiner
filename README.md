<div align="center">

# ResumeRefiner

</div>

<br>

<div align="center">

Datawhale AI 夏令营 第四期 浪潮信息源大模型应用开发——AI简历助手



## 它是如何工作的？

</div>

简历匹配器将你的简历和职位描述作为输入，通过 Python 解析它们，并模拟 ATS 的功能，提供见解和建议，以使你的简历对 ATS 更友好。

过程如下：

1. **解析**：系统使用 Python 解析你的简历和提供的职位描述，就像 ATS 一样。

2. **关键词提取**：工具使用先进的机器学习算法从职位描述中提取最相关的关键词。这些关键词代表了雇主所寻求的技能、资格和经验。

3. **关键术语提取**：除了关键词提取，工具还使用 textacy 识别职位描述中的主要关键术语或主题。这一步有助于理解简历所涉及的更广泛的背景。

4. **使用 FastEmbedd 进行向量相似度计算**：工具使用 [FastEmbedd](https://github.com/qdrant/fastembed)，一个高效的嵌入系统，来衡量你的简历与职位描述的匹配程度。它们越相似，你的简历通过 ATS 筛选的可能性就越高。

<br/>

<div align="center">

## 如何安装

</div>

按照以下步骤设置环境并运行应用程序。

1. 克隆仓库。。

```bash
git clone git@github.com:YYForReal/ResumeRefiner.git
cd Resume-Matcher

```

拉一个emebdding模型到models文件夹里面 去替换原仓库的 BAAI/bge-base-en
```
cd models
git clone https://www.modelscope.cn/maidalun/bce-embedding-base_v1.git
cd ..
```
   

2. 激活虚拟环境。

   ```bash
   conda create -n resume_refiner python==3.11
   ```

5. 安装依赖项：

   ```bash
   pip install -r requirements.txt
   ```

```
pip install streamlit -i https://pypi.mirrors.ustc.edu.cn/simple
pip install st-annotated-text -i https://pypi.mirrors.ustc.edu.cn/simple
pip install streamlit-camera-input-live -i https://pypi.mirrors.ustc.edu.cn/simple
pip install streamlit-card -i https://pypi.mirrors.ustc.edu.cn/simple
pip install streamlit-embedcode -i https://pypi.mirrors.ustc.edu.cn/simple
pip install streamlit-extras -i https://pypi.mirrors.ustc.edu.cn/simple
pip install streamlit-faker -i https://pypi.mirrors.ustc.edu.cn/simple
pip install streamlit-image-coordinates -i https://pypi.mirrors.ustc.edu.cn/simple
pip install streamlit-keyup -i https://pypi.mirrors.ustc.edu.cn/simple
pip install streamlit-toggle-switch -i https://pypi.mirrors.ustc.edu.cn/simple
pip install streamlit-vertical-slider -i https://pypi.mirrors.ustc.edu.cn/simple
```

```
pip install pypdf
pip install textacy
pip install spacy==3.6.0 
```



然后进models文件夹(确保手动下了模型，有文件，也可以看requirements.txt里面的链接)，
```
cd models
pip install en_core_web_sm-3.6.0-py3-none-any.whl
pip install en_core_web_md-3.6.0-py3-none-any.whl
cd ..

```

6. 准备数据：

   - 简历：将你的 PDF 格式的简历放在 `Data/Resumes` 文件夹中。删除该文件夹中现有的内容。
   - 职位描述：将你的 PDF 格式的职位描述放在 `Data/JobDescription` 文件夹中。删除该文件夹中现有的内容。

7. 将简历解析为 JSON：

   ```python
   python run_first.py
   ```

8. 设置并批量处理文件大小：

   ```python
   python run_first.py
   ```

   ```bash
   echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
   ```

9. 运行应用程序：

   ```python
   streamlit run streamlit_app.py
   ```

**注意**：对于本地版本，你不需要运行 "streamlit_second.py"，因为它专门用于部署到 Streamlit 服务器。


<br/>


#### 技术栈

- Python 
   - Streamlit 
   - FastEmbedd 
   - More...

<br/>