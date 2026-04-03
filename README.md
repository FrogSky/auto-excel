# Excel数据问答系统

一个基于Flask的智能Excel数据分析系统，支持上传Excel文件并通过自然语言对话进行数据查询和分析。

## 功能特性

- 📤 **文件上传**: 支持拖拽或点击上传Excel文件（.xlsx, .xls, .csv）
- 📊 **数据预览**: 实时预览Excel数据，支持分页浏览
- 🤖 **智能问答**: 通过自然语言提问，获取数据分析结果
- 📈 **统计分析**: 自动生成数据统计信息和列信息
- 🎯 **双模式问答**: 
  - OpenAI GPT模式（需要API密钥）：更智能的自然语言理解
  - 内置规则模式：无需API密钥，支持常见数据查询

## 技术栈

### 后端
- Flask: Web框架
- Pandas: 数据处理
- OpenPyXL: Excel文件读取
- LangChain: AI集成（可选）
- OpenAI API: 智能问答（可选）

### 前端
- Bootstrap 5: UI框架
- Bootstrap Icons: 图标库
- 原生JavaScript: 交互逻辑

## 安装步骤

### 1. 克隆或下载项目

```bash
cd excel-qa-system
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量（可选）

复制 `.env.example` 为 `.env` 并配置OpenAI API密钥：

```bash
copy .env.example .env
```

编辑 `.env` 文件：

```
OPENAI_API_KEY=your_actual_api_key_here
```

**注意**: 如果不配置OpenAI API密钥，系统将使用内置的规则匹配模式，仍然可以回答常见的数据查询问题。

## 运行系统

### 启动后端服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

### 访问前端界面

在浏览器中打开：
```
http://localhost:5000/
```

## 使用说明

### 1. 上传Excel文件

- 拖拽Excel文件到上传区域
- 或点击"选择文件"按钮选择文件
- 支持的格式：.xlsx, .xls, .csv
- 最大文件大小：16MB

### 2. 查看数据

- 上传成功后，系统会自动显示数据预览
- 可以查看数据的基本信息（行数、列数）
- 浏览数据内容，支持分页
- 查看列的详细信息（数据类型、空值统计）

### 3. 智能问答

在右侧的问答区域输入问题，例如：

**基础查询：**
- "数据有多少行？"
- "有哪些列？"
- "数据类型是什么？"

**统计分析：**
- "统计信息"
- "平均值是多少？"
- "总和是多少？"

**数据质量：**
- "哪些列有空值？"
- "有多少缺失数据？"

**高级查询（需要OpenAI API）：**
- "分析销售数据的趋势"
- "找出异常值"
- "数据分布情况如何？"

## API接口

### 上传文件
```
POST /api/upload
Content-Type: multipart/form-data
Body: file (Excel文件)
```

### 获取文件列表
```
GET /api/files
```

### 获取文件数据
```
GET /api/file/{file_id}/data?page=1&per_page=10
```

### 查询数据
```
POST /api/file/{file_id}/query
Content-Type: application/json
Body: {"question": "你的问题"}
```

### 获取列信息
```
GET /api/file/{file_id}/columns
```

### 获取统计信息
```
GET /api/file/{file_id}/stats
```

### 删除文件
```
DELETE /api/file/{file_id}
```

### 健康检查
```
GET /api/health
```

## 项目结构

```
excel-qa-system/
├── app.py                 # Flask应用主文件
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量示例
├── .env                  # 环境变量（需要创建）
├── uploads/              # 上传文件存储目录（自动创建）
├── templates/
│   └── index.html        # 前端界面
└── README.md             # 项目说明
```

## 注意事项

1. **文件大小限制**: 默认最大16MB，可在 `app.py` 中修改 `MAX_CONTENT_LENGTH`
2. **数据安全**: 上传的文件存储在服务器本地，重启服务后数据会清空
3. **API密钥**: OpenAI API密钥需要自行申请，不配置也能使用基础功能
4. **浏览器兼容**: 推荐使用Chrome、Firefox、Edge等现代浏览器

## 常见问题

### Q: 上传文件后没有显示数据？
A: 检查文件格式是否正确，确保文件没有损坏。

### Q: 问答功能不工作？
A: 
- 如果配置了OpenAI API，检查API密钥是否正确
- 如果没有配置API密钥，确保问题使用的是内置规则支持的关键词

### Q: 如何修改端口？
A: 在 `app.py` 的最后一行修改端口号：
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # 修改5000为其他端口
```

### Q: 数据量很大怎么办？
A: 系统支持分页浏览，可以调整每页显示的行数。对于非常大的文件，建议先进行数据预处理。

## 扩展功能建议

- [ ] 添加用户认证和权限管理
- [ ] 支持数据库存储，持久化数据
- [ ] 添加数据可视化图表
- [ ] 支持多文件同时分析
- [ ] 添加数据导出功能
- [ ] 支持更多AI模型（如本地模型）
- [ ] 添加数据清洗和预处理功能

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过GitHub Issues联系。
