*文中均为Android环境下，iOS实现同样的操作需要越狱，复杂度比Android高得多，强烈建议使用Android机进行调试*

大家新年好啊，我又回来了，难得有空可以搞事情，就把前面挖的坑给填了吧，这次的中级篇就拿初级篇里[Coande](https://www.zhihu.com/people/Coande)同学和[不应该呀](https://www.zhihu.com/people/wan-yu-chao-70)同学提到的酷安和小红书这两个APP来开刀吧。

初级篇传送门：[当你写爬虫抓不到APP请求包的时候该怎么办？【初级篇】](https://zhuanlan.zhihu.com/p/46433599)

---

首先说一下中级篇的主要内容，中级篇要处理的是APP开启SSL Pinning后导致出现的初级篇通杀方案失效的问题。

那么什么是SSL Pinning呢？简单地说一下，SSL Pinning是一种防止中间人攻击（MITM）的技术，主要的机制是在客户端发起请求->收到服务器发来的证书这一步之后，对收到的证书进行校验，如果收到的证书不被客户端所信任，就直接断开连接不继续请求。

所以在遇到对关键请求开启了SSL Pinning的APP时，我们抓包就只能看到APP上提示无法连接网络或者请求失败之类的提示；而在抓包工具的界面上，要么就只能是看到一排CONNECT请求，获取到了证书后却没有后续了，要么就只有一些无关的请求，找不到自己想要的那个接口。

无法抓到包的效果图：

![无法抓到包的效果图1](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/1.png)
![无法抓到包的效果图2](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/2.png)

这个问题是怎么产生的呢？是这样，当我们使用抓包工具抓包时，抓包工具在拦截了服务端返回的内容并重发给客户端的时候使用的证书并不是服务端原来的证书，而是抓包工具自己的，抓包工具自己的证书并不是APP开发者设定的服务端原本的证书，于是就构成了中间人攻击，触发SSL Pinning的机制导致连接被中断，所以我们无法直接抓到包。

那应该怎么办呢？别急，办法很多而且也很简单，先了解一下常见的情况吧，常见的开启了SSL Pinning的APP大致分为两种操作：

1. 服务端使用了某个权威证书颁发机构（CA）颁发的证书，并在APP中校验证书的CA是否是正常的。
2. 服务端使用了CA颁发的证书或是自己给自己颁发的证书，并在APP中校验证书本身是不是正常的，需要将证书与APP本体一同下发。有把证书混淆在代码里藏起来的，也有直接放在资源目录下的。

不过呢，这两种操作都是能被通杀的，下面我将告诉你如何处理。本篇同样提供多种通杀方案，请读者自行根据自己所持设备的情况使用。

1. 直接使用低版本系统的Android手机（低于7.0）

> android 7.0 + 使用系统原生锁定方案,而7.0 Nougat之前则TrustKit自己逻辑实现锁定.

[**瘦蛟舞**](https://github.com/WooyunDota)大佬在[这篇文章](https://github.com/WooyunDota/DroidDrops/blob/6b3008bd409d539775b627ab49580035d8524eb0/2018/SSL.Pinning.Practice.md)中有提到，Android7.0以后是有系统原生的方案提供的，有些APP抓不到包的时候其实是因为版本比较高，用上了原生的方案。所以只要使用低于Android7.0版本系统的手机，就可以轻松绕过大部分APP的SSL Pinning，但这个方法毕竟不能彻底通杀，有些APP（也有可能是使用的请求库）有自己实现的SSL Pinning方案，所以对低版本系统也会有效，建议配合第二个方案使用。

如图所示，在Android 8下，抓包时无法抓到任何的有用的请求。

![Android8手机信息](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/3.jpg)

![在Android8下抓包-酷安](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/4.png)
![在Android8下抓包-小红书](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/5.png)

但在Android5.1.1下，却没有任何问题。

![Android8手机信息](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/6.jpg)
![在Android8下抓包-酷安](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/7.png)
![在Android8下抓包-小红书](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/8.png)

2. 使用Xposed或兼容Xposed的框架+JustTrustMe

这个方案使用的是[JustTrustMe](https://github.com/Fuzion24/JustTrustMe)这个Xposed模块，它所做的事情就是将各种已知的的HTTP请求库中用于校验证书的API都进行Hook，使无论是否是可信证书的情况，校验结果返回都为正常状态，从而实现绕过证书检查的效果。

具体操作的时候唯一麻烦的就是安装Xposed框架，但因为现在[**维术**](https://github.com/tiann)大佬的太极APP（关注他的公众号《虚拟框架》下载）支持使用Magisk挂载启动，实现了几乎与Xposed框架同样的使用方式和效果，并兼容了很多Xposed的模块，所以如果觉得Xposed框架安装太过麻烦或是担心砖机的同学可以尝试使用太极-Magisk，直接解了BL锁之后刷入Magisk并在Magisk-Manager中添加太极模块就可以使用了，安装和使用教程后续会再写一篇专门的说明链接过来，等不及的同学也可以直接看太极的文档进行操作。

效果呢就是开启JustTrustMe之后与低版本下抓包一致，关闭后打回原形，这里就不贴图了。

**注意：这个模块在过高的系统版本(8-9)下偶尔会出现导致所有HTTP请求都失败的BUG，如果不是使用专门的测试机安装这个模块的话，建议日常使用时将其关闭，以免遇到奇怪的问题。**

**注意：本人并未在日常用机上长时间使用太极-Magisk+JustTrustMe，不清楚是否存在其他BUG，如出现问题请联系维术或JustTrustMe作者。**

3. 将抓包工具的证书安装到系统根证书目录中

这个方案的来源是[这个贴子](https://www.v2ex.com/t/528852)中[letitbesqzr](https://www.v2ex.com/member/letitbesqzr)所提到的第二种方案，个人认为较为麻烦，不推荐使用，毕竟有权限往system分区写文件的时候完全可以用JustTrustMe了。

操作方法如下：

> 系统证书的目录是：/system/etc/security/cacerts/
> 每个证书的命名规则为：<Certificate_Hash>.<Number>
> Certificate_Hash 表示证书文件的 hash 值，Number 是为了防止证书文件的 hash 值一致而增加的后缀;
> 证书的 hash 值可以由命令计算出来，在终端输入 openssl x509 -subject_hash_old -in <Certificate_File>，其中 Certificate_File 为证书路径，将证书重命名为 hash.0 放入系统证书目录，之后你就可以正常抓包了。

4. VirtualXposed（VirtualApp）

这个方案的来源是[这个贴子](https://www.v2ex.com/t/528852)中[letitbesqzr](https://www.v2ex.com/member/letitbesqzr)所提到的第三种方案。原理不明，疑似VirtualApp在转发其内部APP的操作时没有进行校验证书的操作？希望有研究过的大佬解释一下具体原理。

使用这个方案时直接安装[VirtualXposed](https://github.com/android-hacker/VirtualXposed)即可，代理的设置还是在原来的地方操作，只需要将需要抓包的APP添加至VirtualXposed中，再打开它内部的那一个对应的APP就可以抓到包了。但并未详细测试这个方案对各种HTTP请求库的兼容性，所以不清楚用了其他HTTP请求库的APP是否也会是同样的效果。

效果如下：

![使用VirtualXposed之后抓包-小红书1](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/9.png)
![使用VirtualXposed之后抓包-小红书2](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E4%B8%AD%E7%BA%A7%E7%AF%87%E3%80%91/assets/10.png)

---

好了，学会了这四招之后，初级篇里的90%占比就被提升至99%了，剩下的那一小撮不被初、中级篇的方案破掉的APP将在高级篇中讲解，但应该是没有能做到通杀的方案了，毕竟每家的处理方式都不同。

欢迎提供高级篇的素材，在评论或私信里告知我都可以。

如果这篇文章有帮到你，请大力点赞，谢谢~~ 欢迎关注我的知乎账号[loco_z](https://www.zhihu.com/people/loco_z)和我的知乎专栏[《手把手教你写爬虫》](https://zhuanlan.zhihu.com/webspider)，我会时不时地发一些爬虫相关的干货和黑科技，说不定能让你有所启发。
