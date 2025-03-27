# Euserv IPv6 服务器管理器 / Euserv IPv6 Server Manager

[中文](#中文文档) | [English](#English-Documentation)

---

## 中文文档

### 项目描述 📌
用于自动监控和恢复基于IPv6的Euserv服务器的Python脚本。当检测到服务器不可达时，自动通过官方API执行重启操作。

### 主要功能 🛠️
- ✅ 优先执行IPv6连通性检查（支持Windows/Linux/macOS）
- 🔄 自动登录Euserv管理后台
- ⚡ 一键式服务器重启操作
- 📊 详细的执行状态输出

### 先决条件 ⚙️
- Python 3.8+
- requests 库
- 有效的Euserv账户和服务订单

### 编辑环境变量：
EUSERV_EMAIL="your_email@example.com"
EUSERV_PASSWORD="your_password"
EUSERV_ORD_NO="your_order_number"
EUSERV_IPV6="2001:db8::1"  # 需替换为实际地址

### 执行示例 📝
正在初始化服务客户端...
ℹ️ 配置地址: 2001:db8::1

[初始检查] 正在测试IPv6连通性...
⛔ 无法连接到服务器

开始执行恢复流程...

步骤1/3 获取会话ID...
✅ 会话ID获取成功

步骤2/3 账号登录...
✅ 登录成功 | 消息: Login successful

步骤3/3 执行服务器重启...
✅ 重启指令发送成功 | 状态: Reset initiated

### 注意事项 ⚠️
IPv6地址必须符合RFC 4291格式规范
建议配置API访问频率限制（默认不限制）
账户信息以环境变量形式存储，请勿提交至版本控制系统
推荐通过cron或Systemd配置定时任务（如每15分钟执行一次）

## English-Documentation
### Project Description 📌
Python script for automated monitoring and recovery of IPv6-based Euserv servers. Automatically performs server reboot via official API when unreachable status is detected.

### Key Features 🛠️
✅ Priority IPv6 connectivity check (Supports Windows/Linux/macOS)
🔄 Automatic Euserv dashboard login
⚡ One-click server reboot
📊 Detailed execution status output

### Prerequisites ⚙️
Python 3.8+
requests library
Active Euserv account and service order

### Edit environment variables:
EUSERV_EMAIL="your_email@example.com"
EUSERV_PASSWORD="your_password"
EUSERV_ORD_NO="your_order_number"
EUSERV_IPV6="2001:db8::1"  # Replace with actual address

### Execution Example 📝
Initializing service client...
ℹ️ Configured address: 2001:db8::1

[Initial Check] Testing IPv6 connectivity...
⛔ Server unreachable detected

Initiating recovery workflow...

Step 1/3 Obtaining session ID...
✅ Session ID acquired successfully

Step 2/3 Account login...
✅ Login successful | Message: Login successful

Step 3/3 Executing server reboot...
✅ Reboot command sent | Status: Reset initiated

### Important Notes ⚠️
IPv6 address must comply with RFC 4291 format
Recommend configuring API rate limits (disabled by default)
Store credentials in environment variables - DO NOT commit to VCS
Suggest setting up cron/Systemd scheduled tasks (e.g., every 15 minutes)
贡献指南 / Contribution
欢迎提交Issue或PR：
📮 Report issues: New Issue
💻 Code contributions: Fork & PR

许可证 / License
MIT License © 2025 hugangba
[New Issue]: https://github.com/hugangba/euserv_reboot/issues
