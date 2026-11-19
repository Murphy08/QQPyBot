# REST 接口目录

每个调用均支持 `query` 和 `json_body` 参数。按官方说明填写请求体。

## 删除子频道

`DELETE /channels/{channel_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/channels_channel_id.delete.html)

```python
await bot.api.call('channels_channel_id_delete', channel_id='你的 channel_id')
```

## 获取子频道详情

`GET /channels/{channel_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/channels_channel_id.get.html)

```python
await bot.api.call('channels_channel_id_get', channel_id='你的 channel_id')
```

## 修改子频道

`PATCH /channels/{channel_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/channels_channel_id.patch.html)

```python
await bot.api.call('channels_channel_id_patch', channel_id='你的 channel_id', json_body=body)
```

## 获取通用 WSS 接入点

`GET /gateway`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/gateway.get.html)

```python
await bot.api.call('gateway_get')
```

## 获取子频道列表

`GET /guilds/{guild_id}/channels`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/guilds_guild_id_channels.get.html)

```python
await bot.api.call('guilds_guild_id_channels_get', guild_id='你的 guild_id')
```

## 创建子频道

`POST /guilds/{guild_id}/channels`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/guilds_guild_id_channels.post.html)

```python
await bot.api.call('guilds_guild_id_channels_post', guild_id='你的 guild_id', json_body=body)
```

## 获取频道详情

`GET /guilds/{guild_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/guilds_guild_id.get.html)

```python
await bot.api.call('guilds_guild_id_get', guild_id='你的 guild_id')
```

## 互动事件响应

`PUT /interactions/{interaction_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/interactions_interaction_id.put.html)

```python
await bot.api.call('interactions_interaction_id_put', interaction_id='你的 interaction_id', json_body=body)
```

## 获取机器人详情

`GET /users/@me`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/users_me.get.html)

```python
await bot.api.call('users_me_get')
```

## 获取机器人频道列表

`GET /users/@me/guilds`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/users_me_guilds.get.html)

```python
await bot.api.call('users_me_guilds_get')
```

## 生成分享链接

`POST /v2/generate_url_link`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_generate_url_link.post.html)

```python
await bot.api.call('v2_generate_url_link_post', json_body=body)
```

## 群聊分片上传完成

`POST /v2/groups/{group_id}/upload_part_finish`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_id_upload_part_finish.post.html)

```python
await bot.api.call('v2_groups_group_id_upload_part_finish_post', group_id='你的 group_id', json_body=body)
```

## 群聊富媒体预上传

`POST /v2/groups/{group_id}/upload_prepare`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_id_upload_prepare.post.html)

```python
await bot.api.call('v2_groups_group_id_upload_prepare_post', group_id='你的 group_id', json_body=body)
```

## 入群申请审批

`POST /v2/groups/{group_openid}/approval_join_request/{member_openid}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_approval_join_request_member_openid.post.html)

```python
await bot.api.call('v2_groups_group_openid_approval_join_request_member_openid_post', group_openid='你的 group_openid', member_openid='你的 member_openid', json_body=body)
```

## 群成员批量移除

`POST /v2/groups/{group_openid}/batch_remove_members`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_batch_remove_members.post.html)

```python
await bot.api.call('v2_groups_group_openid_batch_remove_members_post', group_openid='你的 group_openid', json_body=body)
```

## 获取机器人群内状态

`GET /v2/groups/{group_openid}/bot_state`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_bot_state.get.html)

```python
await bot.api.call('v2_groups_group_openid_bot_state_get', group_openid='你的 group_openid')
```

## 群聊富媒体上传

`POST /v2/groups/{group_openid}/files`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_files.post.html)

```python
await bot.api.call('v2_groups_group_openid_files_post', group_openid='你的 group_openid', json_body=body)
```

## 获取群基本信息

`GET /v2/groups/{group_openid}/info`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_info.get.html)

```python
await bot.api.call('v2_groups_group_openid_info_get', group_openid='你的 group_openid')
```

## 入群申请列表拉取

`GET /v2/groups/{group_openid}/join_request_list`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_join_request_list.get.html)

```python
await bot.api.call('v2_groups_group_openid_join_request_list_get', group_openid='你的 group_openid')
```

## 群黑名单查询

`GET /v2/groups/{group_openid}/member_blacklist`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_member_blacklist.get.html)

```python
await bot.api.call('v2_groups_group_openid_member_blacklist_get', group_openid='你的 group_openid')
```

## 群黑名单操作

`POST /v2/groups/{group_openid}/member_blacklist`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_member_blacklist.post.html)

```python
await bot.api.call('v2_groups_group_openid_member_blacklist_post', group_openid='你的 group_openid', json_body=body)
```

## 获取群成员列表

`GET /v2/groups/{group_openid}/members`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_members.get.html)

```python
await bot.api.call('v2_groups_group_openid_members_get', group_openid='你的 group_openid')
```

## 获取群成员信息

`GET /v2/groups/{group_openid}/members/{member_openid}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_members_member_openid.get.html)

```python
await bot.api.call('v2_groups_group_openid_members_member_openid_get', group_openid='你的 group_openid', member_openid='你的 member_openid')
```

## 撤回群聊消息

`DELETE /v2/groups/{group_openid}/messages/{message_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_messages_message_id.delete.html)

```python
await bot.api.call('v2_groups_group_openid_messages_message_id_delete', group_openid='你的 group_openid', message_id='你的 message_id')
```

## 发送群聊消息

`POST /v2/groups/{group_openid}/messages`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_messages.post.html)

```python
await bot.api.call('v2_groups_group_openid_messages_post', group_openid='你的 group_openid', json_body=body)
```

