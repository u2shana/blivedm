import aiohttp
import asyncio

# 全局变量
send_key = ""  # 填写Server酱SendKey
url = f"https://sctapi.ftqq.com/{send_key}.send"
session = None  # 复用会话
max_retries = 999  # 最大重试次数
retry_interval = 30  # 重试间隔时间（秒）

async def send(title, content=''):
    """异步发送消息到Server酱，支持失败重试"""
    global session

    payload = {
        "title": title[:32],  # 确保标题不超过限制
        "desp": content
    }

    retry_count = 0
    while retry_count < max_retries:
        try:
            if not session:
                session = aiohttp.ClientSession()  # 创建会话

            async with session.post(url, data=payload) as response:
                response.raise_for_status()
                
                # 处理Server酱的响应格式
                result = await response.json()
                if result.get('code') not in [0, 200]:
                    error_msg = result.get('message', '未知错误')
                    raise Exception(f"[{result.get('code')}] {error_msg}")
                
                return True  # 发送成功，直接返回
        except (aiohttp.ClientError, ValueError, Exception) as e:
            retry_count += 1
            if retry_count >= max_retries:
                raise Exception(f"推送失败，已达到最大重试次数: {str(e)}")
            
            print(f"推送失败，第 {retry_count} 次重试... 错误信息: {str(e)}")
            await asyncio.sleep(retry_interval)  # 等待重试间隔
        except Exception as e:
            raise Exception(f"未知错误: {str(e)}")

async def close_session():
    """关闭会话"""
    global session
    if session:
        await session.close()
