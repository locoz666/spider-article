嗯，在看完了《当你写爬虫抓不到APP请求包的时候该怎么办？》系列之后，同学们对抓APP的请求包应该已经是轻车熟路了吧。在对想爬的APP抓个包之后你可能会发现，只是抓到包似乎没有什么卵用啊，凡是有用的接口基本都有一个或多个加密的参数，而且它还每次请求都变，而自己去请求对应的接口时，如果没带或者随便输入一串值给这种参数，还会出现不返回数据的情况，这可怎么办才好？

别担心，据我观察，目前至少80%左右的常见APP（BAT这类大厂的除外）在安全方面做的并不好，在看完这篇文章之后，你将知道如何轻松地拿下它们。

---

我们直接开始实战演练吧，这里我写了一个演示用的APP给你玩，它会像我前面所说的一样，发出一个请求并带有一个加密参数——sign，且每次请求时sign都会变化。

![APP启动界面](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/1.png?x-oss-process=style/weixin)

安装之后打开它，并准备好你的抓包工具，然后点击“点击发送请求”按钮。

![请求完毕](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/2.png?x-oss-process=style/weixin)

不出意外的话会出现一个“sign校验通过”的提示，然后我们看看抓到的包吧。

![抓包结果](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/3.png?x-oss-process=style/weixin)

从抓包工具中我们可以很明显地看出来，会变动的参数有两个，一个是ts，一个是sign。（为了看到变化建议多发两个请求对比）

先分析一下参数的含义吧，ts从名字上可以看出来，应该是个时间戳，实际将ts的值格式化一下也可以确定这就是个请求时的时间戳；然后是sign，一眼看上去大概32位左右，而外观长这样的一般是hash，猜测一下最有可能性的是md5之类的，但不知道实际是如何生成的，只能逆向看看了。

---

该正式开始破解这个加密参数了，由于Android APP是静态编译的，不像JS，直接可以看到源码，所以...我们需要对APP进行反编译，这里我使用的工具名为Jadx，前面的《写APP爬虫会需要用到哪些工具呢？》和《当你写爬虫抓不到APP请求包的时候该怎么办？【高级篇-混淆导致通用Hook工具失效】》文章中也有提到，这里就不再赘述了。

![使用jadx反编译APK](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/4.png?x-oss-process=style/weixin)

反编译之后可以看到这么一堆乱七八糟的的东西，那么我们要怎么找到生成sign参数的地方呢？

看到那个像魔法棒一样的按钮了吗？点一下它。

![jadx搜索文本](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/5.png?x-oss-process=style/weixin)

然后它会弹出一个“搜索文本”的窗口，接着我们有两种方式快速定位到生成的位置：

1. 搜索URL的路径部分

   路径部分指的是/learning/hash_sign这一段，当然有些APP为了复用可能会将路径拆分成多段的，如果直接搜索完整路径搜索不到的话可以尝试以反斜杠为分隔符，将路径拆分成多个来搜（记得从右往左搜，别问为什么），这里的话我们直接搜索hash_sign即可，因为这个名字很独特，一般应该不会出现有其他不相关的东西也叫这个名字的情况。

   一搜就能定位到请求的位置了~

   ![通过搜索路径方式定位](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/6.png?x-oss-process=style/weixin)

2. 搜索你要找的参数

   比如这里我们需要找的是sign这个参数，可以直接搜索"sign"（注意带上双引号），但如果结果很多，而且还都很像生成/设置sign的地方的话，可以搜一些别的比较独特的参数，比如这里出现的model、brand之类的在代码中一般不会经常出现的词。

   由于这个DEMO APP比较简单，所以直接搜索"sign"就能定位到设置值的位置了~

   ![通过搜索参数名方式定位](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/7.png?x-oss-process=style/weixin)

定位到了代码位置之后我们就可以开始看代码了，从搜到的结果中我们可以看到生成sign、设置sign、设置路径的代码都在这个l方法下，然后我们来从设置sign的位置开始从下往上分析，这样代码的逻辑会更容易看懂一些。

![定位到的代码](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/8.png?x-oss-process=style/weixin)

这里我将代码中的关键点都做了标记，你可以按着旁边标注的序号跟着我一起来看这个代码。

首先这个aVar4.a有两个地方出现了，但是传入的第二个参数都是stringBuilder2，而下面那里是直接设置了一个空值进去，显然不是我们想要找的，所以我们可以忽略掉下面的那一行带有sign关键词的代码，直接看标注了1的那一行。

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/9.png?x-oss-process=style/weixin)

选中stringBuilder2这个变量，可以看到它的值是从上面那个stringBuilder3.toString()得到的，接着看看stringBuilder3的生成，for循环这里做了什么操作看不懂，但是可以看到上面有个很显眼的字符串"MD5"。那么我们可以大胆地猜测一下，这个stringBuilder3实际上就是做了个MD5操作而已，与我们最开始抓包时的猜测相同，直接往上看看Hash前的字符串长啥样，然后测试一下吧，不行的话再回来看。

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/10.png?x-oss-process=style/weixin)

从前面MD5操作的位置可以看到digest方法里用到的参数又是一个叫做stringBuilder2的变量，继续往上看就能看到实际上是从stringBuilder.toString()那得到的，那么这个stringBuilder又是怎么来的呢？从代码中我们可以看出似乎是for一个TreeMap然后把每一个key和value组成key=value的格式写入stringBuilder中，如果stringBuilder里已经有值的话还会添加&符号，那么这最终出来的东西可以联想到的是什么？对！就是queryString那部分，只不过它的参数是被排过序的（因为TreeMap会自动进行排序）。

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/11.png?x-oss-process=style/weixin)

然后我们再往上面看，验证一下想法正不正确，可以看到最源头的地方是个HashMap，被put进去的都是我们抓包时看到的参数。

---

现在我们就把这个sign的生成逻辑给理清楚了，其实它就是个按照参数名排过序的queryString进行了一次MD5操作后的产物，接下来我们只需要在代码中实现这个生成逻辑就行了，在Python中，你可以使用它自带的官方库hashlib来对一个字符串做MD5操作。

![](https://oss.crawler-lab.com/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E9%81%87%E5%88%B0APP%E7%9A%84%E8%AF%B7%E6%B1%82%E6%9C%89%E5%8A%A0%E5%AF%86%E5%8F%82%E6%95%B0%E6%97%B6%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E5%88%9D%E7%BA%A7%E7%AF%87-%E5%B8%B8%E8%A7%84%E6%A8%A1%E5%BC%8F%E3%80%91/assert/12.png?x-oss-process=style/weixin)

那么我们写一段代码模拟请求一下试试，sign确实可以通过校验，说明我们生成的sign是可以使用的，至此，加密参数破解完成。

提示：建议实际操作中不要这么测试，容易触发反爬。可以先拿抓包得到的参数生成一遍对比一下，如果一样则说明生成的sign没有问题。

---

这个时代各种东西变化太快，而网络上的垃圾信息又很多，你需要有一个良好的知识获取渠道，很多时候早就是一种优势，所以还不赶紧关注我的公众号并置顶/星标一波。

发送消息“APP加密参数破解初级篇代码”到我的公众号【小周码字】即可获得demo代码和APP的下载地址~

