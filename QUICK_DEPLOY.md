# 🚀 Railway快速部署指南

## 第一步：准备GitHub仓库
✅ 已完成：代码已推送到 `https://github.com/LunaYang1017/studyhard`

## 第二步：注册Railway账户
1. 访问 [Railway官网](https://railway.app/)
2. 点击 "Start a New Project"
3. 使用GitHub账户登录

## 第三步：部署项目
1. 登录后，点击 "Deploy from GitHub repo"
2. 选择您的仓库：`LunaYang1017/studyhard`
3. 点击 "Deploy Now"

## 第四步：配置环境变量
在Railway项目页面，点击 "Variables" 标签，添加以下变量：

```
STEPFUN_API_KEY=5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4
STEPFUN_BASE_URL=https://api.stepfun.com/v1
STEPFUN_MODEL=step-1-8k
SECRET_KEY=your-production-secret-key-change-this-123456
ALLOWED_ORIGINS=https://your-app-name.railway.app,http://localhost:3000
```

## 第五步：等待部署完成
- Railway会自动构建Docker镜像
- 部署时间约3-5分钟
- 完成后会显示域名，类似：`https://your-app-name.railway.app`

## 第六步：测试部署
使用提供的检查脚本：
```bash
python check_deployment.py https://your-app-name.railway.app
```

## 第七步：访问应用
- 健康检查：`https://your-app-name.railway.app/health`
- API文档：`https://your-app-name.railway.app/docs`
- 知识库：`https://your-app-name.railway.app/knowledge-base`

## 常见问题解决

### 1. 部署失败
- 检查环境变量是否正确设置
- 查看Railway日志获取错误信息
- 确保GitHub仓库代码是最新的

### 2. 健康检查失败
- 检查端口配置
- 确认应用启动命令正确
- 查看应用日志

### 3. API调用失败
- 检查CORS配置
- 确认API密钥有效
- 验证域名配置

## 部署成功标志
✅ 健康检查返回200状态码
✅ API文档可以正常访问
✅ 知识库端点响应正常
✅ 可以创建会话和上传文件

## 下一步
部署成功后，您可以：
1. 分享Railway域名给其他人使用
2. 配置自定义域名（可选）
3. 设置自动部署（代码推送时自动更新）

🎉 恭喜！您的考试复习助手现在已经可以在公网上访问了！ 