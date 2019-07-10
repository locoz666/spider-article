说到逆向APP，很多人首先想到的都是反编译，但是单看反编译出来的代码很难得知某个函数在被调用时所传入的参数和它返回的值，极大地增加了逆向时的复杂度，有没有什么办法可以方便地知道被传入的参数和返回值呢？

答案是有的，这个方法就是Hook，Hook的原理简单地说就是**用一个新的函数替代掉原来的函数**，在这个新的函数中你想做什么都可以，为所欲为。

本文中的Frida就是一个很常用的Hook工具，只需要编写一段Javascript代码就能轻松地对指定的函数进行Hook，而且它基本上可以算是全平台的（主流平台全覆盖），除了Android以外，iOS和PC端的APP也可以用它来进行Hook，非常方便。

---

那么怎么使用呢？首先我们在Frida官方文档中的Installation页可以看到，我们需要有Python环境，并且用pip安装一个叫frida-tools的库，然后才可以开始使用。

![](https://oss.crawler-lab.com/20190702201658.png?x-oss-process=style/weixin)

Python环境相信大家都有了，直接打开命令行，执行一波`pip install frida-tools`吧。

安装完毕以后，因为这一页文档的下半部分用于测试刚装好的库是否可用的话过于麻烦，我们这里就直接使用`frida-ps`命令来测试吧。

![](https://oss.crawler-lab.com/20190702201022.png?x-oss-process=style/weixin)

看起来是没问题了，然后我们怎么Hook Android手机上的APP呢？别急，还需要在手机上做一些操作你才能这么做。

---

我们需要有一台已经Root了的Android手机，因为不同型号的手机Root方法存在差异，本文中就不指导如何对手机进行Root操作了，请自行通过搜索引擎查找方法。**实在没有可以Root的Android手机的话可以选择使用模拟器，推荐使用Genymotion之类系统较为原生的模拟器，并将Android版本选择在6.0以上，否则可能会出现一些奇奇怪怪的问题**。

手机准备好了之后，找到Frida文档中Tutorials栏里的Android页，开始进行Frida的手机端准备工作。

![](https://oss.crawler-lab.com/20190702201427.png?x-oss-process=style/weixin)

文档中能看到，Frida官方最近的大部分测试都是在运行着Android 9的Pixel 3上进行的，所以理论上来讲如果你在使用中遇到任何奇怪的问题，都可能是你手机的系统导致，**所以这里再次建议，使用较为原生和偏高版本的系统（建议至少6.0）进行操作**。

![](https://oss.crawler-lab.com/20190702201516.png?x-oss-process=style/weixin)

接着往下看，我们需要在手机上以Root权限运行一个叫frida-server的东西，这个东西需要在Frida官方的GitHub仓库中下载，文档中有链接可以直接[跳转](https://github.com/frida/frida/releases)。

![](https://oss.crawler-lab.com/20190702194502.png?x-oss-process=style/weixin)

打开GitHub之后你会发现，这里有很多个不同的版本，应该下载哪一个呢？

可以看到这一排的文件中，末尾处都有个系统和CPU架构的标识，我们直接看Android的。这里标了Android的一共有四个，然后X86的因为不是手机使用的CPU架构，可以直接pass掉，剩下的就是arm和arm64两种了，那么我们需要怎么判断自己的手机/模拟器属于哪一种CPU架构的呢？

查CPU架构的方法很多，这里介绍一个比较方便快捷的——使用一个名叫Device Info HW的APP。

![](https://oss.crawler-lab.com/20190702195305.png?x-oss-process=style/weixin)

安装后打开它，在芯片栏中我们可以看到一个叫ABI的东西，右边就是我们手机的CPU架构了，如下：

![](https://oss.crawler-lab.com/20190702195704.png?x-oss-process=style/weixin)

所以这里我需要下载的是arm64版本的frida-server，下载后解压出来一个没后缀的文件，然后我们需要将这个文件放入手机中运行起来。先把这个文件的名字改成`frida-server`，然后在这个文件所在的目录下打开命令行（Windows下为Shift+鼠标右键，选择“在此处打开CMD/PowerShell”），执行以下命令：

```
adb root
adb push frida-server /data/local/tmp/ 
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"
```

如果你的手机和我的一样，直接这么运行会提示权限不足的话，可以先进入`adb shell`，在执行`su`命令获取Root权限后（手机端可能会弹出Root授权提示），再运行`/data/local/tmp/frida-server &`启动frida-server。

![](https://oss.crawler-lab.com/20190702200411.png?x-oss-process=style/weixin)

启动后，我们先照惯例来测试一下是否能正常使用了，和前面一样，使用`frida-ps`命令，但在后面加一个`-U`参数，这个参数的意思是让它对USB连接的设备操作，如果不出意外的话，你应该能看到与不加`-U`参数时截然不同的显示。

![](https://oss.crawler-lab.com/20190702201219.png?x-oss-process=style/weixin)

至此，所有准备工作均已完成。

小提示：在手机重启后需要重新运行一次frida-server，但可以不重新执行`adb push`操作，因为文件已经放进去了。

---

终于到了喜闻乐见的实战环节了，就拿Frida官方文档中的提到的CTF APP来开刀吧，找到文档中Examples栏里的Android页，经过几次跳转后下载APP安装、打开，会看到这样的一个界面：

![](https://oss.crawler-lab.com/20190702202806.png?x-oss-process=style/weixin)

这个APP是一个石头剪子布的游戏，点击下面三个按钮分别选择石头、剪子、布，玩起来的时候是这么一个效果（加号后面的是得分值，正常情况下连胜会每次在原来的基础上+1）：

![](https://oss.crawler-lab.com/20190702202946.png?x-oss-process=style/weixin)

我们先做个比较简单的操作吧，让我们的每次出招都必胜~先复制一下文档中的代码，建一个.py文件粘贴进去，将`this.cnt.value = 999;`这一条删除或注释掉，然后运行这个python脚本，在注入完成后，不管你怎么点，你都是必定胜利的，如下图：

![](https://oss.crawler-lab.com/20190702204031.png?x-oss-process=style/weixin)

注：图中左下方显示的是Hook时产生的日志，其中value是得分值。

但是这样子弄，如果我们需要让分值达到很高的话，就需要点很多次了，怎么让它一次就加到999呢？很简单，直接把得分值也给改了就好了，我们把前面去掉的`this.cnt.value = 999;`再改回来，然后重新运行一遍这个脚本。

![](https://oss.crawler-lab.com/20190702204546.png?x-oss-process=style/weixin)

正常情况下这个分值会是一个+999，这里显示成这样是因为这个样例APP太老了，不兼容新版本系统，导致出现这种情况，换旧版本系统可解，所以这里不纠结这个问题。

---

单看这么一通操作是不是觉得很懵？复制过来的代码是干啥的都不知道，如果换一个APP咋搞？不慌，我把这个代码的意思一行一行地给你解释一遍，你就知道怎么用了。

![](https://oss.crawler-lab.com/20190702211520.png?x-oss-process=style/weixin)

首先import不用说了吧，大家都懂，直接看on_message这个函数。这个on_message的用途是接收下面Javascript代码中调用send函数传出的日志，通常我们可以不用管它，直接复制出来用就行了，或者可以使用console.log打日志，效果也是差不多的。

然后是jscode这个变量，这个变量其实建议使用一个单独的.js文件代替，因为这样的话可以使用各种编辑器、IDE的JavaScript代码格式化、智能提示等功能，写起来会舒服很多。如果你要替换掉的话，改成读JS代码文件之后read出内容字符串赋值给jscode就行了。

![](https://oss.crawler-lab.com/20190702211359.png?x-oss-process=style/weixin)

接着是JS代码中的部分。

先看看`Java.perform`，在Frida官方文档的javascript-api页中可以看到，它的用途是确保当前线程已连接到VM用的，所以我们直接照着这么用就行了；

然后看看`Java.use`这个函数，它的用途是获取一个指向某个类的指针，参数中的`com.example.seccon2015.rock_paper_scissors.MainActivity`就是我们需要Hook的那个类；

接着就是真正执行Hook的部分了，这个代码中使用了一个`MainActivity.onClick.implementation `，意思就是Hook前面获取到的类中的onClick方法，后面跟着的赋值函数的部分，函数的参数为对应要Hook方法的参数，内部执行的部分就是在对应方法被调用时所执行的代码，这里它是先打了一个`onClick`日志，然后调用了原始方法（如果不调用的话原始方法不会被执行），接着它将m、n、cnt（变量具体含义请自行反编译APP后查看代码）的值做了修改，最后，它又打了一个携带着cnt变量值的日志。

![](https://oss.crawler-lab.com/20190702211445.png?x-oss-process=style/weixin)

最后是一些常规操作，`frida.get_usb_device().attach()`是获取指定APP（参数为包名）当前运行着的进程，`process.create_script(jscode)`、`script.load()`是将前面的JS代码注入进去，`script.on('message', on_message)`是设置消息传出时的回调，最后的`sys.stdin.read()`是输出日志用的。

总之，除了JS代码部分，其他的其实只是个壳子，核心的Hook操作逻辑全在JS代码中，我们在使用时一般只改JS代码部分和指定包名的部分就可以了。

---

看了这一篇文章后你应该会对使用Frida对Android手机上Java层的Hook有所了解了吧，如果觉得玩Frida官方文档中的这个石头剪子布APP不够刺激，还可以看看我前面的《当你写爬虫遇到APP的请求有加密参数时该怎么办？【初级篇-秒杀模式】》这篇文章，里面使用的DEMO APP是有SSL Pinning、且对代码进行了混淆的，希望你能够举一反三，自己写出一个干掉这个SSL Pinning的脚本。（如果还不会的话可以看更前面的《当你写爬虫抓不到APP请求包的时候该怎么办？【高级篇-混淆导致通用Hook工具失效】》这篇文章）

发送消息“Frida Android初级篇”到我的公众号【小周码字】即可获得代码和APP的下载地址~

这个时代各种东西变化太快，而网络上的垃圾信息又很多，你需要有一个良好的知识获取渠道，很多时候早就是一种优势，还不赶紧关注我的公众号并置顶/星标一波~ 
