# 事件订阅示例

以下示例假定已有 `bot = Bot(app_id, app_secret)`。需要在 QQ 开放平台勾选对应事件。

## 单聊消息事件

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/c2c_message_create.html)

```python
@bot.on_event("C2C_MESSAGE_CREATE")
async def on_c2c_message_create(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 单聊消息接收开启

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/c2c_msg_receive.html)

```python
@bot.on_event("C2C_MSG_RECEIVE")
async def on_c2c_msg_receive(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 单聊消息接收关闭

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/c2c_msg_reject.html)

```python
@bot.on_event("C2C_MSG_REJECT")
async def on_c2c_msg_reject(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 子频道创建

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/channel_create.html)

```python
@bot.on_event("CHANNEL_CREATE")
async def on_channel_create(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 子频道删除

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/channel_delete.html)

```python
@bot.on_event("CHANNEL_DELETE")
async def on_channel_delete(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 子频道更新

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/channel_update.html)

```python
@bot.on_event("CHANNEL_UPDATE")
async def on_channel_update(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 用户添加好友

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/friend_add.html)

```python
@bot.on_event("FRIEND_ADD")
async def on_friend_add(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 用户删除好友

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/friend_del.html)

```python
@bot.on_event("FRIEND_DEL")
async def on_friend_del(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 机器人加入群聊

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/group_add_robot.html)

```python
@bot.on_event("GROUP_ADD_ROBOT")
async def on_group_add_robot(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 群@机器人消息

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/group_at_message_create.html)

```python
@bot.on_event("GROUP_AT_MESSAGE_CREATE")
async def on_group_at_message_create(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 机器人退出群聊

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/group_del_robot.html)

```python
@bot.on_event("GROUP_DEL_ROBOT")
async def on_group_del_robot(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 用户申请加群事件

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/group_join_request.html)

```python
@bot.on_event("GROUP_JOIN_REQUEST")
async def on_group_join_request(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 群成员加入

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/group_member_add.html)

```python
@bot.on_event("GROUP_MEMBER_ADD")
async def on_group_member_add(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 群成员退出

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/group_member_remove.html)

```python
@bot.on_event("GROUP_MEMBER_REMOVE")
async def on_group_member_remove(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 群消息（全量模式）

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/group_message_create.html)

```python
@bot.on_event("GROUP_MESSAGE_CREATE")
async def on_group_message_create(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 群聊消息接收开启

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/group_msg_receive.html)

```python
@bot.on_event("GROUP_MSG_RECEIVE")
async def on_group_msg_receive(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 群聊消息接收关闭

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/group_msg_reject.html)

```python
@bot.on_event("GROUP_MSG_REJECT")
async def on_group_msg_reject(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 频道创建

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/guild_create.html)

```python
@bot.on_event("GUILD_CREATE")
async def on_guild_create(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 频道解散

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/guild_delete.html)

```python
@bot.on_event("GUILD_DELETE")
async def on_guild_delete(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 频道更新

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/guild_update.html)

```python
@bot.on_event("GUILD_UPDATE")
async def on_guild_update(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 互动事件

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/interaction_create.html)

```python
@bot.on_event("INTERACTION_CREATE")
async def on_interaction_create(ctx):
    print(ctx.event.type, ctx.event.event_id)
```

## 订阅消息授权状态变更

[官方字段说明](https://bot.q.qq.com/wiki/develop/api-v2/autogen/event/subscribe_message_status.html)

```python
@bot.on_event("SUBSCRIBE_MESSAGE_STATUS")
async def on_subscribe_message_status(ctx):
    print(ctx.event.type, ctx.event.event_id)
```
