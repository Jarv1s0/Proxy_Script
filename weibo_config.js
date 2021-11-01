#!name=Weibo
#!desc=Weibo app removes ad.
#!system=ios

[Script]

hostname = api.weibo.cn, mapi.weibo.com, *.uve.weibo.com, new.vip.weibo.cn, %APPEND% api.weibo.cn

# 微博去广告以及去除各部分推广模块 - cherish
^https?://m?api\.weibo\.c(n|om)/2/(cardlist|searchall|page|statuses/(unread_)?friends(/|_)timeline|groups/timeline|statuses/(unread_hot_timeline|extend)|profile/(me|statuses)|video/(community_tab|remind_info|tiny_stream_video_list)|checkin/show|\!/live/media_homelist|comments/build_comments|container/get_item) url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_main.js

# 删除微博开屏广告 - cherish
^https?://(sdk|wb)app\.uve\.weibo\.com(/interface/sdk/sdkad.php|/wbapplua/wbpullad.lua) url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_launch.js

# 自定义tab皮肤
^https://api.weibo.cn/2/!/client/light_skin url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_main.js

# 非会员设置tab皮肤 - cherish
^https://new.vip.weibo.cn/littleskin/preview url script-response-body https://raw.githubusercontent.com/zmqcherish/proxy-script/main/weibo_main.js


// 微博下面的评论
http-response ^https://(api\.weibo\.cn|mapi\.weibo\.com)/2/comments/build_comments\? requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/yjqiang/surge_scripts/main/scripts/weibo/weibo_comment.js

// 微博 推荐 热门/榜单/放映厅… https://api.weibo.cn/2/statuses/unread_hot_timeline?
// 微博 最新微博 https://api.weibo.cn/2/statuses/friends/timeline?
// 视频流（短视频上划，微博继续推荐新视频） https://api.weibo.cn/2/video/tiny_stream_video_list?
// 微博 全部关注 https://api.weibo.cn/2/statuses/unread_friends_timeline?
http-response ^https://(api\.weibo\.cn|mapi\.weibo\.com)/2/(statuses/unread_hot_timeline|statuses/friends/timeline|video/tiny_stream_video_list|statuses/unread_friends_timeline)\? requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/yjqiang/surge_scripts/main/scripts/weibo/weibo_statuses.js

// 发现 搜索 https://api.weibo.cn/2/searchall?
// 超话 帖子/精华/官方 https://api.weibo.cn/2/page?
http-response ^https://(api\.weibo\.cn|mapi\.weibo\.com)/2/(searchall|page)\? requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/yjqiang/surge_scripts/main/scripts/weibo/weibo_cardlist.js

// 发现 热点（这货特殊，有卡片广告） https://api.weibo.cn/2/cardlist?
http-response ^https://(api\.weibo\.cn|mapi\.weibo\.com)/2/cardlist\? requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/yjqiang/surge_scripts/main/scripts/weibo/weibo_cardlist_discover.js

// 每条微博下面 创作者广告共享计划
http-response ^https://(api\.weibo\.cn|mapi\.weibo\.com)/2/statuses/extend\? requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/yjqiang/surge_scripts/main/scripts/weibo/weibo_statuses_extend.js



