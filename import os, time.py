import os, time
from slack_bolt import App

channel_id = os.environ[w1642403489-oli813843]
app = App(token=os.environ["xoxb-2974075862017-3842059675505-whqA4C5qS0hTrVsouN5NFClr"])

def deleteMessage(channel, ts):
    return app.client.chat_delete(
        channel=channel_id,
        ts=ts,
    )

def deleteThreadMessage(channel, thread_ts):
    # https://api.slack.com/methods/conversations.replies
    messages = app.client.conversations_replies(
        channel=channel_id,
        ts = thread_ts,
    )["messages"]

    responses = list()
    # 後ろから順番に削除していく
    for message in reversed(messages):
        responses.append(deleteMessage(
            channel, 
            message["ts"],
        ))
        time.sleep(0.5) # 一応待ちます．
    return responses

def run():
    # https://api.slack.com/methods/conversations.history
    result = app.client.conversations_history(channel=channel_id, limit=1)

    message = result["messages"][0]
    # スレッドに関係したメッセージかどうか
    if "reply_count" in message.keys() or "subtype" in message.keys():
        # thread_tsが親のタイムスタンプ
        return deleteThreadMessage(channel_id, message["thread_ts"])

    # それ以外は通常メッセージなのでそのまま消す
    ts = message["ts"]
    return [deleteMessage(channel_id, ts)]

if __name__ == "__main__":
    responses = run()
    for res in responses:
        print(res)

# スレッドの場合
# $ python3 deleteMessageNow.py
# >> {'ok': True, 'channel': '<channnelID>', 'ts': '<dotted timestamp3>'} 
# >> {'ok': True, 'channel': '<channnelID>', 'ts': '<dotted timestamp2>'} 
# >> {'ok': True, 'channel': '<channnelID>', 'ts': '<dotted timestamp1>'} 