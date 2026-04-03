# 🚀 Excel数据问答系统 - 部署指南

本指南将帮助您将Excel数据问答系统部署到公网，使其可以通过GitHub仓库地址访问。

## 📋 目录

- [部署选项对比](#部署选项对比)
- [推荐方案：Render部署](#推荐方案render部署)
- [备选方案：Streamlit Cloud](#备选方案streamlit-cloud)
- [备选方案：Vercel](#备选方案vercel)
- [GitHub Pages静态部署](#github-pages静态部署)
- [常见问题解答](#常见问题解答)

---

## 🎯 部署选项对比

| 平台 | 类型 | 免费额度 | 优点 | 缺点 | 推荐度 |
|------|------|----------|------|------|--------|
| **Render** | 云服务 | 750小时/月 | 支持Python后端，配置简单，自动部署 | 需要信用卡验证 | ⭐⭐⭐⭐⭐ |
| **Streamlit Cloud** | 云服务 | 无限制 | 专为数据应用设计，部署极简 | 需要修改代码结构 | ⭐⭐⭐⭐ |
| **Vercel** | 云服务 | 100GB带宽 | 速度快，支持GitHub集成 | 主要用于前端，后端需调整 | ⭐⭐⭐ |
| **GitHub Pages** | 静态托管 | 无限制 | 完全免费，与GitHub集成 | 仅支持静态页面 | ⭐⭐ |

---

## 🌟 推荐方案：Render部署

Render是一个现代化的云平台，支持Python Flask应用，提供免费额度，非常适合部署此类应用。

### 📝 前置要求

- GitHub账号
- Render账号（需要GitHub账号登录）
- 信用卡（用于验证，免费套餐不会扣费）

### 🔧 步骤1：准备代码

项目已经包含以下部署配置文件：

```
excel-qa-system/
├── app.py              # Flask应用（已配置生产环境）
├── requirements.txt    # Python依赖（已添加gunicorn）
├── Procfile           # Render启动配置
├── render.yaml        # Render部署配置
└── .env.example       # 环境变量示例
```

### 🚀 步骤2：部署到Render

#### 2.1 注册Render账号

1. 访问 [https://render.com](https://render.com)
2. 点击 "Sign Up" 使用GitHub账号注册
3. 完成邮箱验证

#### 2.2 创建新服务

1. 登录Render后，点击 "New +"
2. 选择 "Web Service"
3. 连接GitHub仓库：
   - 选择 "Connect a repository"
   - 搜索并选择 `FrogSky/auto-excel`
   - 点击 "Connect"

#### 2.3 配置服务

**基本信息：**
- **Name**: `auto-excel`（或其他名称）
- **Region**: 选择离您最近的区域（如 Singapore）
- **Branch**: `main`

**构建配置：**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**环境变量：**
- `PYTHON_VERSION`: `3.13.0`
- `PORT`: `10000`（Render默认端口）

**高级配置：**
- **Instance Type**: `Free`
- **RAM**: `512 MB`
- **CPU**: `0.1`

#### 2.4 配置持久化存储（可选）

由于应用需要上传文件，建议配置持久化存储：

1. 在服务配置页面，找到 "Disk" 部分
2. 点击 "Add Disk"
3. 配置：
   - **Name**: `uploads`
   - **Mount Path**: `/opt/render/project/uploads`
   - **Size**: `1 GB`

#### 2.5 部署应用

1. 点击 "Create Web Service"
2. 等待构建和部署完成（通常需要2-5分钟）
3. 部署成功后，会获得一个公网URL，如：`https://auto-excel.onrender.com`

### 🔗 步骤3：配置自定义域名（可选）

如果您想使用自定义域名：

1. 在服务页面，点击 "Domains"
2. 点击 "Add Domain"
3. 输入您的域名（如 `excel.yourdomain.com`）
4. 按照提示配置DNS记录

### 📊 步骤4：监控和维护

**查看日志：**
- 在服务页面点击 "Logs" 查看运行日志
- 可以实时监控应用状态

**自动部署：**
- 当您推送代码到GitHub时，Render会自动重新部署
- 可以在 "Settings" 中配置部署分支

**性能监控：**
- 在 "Metrics" 中查看CPU、内存使用情况
- 免费套餐有750小时/月的限制

---

## 🎨 备选方案：Streamlit Cloud

Streamlit Cloud是专门为数据应用设计的云平台，部署非常简单。

### 📝 前置要求

- Streamlit账号
- GitHub账号

### 🔧 步骤1：修改代码结构

需要将Flask应用转换为Streamlit应用。创建 `streamlit_app.py`：

```python
import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(
    page_title="Excel数据问答系统",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Excel数据问答系统")

# 文件上传
uploaded_file = st.file_uploader(
    "上传Excel文件",
    type=['xlsx', 'xls', 'csv'],
    help="支持.xlsx, .xls, .csv格式"
)

if uploaded_file:
    # 读取文件
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # 显示数据信息
    st.success(f"✅ 文件上传成功！")
    st.info(f"📊 数据规模：{len(df)} 行 × {len(df.columns)} 列")
    
    # 显示数据预览
    st.subheader("📋 数据预览")
    st.dataframe(df.head(10))
    
    # 数据分析
    st.subheader("📈 数据分析")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**列信息：**")
        for col in df.columns:
            st.write(f"- {col} ({df[col].dtype})")
    
    with col2:
        st.write("**统计信息：**")
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.dataframe(df[numeric_cols].describe())
        else:
            st.write("没有数值列")
    
    # 智能问答
    st.subheader("🤖 智能问答")
    question = st.text_input("请输入您的问题：")
    
    if question:
        # 这里可以集成OpenAI API或使用规则匹配
        st.info(f"您的问题是：{question}")
        # 添加问答逻辑...
```

### 🚀 步骤2：部署到Streamlit Cloud

1. 访问 [https://share.streamlit.io](https://share.streamlit.io)
2. 点击 "Deploy an app"
3. 连接GitHub仓库 `FrogSky/auto-excel`
4. 配置：
   - **Repository**: `FrogSky/auto-excel`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. 点击 "Deploy"

### 📝 步骤3：创建requirements.txt

确保 `requirements.txt` 包含：
```
streamlit
pandas
openpyxl
python-dotenv
```

---

## 🌐 备选方案：Vercel

Vercel主要用于前端应用，但也可以部署Python后端。

### 🔧 步骤1：创建vercel.json配置

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 🚀 步骤2：部署到Vercel

1. 访问 [https://vercel.com](https://vercel.com)
2. 使用GitHub账号登录
3. 点击 "New Project"
4. 选择 `FrogSky/auto-excel` 仓库
5. 配置环境变量
6. 点击 "Deploy"

---

## 📄 GitHub Pages静态部署

GitHub Pages仅支持静态页面，但可以创建一个静态展示页面。

### 🔧 步骤1：创建静态页面

创建 `docs/index.html`：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Excel数据问答系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="text-center">
            <h1>📊 Excel数据问答系统</h1>
            <p class="lead">智能Excel数据分析工具</p>
        </div>
        
        <div class="row mt-5">
            <div class="col-md-6 offset-md-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">功能特性</h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">📤 Excel文件上传</li>
                            <li class="list-group-item">📊 数据预览和分析</li>
                            <li class="list-group-item">🤖 智能问答</li>
                            <li class="list-group-item">📈 统计分析</li>
                        </ul>
                        
                        <div class="mt-4">
                            <a href="https://auto-excel.onrender.com" class="btn btn-primary btn-lg">
                                访问应用
                            </a>
                        </div>
                        
                        <div class="mt-3">
                            <a href="https://github.com/FrogSky/auto-excel" class="btn btn-outline-secondary">
                                查看源码
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

### 🚀 步骤2：启用GitHub Pages

1. 进入GitHub仓库设置
2. 点击 "Pages"
3. 在 "Source" 中选择：
   - **Branch**: `main`
   - **Folder**: `/docs`
4. 点击 "Save"

### 🔗 步骤3：访问静态页面

部署完成后，可以通过以下地址访问：
```
https://frogsky.github.io/auto-excel/
```

---

## ❓ 常见问题解答

### Q1: Render免费套餐有什么限制？

**A:** Render免费套餐限制：
- 750小时/月的运行时间
- 512MB RAM
- 0.1 CPU
- 15分钟无活动会休眠
- 首次访问需要30-60秒唤醒

### Q2: 如何配置OpenAI API密钥？

**A:** 在Render中配置环境变量：
1. 进入服务设置页面
2. 找到 "Environment Variables"
3. 添加变量：
   - **Key**: `OPENAI_API_KEY`
   - **Value**: 您的OpenAI API密钥

### Q3: 如何处理文件上传的持久化？

**A:** Render提供持久化存储：
1. 在服务配置中添加Disk
2. 挂载路径：`/opt/render/project/uploads`
3. 免费套餐提供1GB存储空间

### Q4: 如何查看应用日志？

**A:** 在Render中：
1. 进入服务页面
2. 点击 "Logs" 标签
3. 可以查看实时日志和历史日志

### Q5: 如何实现自动部署？

**A:** Render支持自动部署：
1. 连接GitHub仓库后自动启用
2. 推送代码到main分支会自动触发部署
3. 可以在设置中配置部署分支

### Q6: 应用休眠后如何保持活跃？

**A:** 可以使用外部监控服务：
- 使用UptimeRobot等免费监控服务
- 设置每5分钟ping一次应用
- 这样可以保持应用始终活跃

### Q7: 如何配置自定义域名？

**A:** 在Render中：
1. 进入服务设置
2. 点击 "Domains"
3. 添加自定义域名
4. 配置DNS记录指向Render

### Q8: 如何升级到付费套餐？

**A:** 在Render中：
1. 进入服务设置
2. 点击 "Change Plan"
3. 选择合适的套餐
4. 付费套餐提供更多资源和更快的响应速度

---

## 📞 技术支持

如果遇到问题，可以：

1. 查看Render文档：https://render.com/docs
2. 查看项目GitHub Issues
3. 联系开发者

---

## 🎉 总结

推荐使用 **Render** 部署方案，因为：
- ✅ 支持完整的Python Flask应用
- ✅ 配置简单，部署快速
- ✅ 提供免费额度
- ✅ 自动部署和监控
- ✅ 支持持久化存储

按照本指南操作，您就可以将Excel数据问答系统部署到公网，让任何人都可以通过GitHub仓库地址访问您的应用！