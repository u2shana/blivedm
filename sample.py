# -*- coding: utf-8 -*-
import asyncio
import http.cookies
import random
from typing import *

import aiohttp

import blivedm
import blivedm.models.web as web_models
from datetime import datetime
import os

# 直播间ID的取值看直播间URL
TEST_ROOM_IDS = [
    1376666,
]

# 这里填一个已登录账号的cookie的SESSDATA字段的值。不填也可以连接，但是收到弹幕的用户名会打码，UID会变成0
SESSDATA = ''

session: Optional[aiohttp.ClientSession] = None

log_file_path = os.path.join(os.getcwd(), 'logs', 'gift.log')

def log_message(message):
    full_message = f"{message}"
    print(full_message)  # 打印到控制台
    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:  # 以追加模式打开文件
            log_file.write(full_message + '\n')  # 写入消息并换行
    except IOError as e:
        print(f"写入日志失败: {e}")

async def main():
    init_session()
    try:
        await run_single_client()
        await run_multi_clients()
    finally:
        await session.close()
	
def s_timestamp(timestamp: int) -> str:
    # 创建 datetime 对象
    readable_time = datetime.fromtimestamp(timestamp)
    # 格式化为字符串，保留到毫秒
    s_time = readable_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return s_time
	
def init_session():
    cookies = http.cookies.SimpleCookie()
    cookies['SESSDATA'] = SESSDATA
    cookies['SESSDATA']['domain'] = 'bilibili.com'

    global session
    session = aiohttp.ClientSession()
    session.cookie_jar.update_cookies(cookies)

async def run_single_client():
    """
    演示监听一个直播间
    """
    room_id = random.choice(TEST_ROOM_IDS)
    client = blivedm.BLiveClient(room_id, session=session)
    handler = MyHandler()
    client.set_handler(handler)

    client.start()
    try:
        # 演示5秒后停止
        await asyncio.sleep(5)
        client.stop()

        await client.join()
    finally:
        await client.stop_and_close()

async def run_multi_clients():
    """
    演示同时监听多个直播间
    """
    clients = [blivedm.BLiveClient(room_id, session=session) for room_id in TEST_ROOM_IDS]
    handler = MyHandler()
    for client in clients:
        client.set_handler(handler)
        client.start()

    try:
        await asyncio.gather(*(
            client.join() for client in clients
        ))
    finally:
        await asyncio.gather(*(
            client.stop_and_close() for client in clients
        ))

class MyHandler(blivedm.BaseHandler):
    def _on_heartbeat(self, client: blivedm.BLiveClient, message: web_models.HeartbeatMessage):
        pass
		
    def _on_danmaku(self, client: blivedm.BLiveClient, message: web_models.DanmakuMessage):
        log_message(f'[{s_timestamp(message.timestamp / 1000.0)}] [{client.room_id}] uid="{message.uid}" user="{message.uname}"：{message.msg}')
		
    def _on_gift(self, client: blivedm.BLiveClient, message: web_models.GiftMessage):
        cointype = "金" if message.coin_type == "gold" else "银"
        log_message(f'<gift ts=" "[{s_timestamp(message.timestamp)}] [{client.room_id}] uid="{message.uid}]" user="{message.uname}" giftname="{message.gift_name}" giftcount="{message.num}" cointype="{cointype}瓜子" price="{message.price}">')

    def _on_user_toast_v2(self, client: blivedm.BLiveClient, message: web_models.UserToastV2Message):
        log_message(f'<toast ts=" "[{s_timestamp(message.start_time)}] [{client.room_id}] uid="{message.uid}" user="{message.username}" unit="{message.unit}" count="{message.num}" price="{message.price}" level="{message.guard_level}" {message.toast_msg}>')
		
    def _on_super_chat(self, client: blivedm.BLiveClient, message: web_models.SuperChatMessage):
        log_message(f'<sc ts=" "[{s_timestamp(message.start_time)}] [{client.room_id}] time="{message.time}" price="{message.price * 1000}" uid="{message.uid}" user="{message.uname}"： {message.message}>')
 
    # def _on_interact_word(self, client: blivedm.BLiveClient, message: web_models.InteractWordMessage):
    #     if message.msg_type == 1:
    #         print(f'[{client.room_id}] {message.username} 进入房间')

if __name__ == '__main__':
    asyncio.run(main())
