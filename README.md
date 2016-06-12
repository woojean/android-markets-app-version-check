# amavc - Android Markets App Version Check
***
<br/>

## 简介
这是一个用于快速检测指定Android App在目前国内流行的诸多安卓应用市场中的最新发布版本的工具，可以**帮助跟踪android app新版本的对外发布情况，进而保证app在安卓应用市场中的发布版本都是最新的。**
<br/>


***
## 使用
例如腾讯视频当前最新的发布版本是4.8.5.10223，现在想要检测新版本的发布情况，可以在项目目录下执行如下命令：
```
  cd /yourpath/amavc
  python check 腾讯视频 4.8.5.10223
```
脚本将会扫描预先配置的多个安卓应用市场，并在amavc/reports目录下分别生成`json、html格式的两份检测报告文件`。
###json文件的格式如下：
 ![image](https://github.com/woojean/amavc/raw/master/imgs/json.png)
###html文件的内容如下：
 ![image](https://github.com/woojean/amavc/raw/master/imgs/report.png)
如果因为网络超时，或者解析误判等原因造成版本解析失败，可以点击报告中的`“查看详情”`，快速进行人工判断。

