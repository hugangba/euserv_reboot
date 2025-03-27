"""
Python script for automated monitoring and recovery of IPv6-based Euserv servers. Automatically performs server reboot via official API when unreachable status is detected.
Feedback:https://github.com/hugangba/euserv_reboot
"""
import requests
import os
import platform
import subprocess
from typing import Optional, Dict

# 配置信息（必须配置以下参数）
EMAIL = os.getenv("EUSERV_EMAIL", "your@email.com")        # 替换为自己的邮箱
PASSWORD = os.getenv("EUSERV_PASSWORD", "your_password")        # 替换为自己的密码
ORD_NO = os.getenv("EUSERV_ORD_NO", "your_order_number")                   # 替换为自己的订单号
IPV6_ADDRESS = os.getenv("EUSERV_IPV6", "2001:180:6:1::1")          # 必须配置服务器的IPv6地址

BASE_URL = "https://support.euserv.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

class EuservAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.sess_id: Optional[str] = None
        self.ipv6_address = IPV6_ADDRESS

        # 基础格式验证
        if ":" not in self.ipv6_address or len(self.ipv6_address) < 4:
            raise ValueError("IPv6地址格式无效")

    def _handle_response(self, response: requests.Response) -> Dict:

        try:
            data = response.json()
        except requests.JSONDecodeError:
            raise ValueError(f"响应解析失败，原始内容：{response.text[:200]}")

        if response.status_code != 200:
            raise Exception(f"HTTP错误 ({response.status_code}): {data.get('message', '未知错误')}")

        if data.get("code") != "100":
            raise Exception(f"业务错误: {data.get('message', '未知错误')}")

        return data

    def check_connectivity(self) -> bool:
        """优先执行的连通性检查"""
        print("\n[初始检查] 正在测试IPv6连通性...")
        os_type = platform.system().lower()
        
        # 构造ping命令
        ping_args = {
            "timeout": 5,
            "count": 4
        }
        
        command = [
            "ping", "-6", "-n", str(ping_args["count"]),
            "-w", str(ping_args["timeout"] * 1000), self.ipv6_address
        ] if os_type == "windows" else [
            "ping6" if os_type == "darwin" else "ping",
            "-c", str(ping_args["count"]),
            "-W", str(ping_args["timeout"]), self.ipv6_address
        ]

        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=ping_args["timeout"] * ping_args["count"] + 2
            )
            success = result.returncode == 0
            print(f"✅ 连通性测试成功" if success else "⛔ 无法连接到服务器")
            return success
        except Exception as e:
            print(f"⚠️ 检测异常: {str(e)}")
            return False

    def get_sess_id(self) -> str:
        """获取会话ID"""
        params = {"method": "json"}
        response = self.session.get(BASE_URL, params=params)
        data = self._handle_response(response)
        
        if not (sess_id := data.get("result", {}).get("sess_id", {}).get("value")):
            raise ValueError("获取会话ID失败")
        
        self.sess_id = sess_id
        return sess_id

    def login(self) -> Dict:
        """用户登录"""
        params = {
            "subaction": "login",
            "method": "json",
            "sess_id": self.sess_id,
            "email": EMAIL,
            "password": PASSWORD,
            "ord_no": ORD_NO,
        }
        response = self.session.get(BASE_URL, params=params)
        return self._handle_response(response)

    def reset_server(self) -> Dict:
        """执行服务器重启"""
        params = {
            "subaction": "kc2_server_reset_do_reset",
            "method": "json",
            "sess_id": self.sess_id,
            "ord_no": ORD_NO,
        }
        response = self.session.get(BASE_URL, params=params)
        return self._handle_response(response)

def main():
    try:
        print("正在初始化服务客户端...")
        api = EuservAPI()
        print(f"ℹ️ 配置地址: {api.ipv6_address}")

        # 第一步：立即检查连通性
        if api.check_connectivity():
            print("\n服务器状态正常，无需其他操作")
            return

        # 仅在需要时执行后续操作
        print("\n开始执行恢复流程...")
        
        print("\n步骤1/3 获取会话ID...")
        api.get_sess_id()
        print(f"✅ 会话ID获取成功")

        print("\n步骤2/3 账号登录...")
        login_resp = api.login()
        print(f"✅ 登录成功 | 消息: {login_resp.get('message')}")

        print("\n步骤3/3 执行服务器重启...")
        reset_resp = api.reset_server()
        print(f"✅ 重启指令发送成功 | 状态: {reset_resp.get('message')}")

    except Exception as e:
        print(f"\n❌ 流程异常终止: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
