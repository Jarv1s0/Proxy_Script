const version = 'v0106.1';

let $ = new nobyda();
let storeMainConfig = $.read('mainConfig');
let storeItemMenusConfig = $.read('itemMenusConfig');

//主要的选项配置
const mainConfig = storeMainConfig ? JSON.parse(storeMainConfig) : {
	isDebug: false,						//开启调试，会打印运行中部分日志
	//个人中心配置，其中多数是可以直接在更多功能里直接移除
	removeHomeVip: true,				//个人中心头像旁边的vip样式
	removeHomeCreatorTask: true,		//个人中心创作者中心下方的轮播图

	//微博详情页配置
	removeRelate: true,			//相关推荐
	removeGood: true,			//微博主好物种草
	removeFollow: true,			//关注博主
	modifyMenus: true,			//编辑上下文菜单
	removeRelateItem: true,	//评论区相关内容
	removeRecommendItem: true,	//评论区推荐内容
	removeRewardItem: true,	//微博详情页打赏模块

	removeLiveMedia: true,		//首页顶部直播
	removeNextVideo: true,					//关闭自动播放下一个视频

	removeInterestFriendInTopic: true,		//超话：超话里的好友
	removeInterestTopic: true,				//超话：可能感兴趣的超话 + 好友关注
	removeInterestUser: true,				//用户页：可能感兴趣的人

	removeLvZhou: true,					//绿洲模块

	// profileSkin1: ["https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaingvoj6046046dg802.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaiuoxtj6046046dga02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaiytuyj60460463yv02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaj19hvj6046046aac02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaj5ka0j6046046jrp02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeaj9jfmj6046046dg502.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajd0hfj60460463yu02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajfce5j6046046wet02.jpg"],	//用户页：自定义 我的相册 - 客服 8个图标（需要8项），如果不需要设置为profileSkin1: null
	// profileSkin2: ["https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajhmrnj6046046jro02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajmgs0j60460460t102.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajp9uuj6046046jrp02.jpg","https://wx2.sinaimg.cn/large/006Y6guWly1gvjeajrwrwj6046046dg102.jpg"],		//用户页：自定义 创作首页 - 任务中心 4个图标（需要4项），如果不需要设置为profileSkin2: null

	profileSkin1: ["http://ww4.sinaimg.cn/mw690/acf865f8ly1geywm0xiz9g2074074tbk.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywm0l1jsg2074074ab7.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywm0f40qg2074074myw.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywm08lc7g2074074q5v.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywlzuuo5g2074074n01.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywlzl7oqg207407476m.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywlzawwmg207407441d.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywlyvqu3g2074074goe.gif"],
	profileSkin2: ["http://ww4.sinaimg.cn/mw690/acf865f8ly1geywluvq88g2074074gol.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywlu5xujg2074074gok.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywltdtcgg207407477b.gif","http://ww4.sinaimg.cn/mw690/acf865f8ly1geywlt2k73g2074074dhg.gif"],

	tabIconVersion: 10,	//配置大于100的数
	tabIconPath: "http://r1j12u5w9.hn-bkt.clouddn.com/skin-hebe1.zip",	//配置图标路径
}


