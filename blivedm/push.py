import aiohttp
import asyncio
from datetime import datetime

class _push:
    def __init__(self):
        self.send_key = ""  # 填写Server酱SendKey
        self.url = f"https://sctapi.ftqq.com/{self.send_key}.send"
        self.session = None  # 复用会话
        self.max_retries = 999  # 最大重试次数
        self.retry_interval = 30  # 重试间隔时间（秒）

    async def send(self, title, content=''):
        """异步发送消息到Server酱，支持失败重试"""
        payload = {
            "title": title[:32],  # 确保标题不超过限制
            "desp": content
        }

        retry_count = 0
        while retry_count < self.max_retries:
            try:
                if not self.session:
                    self.session = aiohttp.ClientSession()  # 创建会话

                async with self.session.post(self.url, data=payload) as response:
                    response.raise_for_status()
                    
                    # 处理Server酱的响应格式
                    result = await response.json()
                    if result.get('code') not in [0, 200]:
                        error_msg = result.get('message', '未知错误')
                        raise Exception(f"[{result.get('code')}] {error_msg}")
                    
                    return True  # 发送成功，直接返回
            except (aiohttp.ClientError, ValueError, Exception) as e:
                retry_count += 1
                if retry_count >= self.max_retries:
                    raise Exception(f"推送失败，已达到最大重试次数: {str(e)}")
                
                print(f"推送失败，第 {retry_count} 次重试... 错误信息: {str(e)}")
                await asyncio.sleep(self.retry_interval)  # 等待重试间隔
            except Exception as e:
                raise Exception(f"未知错误: {str(e)}")

    async def close(self):
        """关闭会话"""
        if self.session:
            await self.session.close()

# 全局单例实例
push = _push()