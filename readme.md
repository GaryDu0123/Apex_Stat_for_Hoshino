# APEX Legend制造器,地图轮换查询

要获得完整功能, 需要去 [APEX LEGENDS STATUS](https://apexlegendsapi.com) 申请api

# 部署
1. 下载或者clone本插件到`hoshino\modules`目录下
```shell
git clone https://github.com/GaryDu0123/Apex_Stat_for_Hoshino
```
2. 将申请到的APIkey填写到`api.py`文件内的`API_KEY`变量中, 或者不填写
> 填写示范 API_KEY = "你的APIkey"
3. 在`hoshino\config\bot.py`的`MODULES_ON`中添加 `"Apex_Stat_for_Hoshino"`
4. 重启Hoshino Bot

# API申请以及使用
## 基本
在浏览器中打开[APEX LEGENDS STATUS(https://apexlegendsapi.com)](https://apexlegendsapi.com),
看向`Create an API key`(创建一个API Key), 选择`Non-Commercial`(非商用), 
描述一下使用原因(用于apex数据查询 `For apex data query`), 尽量使用英文, ~~开发者好像没有审核描述信息~~, `I agree with API usage rules`打钩, 然后点击`Create my API key`就可以了

> 注意, 该API注明了商用限制, 若BOT为商用则需要选择`Commercial`, 请仔细阅读该API提供者发布的使用文档.

这时候页面会跳转, 你将会从页面看到如下信息 `You are currently logged in with API key [此处是你的APIkey]. You can access the other pages.`

复制这个APIkey到`api.py`文件内的`API_KEY`变量中, 便可以正常使用了

## 进阶
> When first creating an API key, you are limited to one request per 2 seconds. This limit can be increased to 2 requests/seconds by connecting with your Discord account. To do so, click on the red popup at the top of the API Portal.
> 
> From https://apexlegendsapi.com/#rate-limiting

对于新创建的APIkey, 会被限制为2秒钟才能请求一次, 该限制可以通过绑定Discord账号来提升到1秒请求2次.
具体详细请根据页面提示绑定你的账号从而解除限制.

# 使用区别
不去申请APIkey也可以使用, 但是使用的命令会有限制. 参考了[Apex-Stats-Bot](https://github.com/StryderDev/Apex-Stats-Bot)的代码, 使用了`fn.alphaleagues.com/v2/apex/map/`网站作为了API来源, 但是该网站提供的数据有限, 并且请求参数尚不清楚, 所以只实现了小部分功能.

**功能使用方法**

```
@bot apex 查询当前地图
bot名字 apex 查询轮换地图 3
```

## 填写APIKEY后的可用指令

| 指令                    | 描述                              |
| ----------------------- | --------------------------------- |
| apex 查询当前地图       | 查询当前为哪张地图                |
| apex 查询下张地图       | 查询下张地图                      |
| apex 查询轮换地图 [1-5] | 查询未来1-5小时的地图以及轮换时间 |
| apex 查询制造器         | 查询今日复制器可制造物品          |

## 未填写APIKEY的可用指令

| 指令                    | 描述                              |
| ----------------------- | --------------------------------- |
| apex 查询当前地图       | 查询当前为哪张地图                |
| apex 查询轮换地图 [1-5] | 查询未来1-5小时的地图以及轮换时间 |

# 待实现

1. 玩家个人数据查询
2. 查询数据图片化
3. APEX新闻



# 附录

APEX LEGENDS STATUS API 接口文档

https://apexlegendsapi.com/#introduction