看完了初级篇的常规模式之后，你是不是发现了一个很严重的问题：如果每个APP都需要这么反编译看代码仿写的话，那么当想要大批量爬不同的APP的时候，光是找加密参数的生成部分就已经很花时间了，有没有更快捷的办法呢？

答案是有的，而且对于初级篇水平的APP来说，这个操作可以让你在一分钟内直接秒掉它的加密参数部分，可以说是一种降维打击了！

---

那么这个效果是怎么做到的呢？其实很简单，就是直接将Java标准库中常见的被用于生成加密参数的方法给Hook了，监听它们的输入参数和返回值，这样就能直接得到加密、Hash前的原文、密钥、IV等内容了，怎么样？是不是很简单？

**小提示**：之所以不提Kotlin，是因为在Kotlin下写加密、Hash操作的代码时如果不使用第三方库的话，就只能调用Java的标准库了，而第三方库的类名、方法名可能性太多了，不像标准库那样可以直接秒杀一大片，所以不属于本系列初级篇内容。（已询问多位Android开发同学验证此结论）

所以...要怎么操作呢？其实目前已经有一个非常方便的、基于Xposed框架编写的、能实现这种效果的工具了，它就是——Inspeckage。这个工具其实我在前面的《写APP爬虫会需要用到哪些工具呢？》文章中有提到过，它已经将标准库中常用的加密、Hash方法都给Hook了：

![Inspeckage Hook 加密类操作标准库的代码](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E7%A7%92%E6%9D%80%E6%A8%A1%E5%BC%8F%E3%80%91/assert/1.png?x-oss-process=style/weixin)

![Inspeckage Hook Hash类操作标准库的代码](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E7%A7%92%E6%9D%80%E6%A8%A1%E5%BC%8F%E3%80%91/assert/2.png?x-oss-process=style/weixin)

而在你需要的时候，只需要打开Inspeckage -> 选择需要Hook的APP -> 打开Inspeckage的Web端或者在日志中搜索你所需要找的加密参数就可以得到原文和使用的加密、Hash类型，直接秒杀！

接下来我将继续使用前面常规模式中的Demo APP来进行演示，如果你迫不及待地想要尝试了的话，可以发送消息【APP加密参数破解初级篇代码】到我的公众号[小周码字]获得Demo APP的下载地址，注意是发送【APP加密参数破解初级篇代码】，上一篇中有人发的是“小周码字”，还问我为啥没有反应...

---

话不多说，我们开始实战，首先我们需要准备一台已经安装好Xposed框架的Android手机，然后在Inspeckage的GitHub仓库中下载最新编译好的Inspeckage安装包或直接在Xposed管理器中安装它。

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E7%A7%92%E6%9D%80%E6%A8%A1%E5%BC%8F%E3%80%91/assert/3.png?x-oss-process=style/weixin)

装好后记得在Xposed管理器中将它启用，启用后需要重启生效。

---

准备好了环境之后，我们就可以开始破解这个Demo APP了，打开Inspeckage，点击“choose target”选中想要Hook的APP（这里选择“APP加密参数DEMO-初级篇”）。

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E7%A7%92%E6%9D%80%E6%A8%A1%E5%BC%8F%E3%80%91/assert/4.png?x-oss-process=style/weixin)

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E7%A7%92%E6%9D%80%E6%A8%A1%E5%BC%8F%E3%80%91/assert/5.png?x-oss-process=style/weixin)

选中后点击“LAUNCH APP”按钮就可以了。

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E7%A7%92%E6%9D%80%E6%A8%A1%E5%BC%8F%E3%80%91/assert/6.png?x-oss-process=style/weixin)

**小提示**：如果在这之前你打开过指定的APP的话，需要将其强制停止后再点击“LAUNCH APP”按钮，否则可能会出现Hook失败的情况。

在启动之后我们就可以在Inspeckage的Web端或日志中搜索sign的加密后参数了，这里说一下怎么操作：

- Web端

  Web端的话，如果你的手机和电脑是在同一个网络环境下，且手机和电脑能互通，那么你可以在电脑上直接用浏览器访问手机上显示的内网IP地址（如`http://192.168.137.64:8008`）；如果你的网络环境使你不能这么操作的话，你还可以用adb命令`adb forward tcp:8008 tcp:8008`将手机上的8008端口映射到电脑上，然后就可以直接访问`http://127.0.0.1:8008`了（需要8008端口未被占用）。

  ![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E7%A7%92%E6%9D%80%E6%A8%A1%E5%BC%8F%E3%80%91/assert/7.png?x-oss-process=style/weixin)

  在打开了Web端之后，将页面上方那个扳手按钮右边的自动刷新选项打开，就可以看到被Hook出来的东西了。

- 日志

  可以使用adb命令`adb logcat`来导出日志然后查看，或者是用像Android Studio中的logcat工具这种流式、带搜索功能的工具来查看。另外如果在Web端找到对应的加密参数时，原文过长导致出现被截断的情况，也可以在日志中找到对应的内容进行查看，打到日志中的会是完全体。

---

之后依然是常规流程，先抓个包看看。**（再次提醒，如果你抓不到包的话，先看看我之前的抓包系列文章，这是基本操作！）**

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E7%A7%92%E6%9D%80%E6%A8%A1%E5%BC%8F%E3%80%91/assert/8.png?x-oss-process=style/weixin)

这里我们抓包后得到了一个sign：`188c338423f3af3c2c0277946de958f8`，直接将它复制出来，然后在Inspeckage的Web端中的Hash栏内搜索（日志内搜索直接搜sign的内容即可）。

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E7%A7%92%E6%9D%80%E6%A8%A1%E5%BC%8F%E3%80%91/assert/9.png?x-oss-process=style/weixin)

看到了吗？直接就得到了它的原文：`brand=Xiaomi&device=capricorn&model=MI 5s&ts=1560859682&version=8.1.0`了，轻轻松松地就破解了这个APP的sign参数，全程只用了一分钟！

------

这个时代各种东西变化太快，而网络上的垃圾信息又很多，你需要有一个良好的知识获取渠道，很多时候早就是一种优势，还不赶紧关注我的公众号并置顶/星标一波~

发送消息“APP加密参数破解初级篇代码”到我的公众号【小周码字】即可获得demo代码和APP的下载地址~