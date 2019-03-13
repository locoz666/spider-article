*文中均为Android环境下，实战中可以尝试降低APP版本或是尝试抓一下iOS版APP的包（如果有），但不建议太过依赖iOS版APP*

助人为乐的我又来了，这次又是在逛v2ex时看到的一个[求助帖](https://www.v2ex.com/t/496299)。

帖子内容：

> 最近在抓包一个 APP：淘最热点
> 一款新闻 APP
> 抓不到新闻列表内容
> 只抓到了新闻图片
> 其他同类型的 APP 也抓过
> 没出现这种问题
> 用的 charles 抓的，证书设置没问题
> 不知道是不是这个 APP 的新闻列表走了其他协议
> 有大佬帮忙抓下看看嘛

看起来这位同学是遇到了一个APP的请求不走代理，以至于出现抓包时看不到关键的请求的问题，我们先来把这个APP装上，抓个包看看具体情况吧。

![没有抓到新闻列表的请求](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/1.png)

抓到的包里确实没有看到新闻列表的请求，除了图中的这些部分以外全都是图片以及CONNECT请求。

---

插播一个小提示：Fiddler在这个地方可以移除图片、CONNECT类型的请求等干扰项哦。

![移除CONNECT类型的请求](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/2.png)
![移除返回内容为图片类型的请求](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/3.png)

---

如果抓不到包的话就没法继续写爬虫了，那么这种情况应该怎么办呢？不要慌，看完这篇文章后你就能轻松通杀90%以上**无法通过直接设置系统代理就抓到包**的APP。

这里说两种非常简单的方案吧：

1.  使用强制全局代理

这里选用[Proxy Droid](https://github.com/madeye/proxydroid)这个工具来实现强制全局代理的效果。**注意：需要有ROOT权限才能使用**

Proxy Droid的原理是通过iptables将所有TCP连接重定向到代理服务器上，强制性地让APP的HTTP请求通过代理。

在安装Proxy Droid时可以选择clone一份GitHub仓库的代码然后自己编译安装，也可以选择直接在应用商店下载安装，推荐在[GooglePlay](https://play.google.com/store/apps/details?id=org.proxydroid)上下载，如果你没有科学上网的话，在其他应用商店比如[UpToDown](https://proxydroid.cn.uptodown.com/android)和[ApkHere](https://cn.apkhere.com/app/org.proxydroid)上也可以下载到。（**安装完之后记得要给它ROOT权限**）

使用方法很简单，**设置好系统代理后**打开Proxy Droid并设置好代理服务器的IP和端口，然后点击开启按钮。

![开启Proxy Droid](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/4.png)

此时再抓包就能抓到这个APP的列表页请求了。

![成功抓到新闻列表的请求](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/5.jpg)

2. 使用VPN抓包

如果使用强制全局代理方案的时候发现APP内请求速度明显变慢很多或是完全无效的话，可以尝试一下使用VPN抓包，这里使用Packet Capture来实现。**注意：这个APP不需要ROOT权限**

Packet Capture的原理是在本地创建一个VPN，使所有请求都从VPN中流过，从而实现不适用代理抓包的效果。（这个APP不是开源的，且处理部分都是调用的so库，APP本身只是一个壳而已，想要看代码的话需要有一定的Android逆向知识和经验）

因为没有开源，所以这个APP只能在应用商店里下载，推荐在[GooglePlay](https://play.google.com/store/apps/details?id=app.greyshirts.sslcapture)上下载，如果没有科学上网话[酷安](https://www.coolapk.com/apk/app.greyshirts.sslcapture)也是有的。

界面展示：

![Packet Capture未开启状态](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/6.png)
![Packet Capture开启后](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/7.png)

---

再插播一个小提示：使用Packet Capture抓包时可以只看某个APP的请求，设置方式如下：

![Packet Capture指定查看某个APP](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/8.jpg)

点击图中画框的图标，会出现一个搜索界面，输入你要抓包的APP名并点击一下就会开始抓包了，会过滤掉其他无关APP的请求，只保留你想要的这一个APP的。

![Packet Capture指定查看淘最热点](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/9.png)

---

那么我们来试试它的效果吧，打开抓包后，在淘最热点的新闻列表里随便翻几下页。

![淘最热点APP内新闻列表](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/10.png)

然后切回Packet Capture。

![使用Packet Capture对淘最热点进行抓包](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/11.png)

可以看到已经抓到很多请求包了，找一个大小比平均值小的点进去看看（因为这里有图片，一般缩略图的大小和来源都比较相似，排除掉这些就是需要的那个API的请求了）。

![成功抓到新闻列表的请求1](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87%E3%80%91/assets/12.jpg)

轻松地抓到了它的列表页请求。

不过Packet Capture的缺点也很明显，因为只有手机上的APP，并且没有能从PC上连接的工具或接口，所以如果被抓包的APP在短时间内发出的请求过多，想要找到需要的那一个就是一件很令人头疼的事情了。

---

好了，学会了这两招的你，现在可以通杀90%以上抓不到包的APP了，接下来的中级篇里将会告诉你如何破掉开启了SSL Pinning的APP，将这90%提升至99%。

中级篇传送门：[当你写爬虫抓不到APP请求包的时候该怎么办？【中级篇】](https://zhuanlan.zhihu.com/p/56397466)

如果这篇文章有帮到你，请大力点赞，谢谢~~ 欢迎关注我的知乎账号[loco_z](https://www.zhihu.com/people/loco_z)和我的知乎专栏[《手把手教你写爬虫》](https://zhuanlan.zhihu.com/webspider)，我会时不时地发一些爬虫相关的干货和黑科技，说不定能让你有所启发。
