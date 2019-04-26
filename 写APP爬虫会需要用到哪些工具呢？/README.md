在各大平台的Web端内容日渐缩水、各种限制逐渐增多、各大流氓开始强行往APP导流的今天，作为爬虫工程师的你是否还只会写一些Web端爬虫？是否在面对需要跳转APP处理的部分时毫无办法？看完这一篇文章，你将会了解到写APP爬虫时所需要用到的工具，让你不用再自己摸索，不用再跟着网上那堆年代久远的教程使用着一些过时的工具。

---

**以下内容以常规分析流程中的阶段和类型来划分**

- 抓包

  - HTTP请求类

    - [Fiddler](https://www.telerik.com/fiddler)/[Charles](https://www.charlesproxy.com/)**（必备常用工具之一）**

      最常见的代理抓包工具，这两个就不用多说了吧？应该都知道了。

    - [ProxyDroid](https://github.com/madeye/proxydroid)**（必备常用工具之一）**

      强制全局代理工具，详细介绍见[当你写爬虫抓不到APP请求包的时候该怎么办？【初级篇】](https://zhuanlan.zhihu.com/p/46433599)。

    - [PacketCapture](https://play.google.com/store/apps/details?id=app.greyshirts.sslcapture)/[HTTPCanary](https://github.com/MegatronKing/HttpCanary)**（必备常用工具之一）**

      VPN抓包工具，详细介绍见[当你写爬虫抓不到APP请求包的时候该怎么办？【初级篇】](https://zhuanlan.zhihu.com/p/46433599)。

    - [JustTrustMe](https://github.com/Fuzion24/JustTrustMe)**（必备常用工具之一）**

      基于Xposed写的反SSL Pinning工具，详细介绍见[当你写爬虫抓不到APP请求包的时候该怎么办？【中级篇】](https://zhuanlan.zhihu.com/p/56397466)。

    - [ObjectionUnpinningPlus](https://github.com/WooyunDota/DroidSSLUnpinning/tree/master/ObjectionUnpinningPlus)**（必备常用工具之一）**

      瘦蛟舞写的一个Frida脚本，功能与JustTrustMe相同，但因为Frida的特殊性，可以随时修改内容，面对一些特殊情况时会很方便。

    - [WireShark](https://www.wireshark.org/)

      也是一个很常见的抓包工具，但由于工作方式过于底层，对HTTPS请求的处理比较麻烦，一般不建议对使用HTTP协议的APP使用。

  - 非HTTP请求类

    - [WireShark](https://www.wireshark.org/)

      非HTTP的还是使用WireShark这类工具方便些，通常需要配合反编译找到协议的组成方式。

      建议使用方式：电脑端开热点，然后指定用于创建热点的虚拟网卡，再把手机连上热点开始抓包。

    - [Tcpdump](https://www.tcpdump.org/#latest-releases)

      在使用没有无线网卡的电脑或无法开热点的情况下可以直接在手机上运行Tcpdump然后导出文件在电脑端WireShark中打开，与直接使用WireShark抓包效果相同。

- 破解加密参数，使用协议请求

  - Java层

    - [Jadx](https://github.com/skylot/jadx)**（必备常用工具之一）**

      一个非常方便的Java反编译工具，一般用到的功能主要是搜索、反混淆、查找方法调用这几样，性能和反编译出来的代码效果都比使用dex2jar+jd-gui之类的方式好。

    - [Xposed](https://repo.xposed.info/)**（必备常用工具之一）**

      Xposed框架大家应该都知道吧？这是一个功能十分强大的Hook框架，很多逆向工具都是基于它来写的，有特殊需求时也可以自己写一个模块使用。

    - [Frida](https://www.frida.re/)**（必备常用工具之一）**

      相对于Xposed而言，Frida算是一个在安全圈外没有那么高知名度的Hook工具了，但它的功能在某些方面要比Xposed强得多（当然也有缺点），举个常用到的例子：用它来Hook So库中的函数~。

    - [inspeckage](https://github.com/ac-pm/Inspeckage)**（必备常用工具之一）**

      这是一个基于Xposed写的动态分析工具，Hook了大量逆向时常见的方法，下面是它的GitHub中给出的列表：

      > - Shared Preferences (log and file);
      > - Serialization;
      > - Crypto;
      > - Hashes;
      > - SQLite;
      > - HTTP (an HTTP proxy tool is still the best alternative);
      > - File System;
      > - Miscellaneous (Clipboard, URL.Parse());
      > - WebView;
      > - IPC;
      > - - Hooks (add new hooks dynamically)

      注意它Hook列表中有Crypto和Hash，这两个类型在破解大部分APP的加密参数时可以说是降维打击，因为大部分APP的加密参数都逃不过MD5、SHA1、AES、DES这四种，而它们都被Hook了（不仅仅只有这四种）。基本上就是打开Inspeckage再打开它的Web端，然后打开指定的APP操作一下，一个搜索，加密参数就原形毕露了。

    - [DeveloperHelper](https://github.com/WrBug/DeveloperHelper)

      一个基于Xposed写的辅助工具，通常会用到的功能是查看Activity名、查看加固类型、查看Activity结构、自动脱壳这几个。

    - [UCrack](https://gitee.com/virjar/ucrack)

      也是一个基于Xposed写的辅助工具，集成了自动网络抓包、网络堆栈爆破、文件日志、WebView调试环境、自动脱壳、Native函数注册监控、记录程序自杀堆栈等功能，这个工具是我之前偶然发现的，还没有使用过，有兴趣的同学可以用用看。

  - C/C++层（So库）

    - [IDA](https://www.hex-rays.com/products/ida/)**（必备常用工具之一）**

      非常强大的反汇编和动态调试工具，强烈不推荐使用NSA开源的Ghidra，效果跟IDA比起来差太多了。IDA可以在反汇编之后将汇编代码转成伪C代码，并且能在手机端启动了服务端之后注入APP进程使用动态调试功能。

    - [Frida](https://www.frida.re/)**（必备常用工具之一）**

      上面讲过了

  - 有壳（加固）的

    - [DeveloperHelper](https://github.com/WrBug/DeveloperHelper)

      上面讲过了

    - [UCrack](https://gitee.com/virjar/ucrack)

      上面讲过了

    - [FDex2](https://bbs.pediy.com/thread-224105.htm)

      其实就是把几行代码包了一层而已，原理就是Hook ClassLoader的loadClass方法，反射调用getDex方法取得Dex(com.android.dex.Dex类对象)，再将里面的dex写出。（原理来自原帖）

- 破不动，使用群控

  - [Appium](http://appium.io/)

    一个自动化测试工具，但是拿来做群控也是没啥问题的。

  - [AirTest](https://github.com/AirtestProject/Airtest)

    网易搞的一个自动化测试工具，原生支持群控，各方面方便程度都要比Appium高。

  - [ATX](https://github.com/openatx)

    一个手机控制套件，改一改包一层就是群控了。

**可能还有一些工具因为不常用的关系一时没想起来，等想起来了会继续加在这个列表中，建议收藏本文。**

---

如果这篇文章有帮到你，请大力点赞，谢谢~~ 欢迎关注我的知乎账号[loco_z](https://www.zhihu.com/people/loco_z)和我的知乎专栏[《手把手教你写爬虫》](https://zhuanlan.zhihu.com/webspider)，我会时不时地发一些爬虫相关的干货和黑科技，说不定能让你有所启发。





