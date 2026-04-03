# 🚀 Render.com 部署操作指南

## 📋 部署前检查清单

- ✅ GitHub仓库已创建：`https://github.com/FrogSky/auto-excel`
- ✅ 代码已推送到main分支
- ✅ 部署配置文件已准备：
  - `render.yaml` - Render部署配置
  - `Procfile` - 启动命令配置
  - `requirements.txt` - Python依赖
  - `app.py` - Flask应用（已配置生产环境）

---

## 🎯 第一步：注册Render账号

1. 访问 [https://render.com](https://render.com)
2. 点击右上角的 "Sign Up"
3. 选择 "Sign up with GitHub"
4. 使用GitHub账号登录并授权
5. 完成邮箱验证（如需要）

**注意：** Render需要信用卡验证，但免费套餐不会扣费。

---

## 🚀 第二步：创建Web服务

### 2.1 开始创建

1. 登录Render后，点击右上角的 "New +"
2. 选择 "Web Service"

### 2.2 连接GitHub仓库

1. 在 "Connect a repository" 部分
2. 搜索并选择 `FrogSky/auto-excel` 仓库
3. 点击 "Connect" 按钮

### 2.3 配置服务基本信息

**Name（服务名称）：**
- 输入：`auto-excel`
- 这将决定您的访问URL：`https://auto-excel.onrender.com`

**Region（区域）：**
- 选择：`Singapore`（新加坡）或 `Oregon (US West)`
- 建议选择离您最近的区域以获得更好的性能

**Branch（分支）：**
- 选择：`main`

### 2.4 配置构建和运行

**Runtime（运行时）：**
- 选择：`Python 3`

**Build Command（构建命令）：**
```
pip install -r requirements.txt
```

**Start Command（启动命令）：**
```
gunicorn app:app
```

### 2.5 配置环境变量

在 "Environment Variables" 部分添加以下变量：

| Key | Value | 说明 |
|-----|-------|------|
| `PYTHON_VERSION` | `3.13.0` | Python版本 |
| `PORT` | `10000` | Render默认端口 |
| `FLASK_ENV` | `production` | Flask环境模式 |

**可选：如果您有OpenAI API密钥**
| Key | Value | 说明 |
|-----|-------|------|
| `OPENAI_API_KEY` | `您的API密钥` | OpenAI API密钥 |

### 2.6 配置实例类型

**Instance Type（实例类型）：**
- 选择：`Free`（免费套餐）

**免费套餐限制：**
- 750小时/月运行时间
- 512MB RAM
- 0.1 CPU
- 15分钟无活动会休眠
- 首次访问需要30-60秒唤醒

### 2.7 配置持久化存储（重要）

由于应用需要上传文件，建议配置持久化存储：

1. 在服务配置页面，找到 "Disk" 部分
2. 点击 "Add Disk"
3. 配置如下：
   - **Name**: `uploads`
   - **Mount Path**: `/opt/render/project/uploads`
   - **Size**: `1 GB`（免费套餐）

---

## 🎉 第三步：部署应用

1. 检查所有配置是否正确
2. 点击底部的 "Create Web Service" 按钮
3. 等待构建和部署完成（通常需要2-5分钟）

### 部署过程

您会看到以下阶段：
1. **Cloning** - 克隆代码仓库
2. **Building** - 安装依赖
3. **Deploying** - 启动应用
4. **Live** - 部署成功

### 查看部署日志

- 在服务页面点击 "Logs" 标签
- 可以实时查看部署进度和错误信息
- 如果部署失败，检查日志中的错误信息

---

## 🔗 第四步：访问应用

部署成功后，您会获得一个公网URL：

```
https://auto-excel.onrender.com
```

### 测试访问

1. 点击服务页面顶部的URL
2. 应该能看到Excel数据问答系统的首页
3. 尝试上传Excel文件测试功能

### 健康检查

访问健康检查端点：
```
https://auto-excel.onrender.com/api/health
```

应该返回类似：
```json
{
  "status": "healthy",
  "uploaded_files_count": 0,
  "timestamp": "2024-01-01T00:00:00.000000"
}
```

---

## ⚙️ 第五步：配置自动部署

Render支持自动部署，当您推送代码到GitHub时会自动重新部署：

1. 进入服务设置页面
2. 点击 "Settings" 标签
3. 找到 "Auto-Deploy" 部分
4. 确认已启用（默认启用）
5. 可以配置部署分支（默认为main）

---

## 📊 监控和维护

### 查看日志

- **实时日志**: 在服务页面点击 "Logs"
- **历史日志**: 可以查看过去的日志记录
- **错误日志**: 重点关注ERROR级别的日志

### 性能监控

- **Metrics**: 查看CPU、内存使用情况
- **Response Time**: 监控响应时间
- **Request Count**: 查看请求统计

### 保持应用活跃

免费套餐15分钟无活动会休眠，可以使用以下方法保持活跃：

1. **使用UptimeRobot**（免费监控服务）
   - 访问 https://uptimerobot.com
   - 添加监控：`https://auto-excel.onrender.com/api/health`
   - 设置每5分钟检查一次

2. **使用其他监控服务**
   - Pingdom
   - StatusCake
   - Better Uptime

---

## 🛠️ 故障排除

### 问题1：部署失败

**可能原因：**
- 依赖安装失败
- 端口配置错误
- 环境变量缺失

**解决方法：**
1. 检查 "Logs" 中的错误信息
2. 确认 `requirements.txt` 中的依赖版本正确
3. 检查环境变量是否配置正确

### 问题2：应用无法访问

**可能原因：**
- 应用正在休眠
- 部署未完成
- 端口配置错误

**解决方法：**
1. 等待30-60秒让应用从休眠中唤醒
2. 检查部署状态是否为 "Live"
3. 确认 `PORT` 环境变量设置为 `10000`

### 问题3：文件上传失败

**可能原因：**
- 持久化存储未配置
- 文件大小超过限制
- 权限问题

**解决方法：**
1. 确认已配置Disk持久化存储
2. 检查文件大小是否超过16MB
3. 查看日志中的详细错误信息

### 问题4：OpenAI API不工作

**可能原因：**
- API密钥未配置
- API密钥无效
- 配额用尽

**解决方法：**
1. 在环境变量中添加 `OPENAI_API_KEY`
2. 确认API密钥有效且有足够配额
3. 检查OpenAI账户状态

---

## 🎨 自定义域名（可选）

如果您想使用自定义域名：

1. 在服务页面，点击 "Domains" 标签
2. 点击 "Add Domain"
3. 输入您的域名（如 `excel.yourdomain.com`）
4. 按照提示配置DNS记录：
   - **类型**: CNAME
   - **名称**: excel
   - **值**: auto-excel.onrender.com

---

## 📈 升级到付费套餐（可选）

如果免费套餐无法满足需求：

1. 进入服务设置
2. 点击 "Change Plan"
3. 选择合适的套餐：
   - **Starter**: $7/月，512MB RAM，0.5 CPU
   - **Standard**: $25/月，2GB RAM，1 CPU
   - **Pro**: $100/月，8GB RAM，4 CPU

付费套餐优势：
- 更快的响应速度
- 更多资源
- 不会休眠
- 更好的性能

---

## 📞 技术支持

如果遇到问题：

1. **查看Render文档**: https://render.com/docs
2. **查看项目GitHub**: https://github.com/FrogSky/auto-excel
3. **查看部署日志**: 在Render控制台中查看
4. **联系Render支持**: support@render.com

---

## 🎉 部署完成！

恭喜！您的Excel数据问答系统已成功部署到公网！

**访问地址：** `https://auto-excel.onrender.com`

**GitHub仓库：** `https://github.com/FrogSky/auto-excel`

现在任何人都可以通过公网访问您的Excel数据问答系统了！

---

## 📝 后续维护建议

1. **定期更新依赖**: 保持 `requirements.txt` 中的依赖版本最新
2. **监控应用状态**: 定期检查日志和性能指标
3. **备份数据**: 重要数据定期备份
4. **安全更新**: 及时更新安全补丁
5. **用户反馈**: 收集用户反馈并持续改进

---

**部署日期：** 2024年
**部署版本：** v1.0
**部署平台：** Render.com
**服务状态：** 🟢 运行中