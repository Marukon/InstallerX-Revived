#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
from datetime import datetime, timedelta, timezone

def send_text(bot_token: str, chat_id: str, text: str):
    """
    发送纯文本消息到 Telegram
    """
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        data={"chat_id": chat_id, "text": text}
    )
    if response.status_code == 200:
        print("成功发送文本消息")
    else:
        print("文本消息发送失败")
        print(response.text)


def send_file(bot_token: str, chat_id: str, file_path: str):
    """
    使用 Telegram Bot API 上传单个文件
    """
    if not file_path or not os.path.exists(file_path):
        print(f"文件不存在或路径为空: {file_path}")
        return

    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendDocument",
            data={"chat_id": chat_id},
            files={"document": (file_name, f)}
        )
    if response.status_code == 200:
        print(f"成功发送: {file_name}")
    else:
        print(f"发送失败: {file_name}")
        print(response.text)


def main():
    bot_token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")

    if not bot_token or not chat_id:
        print("错误: 请在 GitHub Actions Secrets 中设置 BOT_TOKEN 和 CHAT_ID")
        sys.exit(1)

    # 从命令行参数读取文件路径
    files_to_send = sys.argv[1:]
    if not files_to_send:
        print("没有指定要发送的文件")
        sys.exit(0)

    # ⭐ 在发送文件之前，先发送当前时间
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    send_text(bot_token, chat_id, f"📅 当前时间（UTC+8）：{now}"}")

    # 发送文件
    for file_path in files_to_send:
        send_file(bot_token, chat_id, file_path)


if __name__ == "__main__":
    main()
