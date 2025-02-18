# blivedm

Python获取bilibili直播弹幕的库，使用WebSocket协议，支持web端和B站直播开放平台两种接口

[协议解释](https://open-live.bilibili.com/document/657d8e34-f926-a133-16c0-300c1afc6e6b)

根据个人需求基于blivedm原版修改，格式化输出信息流，~~使用user_toast代替guard_buy~~

**~~只改了web端。~~**
增加房间连接出错后server酱推送功能，修改push文件里面的sendkey

## 使用说明

1. 需要Python 3.8及以上版本
2. 安装依赖

    ```sh
    pip install -r requirements.txt
    ```

3. web端例程在[sample.py](./sample.py)，B站直播开放平台例程在[open_live_sample.py](./open_live_sample.py)