//菜单配置
const itemMenusConfig = storeItemMenusConfig ? JSON.parse(storeItemMenusConfig) : {
	creator_task:true,					//转发任务
	mblog_menus_custom:true,				//寄微博
	mblog_menus_video_later:true,			//可能是稍后再看？没出现过
	mblog_menus_comment_manager:true,		//评论管理
	mblog_menus_avatar_widget:true,		//头像挂件
	mblog_menus_card_bg: true,			//卡片背景
	mblog_menus_long_picture:true,		//生成长图
	mblog_menus_delete:true,				//删除
	mblog_menus_edit:true,				//编辑
	mblog_menus_edit_history:true,		//编辑记录
	mblog_menus_edit_video:true,			//编辑视频
	mblog_menus_sticking:true,			//置顶
	mblog_menus_open_reward:true,			//赞赏
	mblog_menus_novelty:true,			//新鲜事投稿
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

const modifyCardsUrls = ['/cardlist', '/page', 'video/community_tab', '/searchall'];
const modifyStatusesUrls = ['statuses/friends/timeline', 'statuses/unread_friends_timeline', 'statuses/unread_hot_timeline', 'groups/timeline'];

const otherUrls = {
	'/profile/me': 'removeHome',						//个人页模块
	'/statuses/extend': 'itemExtendHandler',					//微博详情页
	'/video/remind_info': 'removeVideoRemind',			//tab2菜单上的假通知
	'/checkin/show': 'removeCheckin',					//签到任务
	'/live/media_homelist': 'removeMediaHomelist',		//首页直播
	'/comments/build_comments': 'removeComments',		//微博详情页评论区相关内容
	'/container/get_item': 'containerHandler',			//列表相关
	'/profile/statuses': 'userHandler',					//用户主页
	'/video/tiny_stream_video_list': 'nextVideoHandler',	//取消自动播放下一个视频
	'/2/statuses/video_mixtimeline': 'nextVideoHandler',	
	'/!/client/light_skin': 'tabSkinHandler',
	'/littleskin/preview': 'skinPreviewHandler',
	// '/remind/unread_count': 'unreadCountHandler',		
}

function getModifyMethod(url) {
	for (const s of modifyCardsUrls) {
		if(url.indexOf(s) > -1) {
			return 'removeCards';
		}
	}
	for (const s of modifyStatusesUrls) {
		if(url.indexOf(s) > -1) {
			return 'removeTimeLine';
		}
	}
	for(const [path, method] of Object.entries(otherUrls)) {
		if(url.indexOf(path) > -1) {
			return method;
		}
	}
	return null;
}


function isAd(data) {
	if(!data) {
		return true;
	}
	if(data.mblogtypename == '广告' || data.mblogtypename == '热推') {return true};
	if(data.promotion && data.promotion.type == 'ad') {return true};
	return true;
}


function removeCards(data) {
	if(!data.cards) {
		return;
	}
	let newCards = [];
	for (const card of data.cards) {
		let cardGroup = card.card_group;
		if(cardGroup && cardGroup.length > 0) {
			let newGroup = [];
			for (const group of cardGroup) {
				let cardType = group.card_type;
				if(cardType != 118) {
					newGroup.push(group);
				}
			}
			card.card_group = newGroup;
			newCards.push(card);
		} else {
			let cardType = card.card_type;
			if([9,165].indexOf(cardType) > -1) {
				if(!isAd(card.mblog)) {
					newCards.push(card);
				}
			} else {
				newCards.push(card);
			}
		}
	}
	data.cards = newCards;
}


function lvZhouHandler(data) {
	if(!mainConfig.removeLvZhou) return;
	if(!data) return;
	let struct = data.common_struct;
	if(!struct) return;
	let newStruct = [];
	for (const s of struct) {
		if(s.name != '绿洲') {
			newStruct.push(s);
		}
	}
	data.common_struct = newStruct;
}



function removeTimeLine(data) {
	for (const s of ["ad", "advertises", "trends"]) {
		if(data[s]) {
			delete data[s];
		}
	}
	if(!data.statuses) {
		return;
	}
	let newStatuses = [];
	for (const s of data.statuses) {
		if(!isAd(s)) {
			lvZhouHandler(s);
			newStatuses.push(s);
		}
	}
	data.statuses = newStatuses;
}


function removeHomeVip(data) {
	if(!data.header) {
		return data;
	}
	let vipCenter = data.header.vipCenter;
	if(!vipCenter) {
		return data;
	}
	vipCenter.icon = '';
	vipCenter.title.content = '会员中心';
	return data;
}

//移除tab2的假通知
function removeVideoRemind(data) {
	data.bubble_dismiss_time = 0;
	data.exist_remind = true;
	data.image_dismiss_time = 0;
	data.image = '';
	data.tag_image_english = '';
	data.tag_image_english_dark = '';
	data.tag_image_normal = '';
	data.tag_image_normal_dark = '';
}


//微博详情页
function itemExtendHandler(data) {
	if(mainConfig.removeRelate || mainConfig.removeGood) {
		if(data.trend && data.trend.titles) {
			let title = data.trend.titles.title;
			if(mainConfig.removeRelate && title === '相关推荐') {
				data.trend = null;
			} else if (mainConfig.removeGood && title === '博主好物种草') {
				data.trend = null;
			}
		}
	}
	if(mainConfig.removeFollow) {
		if(data.follow_data) {
			data.follow_data = null;
		}
	}

	if(mainConfig.removeRewardItem) {
		if(data.reward_info) {
			data.reward_info = null;
		}
	}

	//广告 暂时判断逻辑根据图片	https://h5.sinaimg.cn/upload/1007/25/2018/05/03/timeline_icon_ad_delete.png
	try {
		let picUrl = data.trend.extra_struct.extBtnInfo.btn_picurl;
		if(picUrl.indexOf('timeline_icon_ad_delete') > -1) {
			data.trend = null;
		}
	} catch (error) {
		
	}


	if(mainConfig.modifyMenus && data.custom_action_list) {
		let newActions = [];
		for (const item of data.custom_action_list) {
			let _t = item.type;
			let add = itemMenusConfig[_t]
			if(add === undefined) {
				newActions.push(item);
			} else if(_t === 'mblog_menus_copy_url') {
				newActions.unshift(item);
			} else if(add) {
				newActions.push(item);
			}
		}
		data.custom_action_list = newActions;
	}
}

function updateFollowOrder(item) {
	try {
		for (let d of item.items) {
			if(d.itemId === 'mainnums_friends') {
				let s = d.click.modules[0].scheme;
				d.click.modules[0].scheme = s.replace('231093_-_selfrecomm', '231093_-_selffollowed');
				log('updateFollowOrder success');
				return;
			}
		}
	} catch (error) {
		console.log('updateFollowOrder fail');
	}
}

function updateProfileSkin(item, k) {
	try {
		let profileSkin = mainConfig[k];
		if(!profileSkin) {return;}
		let i = 0;
		for (let d of item.items) {
			if(!d.image) {
				continue;
			}
			d.image.iconUrl = profileSkin[i++];
			if(d.dot) {
				d.dot = [];
			}
		}
		log('updateProfileSkin success');
	} catch (error) {
		console.log('updateProfileSkin fail');
	}
}


function removeHome(data) {
	if(!data.items) {
		return data;
	}
	let newItems = [];
	for (let item of data.items) {
		let itemId = item.itemId;
		if(itemId == 'profileme_mine') {
			if(mainConfig.removeHomeVip) {
				item = removeHomeVip(item);;
			}
			updateFollowOrder(item);
			newItems.push(item);
		} else if (itemId == '100505_-_top8') {
			updateProfileSkin(item, 'profileSkin1');
			newItems.push(item);
		} else if (itemId == '100505_-_newcreator') {
			if(item.type == 'grid') {
				updateProfileSkin(item, 'profileSkin2');
				newItems.push(item);
			} else {
				if(!mainConfig.removeHomeCreatorTask) {
					newItems.push(item);
				}
			}
		} else if(['mine_attent_title', '100505_-_meattent_pic', '100505_-_newusertask', '100505_-_vipkaitong', '100505_-_hongbao2022'].indexOf(itemId) > -1) {
			continue;
		} else if (itemId.match(/100505_-_meattent_-_\d+/)) {
			continue;
		} else {
			newItems.push(item);
		}
	}
	data.items = newItems;
	return data;
}


//移除tab1签到
function removeCheckin(data) {
	log('remove tab1签到');
	data.show = 0;
}


//首页直播
function removeMediaHomelist(data) {
	if(mainConfig.removeLiveMedia) {
		log('remove 首页直播');
		data.data = {};
	}
}

//评论区相关和推荐内容
function removeComments(data) {
	let delType = [];
	if(mainConfig.removeRelateItem) delType.push('相关内容');
	if(mainConfig.removeRecommendItem) delType.push('推荐');
	if(delType.length === 0) return;
	let items = data.datas || [];
	if(items.length === 0) return;
	let newItems = [];
	for (const item of items) {
		let adType = item.adType || '';
		if(delType.indexOf(adType) == -1) {
			newItems.push(item);
		}
	}
	log('remove 评论区相关和推荐内容');
	data.datas = newItems;
}


//处理感兴趣的超话和超话里的好友
function containerHandler(data) {
	if(mainConfig.removeInterestFriendInTopic) {
		if(data.card_type_name === '超话里的好友') {
			log('remove 超话里的好友');
			data.card_group = [];
		}
	}
	if(mainConfig.removeInterestTopic && data.itemid) {
		if(data.itemid.indexOf('infeed_may_interest_in') > -1) {
			log('remove 感兴趣的超话');
			data.card_group = [];
		} else if(data.itemid.indexOf('infeed_friends_recommend') > -1) {
			log('remove 超话好友关注');
			data.card_group = [];
		}
	}
}

//可能感兴趣的人
function userHandler(data) {
	if(!mainConfig.removeInterestUser) {
		return;
	}
	let items = data.cards || [];
	if(items.length === 0) {
		return;
	}
	let newItems = [];
	for (const item of items) {
		if(item.itemid == 'INTEREST_PEOPLE') {
			log('remove 感兴趣的人');
		} else {
			lvZhouHandler(item.mblog);
			newItems.push(item);
		}
	}
	data.cards = newItems;
}


function nextVideoHandler(data) {
	if(mainConfig.removeNextVideo) {
		data.statuses = [];
		data.tab_list = [];
		console.log('nextVideoHandler');
	}
}

function tabSkinHandler(data) {
	try {
		let iconVersion = mainConfig.tabIconVersion;
		if(!iconVersion || !mainConfig.tabIconPath) return;
		if(iconVersion < 100) return;

		let skinList = data['data']['list']
		for (let skin of skinList) {
			// if(skin.usetime) {
			// 	skin['usetime'] = 330
			// }
			skin['version'] = iconVersion;
			skin['downloadlink'] = mainConfig.tabIconPath;
		}
		log('tabSkinHandler success')
	} catch (error) {
		log('tabSkinHandler fail')
	}
}


function skinPreviewHandler(data) {
	data['data']['skin_info']['status'] = 1
}


// function unreadCountHandler(data) {
// 	let ext = data.ext_new;
// 	if(!ext) return;
// 	if(!ext.creator_task) return;
// 	ext.creator_task.text = '';
// }

function log(data) {
	if(mainConfig.isDebug) {
		console.log(data);
	}
}


function nobyda() {
	const isQuanX = typeof $task != "undefined";
	const isSurge = typeof $httpClient != "undefined";
	const isRequest = typeof $request != "undefined";
	const notify = (title, subtitle='', message='') => {
		if (isQuanX) $notify(title, subtitle, message)
		if (isSurge) $notification.post(title, subtitle, message);
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
		read,
		done
	}
}

var body = $response.body;
var url = $request.url;
let method = getModifyMethod(url);
if(method) {
	log(method);
	var func = eval(method);
	let data = JSON.parse(body);
	new func(data);
	body = JSON.stringify(data);
}
// $done({ body });
$.done(body);