//主要的选项配置
const mainConfig = {
	isDebug: true,						//开启调试，会打印运行中部分日志

	//个人中心配置，其中多数是可以直接在更多功能里直接移除
	removeHomeVip: true,				//个人中心头像旁边的vip样式
	removeHomeCreatorTask: true,		//个人中心创作者中心下方的轮播图

	//微博详情页配置
	removeRelate: true,			//相关推荐
	removeGood: true,			//微博主好物种草
	removeFollow: true,			//关注博主
	modifyMenus: true,			//编辑上下文菜单
	removeRelateItem: true,		//评论区相关内容
	removeRecommendItem: true,	//评论区推荐内容
	removeRewardItem: true,		//微博详情页打赏模块

	removeLiveMedia: true,		//首页顶部直播
	removeNextVideo: true,		//关闭自动播放下一个视频

	removeInterestFriendInTopic: true,		//超话：超话里的好友
	removeInterestTopic: true,				//超话：可能感兴趣的超话
	removeInterestUser: true,				//用户页：可能感兴趣的人

	removeLvZhou: true,					//绿洲模块

	profileSkin1: null,						//用户页：自定义图标1
	profileSkin2: null,						//用户页：自定义图标2
	tabIconVersion: 0,						//配置大于100的数
	tabIconPath: ''							//配置图标路径
}

//菜单配置
const itemMenusConfig = {
	creator_task:false,					//转发任务
	mblog_menus_custom:false,				//寄微博
	mblog_menus_video_later:true,			//可能是稍后再看？没出现过
	mblog_menus_comment_manager:true,		//评论管理
	mblog_menus_avatar_widget:false,		//头像挂件
	mblog_menus_card_bg: false,			//卡片背景
	mblog_menus_long_picture:true,		//生成长图
	mblog_menus_delete:true,				//删除
	mblog_menus_edit:true,				//编辑
	mblog_menus_edit_history:true,		//编辑记录
	mblog_menus_edit_video:true,			//编辑视频
	mblog_menus_sticking:true,			//置顶
	mblog_menus_open_reward:true,			//赞赏
	mblog_menus_novelty:false,			//新鲜事投稿
	mblog_menus_favorite:true,			//收藏
	mblog_menus_promote:true,				//推广
	mblog_menus_modify_visible:true,		//设置分享范围
	mblog_menus_copy_url:true,			//复制链接
	mblog_menus_follow:true,				//关注
	mblog_menus_video_feedback:true,		//播放反馈
	mblog_menus_shield:true,				//屏蔽
	mblog_menus_report:true,				//投诉
	mblog_menus_apeal:true,				//申诉
	mblog_menus_home:true					//返回首页
}


function nobyda() {
	const isQuanX = typeof $task != "undefined";
	const isSurge = typeof $httpClient != "undefined";
	const isRequest = typeof $request != "undefined";
	const notify = (title, subtitle='', message='') => {
		if (isQuanX) $notify(title, subtitle, message)
		if (isSurge) $notification.post(title, subtitle, message);
	}
	const write = (value, key) => {
		if (isQuanX) return $prefs.setValueForKey(value, key);
		if (isSurge) return $persistentStore.write(value, key);
	}
	const read = (key) => {
		if (isQuanX) return $prefs.valueForKey(key);
		if (isSurge) return $persistentStore.read(key);
	}
	const done = (value = {}) => {
		if (isQuanX) return $done(value);
		if (isSurge) isRequest ? $done(value) : $done();
	}

	return {
		isRequest,
		isSurge,
		isQuanX,
		notify,
		write,
		read,
		done
	}
}

let $ = new nobyda();
// $.write(JSON.stringify(isDebug), 'isDebug');
$.write(JSON.stringify(mainConfig), 'mainConfig');
$.write(JSON.stringify(itemMenusConfig), 'itemMenusConfig');
// console.log($.read('isDebug'));
console.log($.read('mainConfig'));
console.log($.read('itemMenusConfig'));
console.log('success');
$.notify('微博自定义配置更改成功');
$.done();