## 查询群禁言状态

`GET /v2/groups/{group_openid}/restrict_chat_setting`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_restrict_chat_setting.get.html)

```python
await bot.api.call('v2_groups_group_openid_restrict_chat_setting_get', group_openid='你的 group_openid')
```

## 设置群成员禁言

`POST /v2/groups/{group_openid}/restrict_chat_setting`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_group_openid_restrict_chat_setting.post.html)

```python
await bot.api.call('v2_groups_group_openid_restrict_chat_setting_post', group_openid='你的 group_openid', json_body=body)
```

## 查询入群自动审批策略列表

`GET /v2/groups/join_approval_strategy`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_join_approval_strategy.get.html)

```python
await bot.api.call('v2_groups_join_approval_strategy_get')
```

## 创建入群自动审批策略

`POST /v2/groups/join_approval_strategy`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_join_approval_strategy.post.html)

```python
await bot.api.call('v2_groups_join_approval_strategy_post', json_body=body)
```

## 删除入群自动审批策略

`DELETE /v2/groups/join_approval_strategy/{strategy_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_join_approval_strategy_strategy_id.delete.html)

```python
await bot.api.call('v2_groups_join_approval_strategy_strategy_id_delete', strategy_id='你的 strategy_id')
```

## 执行入群自动审批策略

`POST /v2/groups/join_approval_strategy/{strategy_id}/execute`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_join_approval_strategy_strategy_id_execute.post.html)

```python
await bot.api.call('v2_groups_join_approval_strategy_strategy_id_execute_post', strategy_id='你的 strategy_id', json_body=body)
```

## 修改入群自动审批策略

`PATCH /v2/groups/join_approval_strategy/{strategy_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_join_approval_strategy_strategy_id.patch.html)

```python
await bot.api.call('v2_groups_join_approval_strategy_strategy_id_patch', strategy_id='你的 strategy_id', json_body=body)
```

## 修改入群自动审批策略的白名单号码

`POST /v2/groups/join_approval_strategy/{strategy_id}/whitelist_users`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_groups_join_approval_strategy_strategy_id_whitelist_users.post.html)

```python
await bot.api.call('v2_groups_join_approval_strategy_strategy_id_whitelist_users_post', strategy_id='你的 strategy_id', json_body=body)
```

## 查询全局自定义菜单

`GET /v2/menu`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_menu.get.html)

```python
await bot.api.call('v2_menu_get')
```

## 修改全局自定义菜单

`PUT /v2/menu`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_menu.put.html)

```python
await bot.api.call('v2_menu_put', json_body=body)
```

## 查询指令面板列表

`GET /v2/panels`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_panels.get.html)

```python
await bot.api.call('v2_panels_get')
```

## 删除指令面板

`DELETE /v2/panels/{panel_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_panels_panel_id.delete.html)

```python
await bot.api.call('v2_panels_panel_id_delete', panel_id='你的 panel_id')
```

## 查询指令面板详情

`GET /v2/panels/{panel_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_panels_panel_id.get.html)

```python
await bot.api.call('v2_panels_panel_id_get', panel_id='你的 panel_id')
```

## 修改指令面板

`PUT /v2/panels/{panel_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_panels_panel_id.put.html)

```python
await bot.api.call('v2_panels_panel_id_put', panel_id='你的 panel_id', json_body=body)
```

## 修改指令面板关联对象

`PUT /v2/panels/{panel_id}/target`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_panels_panel_id_target.put.html)

```python
await bot.api.call('v2_panels_panel_id_target_put', panel_id='你的 panel_id', json_body=body)
```

## 创建指令面板

`POST /v2/panels`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_panels.post.html)

```python
await bot.api.call('v2_panels_post', json_body=body)
```

## 单聊分片上传完成

`POST /v2/users/{user_id}/upload_part_finish`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_users_user_id_upload_part_finish.post.html)

```python
await bot.api.call('v2_users_user_id_upload_part_finish_post', user_id='你的 user_id', json_body=body)
```

## 单聊富媒体预上传

`POST /v2/users/{user_id}/upload_prepare`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_users_user_id_upload_prepare.post.html)

```python
await bot.api.call('v2_users_user_id_upload_prepare_post', user_id='你的 user_id', json_body=body)
```

## 单聊富媒体上传

`POST /v2/users/{user_openid}/files`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_users_user_openid_files.post.html)

```python
await bot.api.call('v2_users_user_openid_files_post', user_openid='你的 user_openid', json_body=body)
```

## 获取用户基本信息

`GET /v2/users/{user_openid}/info`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_users_user_openid_info.get.html)

```python
await bot.api.call('v2_users_user_openid_info_get', user_openid='你的 user_openid')
```

## 撤回单聊消息

`DELETE /v2/users/{user_openid}/messages/{message_id}`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_users_user_openid_messages_message_id.delete.html)

```python
await bot.api.call('v2_users_user_openid_messages_message_id_delete', user_openid='你的 user_openid', message_id='你的 message_id')
```

## 发送单聊消息

`POST /v2/users/{user_openid}/messages`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_users_user_openid_messages.post.html)

```python
await bot.api.call('v2_users_user_openid_messages_post', user_openid='你的 user_openid', json_body=body)
```

## 流式发送单聊消息

`POST /v2/users/{user_openid}/stream_messages`

[官方请求和响应字段](https://bot.q.qq.com/wiki/develop/api-v2/autogen/api/v2_users_user_openid_stream_messages.post.html)

```python
await bot.api.call('v2_users_user_openid_stream_messages_post', user_openid='你的 user_openid', json_body=body)
```
