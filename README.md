# WebCam 应用

## 项目简介
基于Flask框架的实时摄像头流媒体应用，支持本地访问和ngrok内网穿透。

## 功能特性
- 实时摄像头画面流媒体传输
- 自动错误处理及可视化提示
- 支持ngrok公网访问
- 自适应分辨率设置
- 多线程运行支持

## 环境要求
- Python 3.7+
- 可用摄像头设备

## 安装步骤
```bash
# 克隆仓库
git clone https://github.com/yourusername/webcam-app.git
cd webcam-app

# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 快速启动
```bash
# 运行应用
python app.py

# 访问本地地址
http://localhost:5000
```

## 配置指南
1. 获取ngrok认证令牌：
   - 访问 [ngrok官网](https://dashboard.ngrok.com/get-started/your-authtoken)
   - 创建文件 `.ngrok_token` 并粘贴令牌
2. 启用公网访问：
   ```bash
   # Linux/macOS
   export USE_NGROK=true
   # Windows PowerShell
   $env:USE_NGROK="true"
   ```

## 常见问题
Q: 摄像头无法正常显示
A: 请检查：
1. 摄像头设备连接状态
2. 系统隐私设置中的摄像头权限
3. 尝试更换视频捕获索引值（app.py第33行）

Q: ngrok连接失败
A: 请确认：
1. 已正确配置ngrok令牌
2. 网络防火墙允许ngrok通信
3. 终端能正常访问ngrok服务

## 依赖说明
- OpenCV：视频流处理
- Flask：Web框架
- pyngrok：内网穿透（可选）

## 许可证
[MIT License](LICENSE)