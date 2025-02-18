import requests

class _push:
    def __init__(self):
        # ========================
        # 在这里手动配置参数（二选一）
        # ========================
        self.send_key = ""  # 方式1：填写Server酱SendKey
        self.url = f"https://sctapi.ftqq.com/{self.send_key}.send"               # 方式2：或直接填写完整URL


    def send(self, title, content=''):
        """发送消息到Server酱
        
        Args:
            title: 消息标题（最长32字符）
            content: 消息内容（支持Markdown，最长64K）
            
        Returns:
            bool: 推送是否成功
            
        Raises:
            Exception: 推送失败时抛出包含错误信息的异常
        """
        payload = {
            "title": title[:32],  # 确保标题不超过限制
            "desp": content
        }

        try:
            response = requests.post(self.url, data=payload)
            response.raise_for_status()
            
            # 处理Server酱的响应格式
            result = response.json()
            if result.get('code') not in [0, 200]:
                error_msg = result.get('message', '未知错误')
                raise Exception(f"[{result.get('code')}] {error_msg}")
            
            return True
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        except ValueError:
            raise Exception("服务器返回异常响应格式")

# 全局单例实例
push = _push()
