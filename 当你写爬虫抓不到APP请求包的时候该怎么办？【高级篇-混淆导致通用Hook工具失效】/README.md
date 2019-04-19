催更的大哥们别打我，我回来更新了😂😂😂。

**提示：因为高级篇以后的APP将无法使用很通用的方式处理，每种类型甚至是每个APP的反抓包处理方式都会有差别，所以这个系列以后会以【高级篇-具体类型】的形式来写。**

这篇文章的主要内容是解决在遇到APP没有使用Android自带的HTTP客户端进行请求，并且对HTTP客户端的代码进行了混淆，导致通用工具JustTrustMe失效的问题。而中级篇中除了JustTrustMe以外的所有方法也都会对这种情况束手无策，原因是中级篇中的1、3、4方法本质上针对的是Android 7.0+系统增加的SSL Pinning方案，而无法对各个HTTP客户端自己实现的检测方案生效。~~（听说有个叫车速拍的APP就是这种类型呢）~~

那么应该怎么做才能抓到这类APP的包呢？很简单，依然是使用JustTrustMe之类的Hook工具就好了，只不过我们需要针对混淆后的名字对原来Hook的部分进行特殊处理。

---

这里我专门写了一个样例APP来进行演示（别抓我，我什么都不知道），这个APP做的事情就是在你点击了按钮之后，对百度首页发起一次请求，但是这个请求在没有破解SSL Pinning的正常情况下是不可能成功的，因为我设置的是一个随便输入的证书哈希，所以在请求的时候会因为正常的证书哈希与我随便输入的哈希不同导致出现请求失败的情况。

![样例APP代码](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/1.png)

这个APP我已经编译好放到GitHub上了，有两个版本，一个是对代码进行过混淆的，一个是没混淆的，文末会有下载地址，读者可以下载下来自己玩玩。

![两个编译好的APK](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/2.png)

开始演示之前说一下测试机的配置吧，这里用的测试机是Android 8.1.0的，已经Root+Xposed，同时已经安装并激活了JustTrustMe。

![测试机系统信息](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/3.png)

![Xposed模块管理界面-JustTrustMe已开启](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/4.png)

---

我们先来看一下没混淆过代码的版本，装上之后打开它，然后点击“点击发送请求”按钮。

![样例APP界面](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/5.png)

![请求成功](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/6.png)

不出意外的话会出现请求成功的字样，如果出现请求失败的话可能是你网络问题，证书问题会提示“证书验证失败”。

接下来我们看看混淆过代码的版本，操作同上。

![证书验证失败](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/7.png)

这次就是证书验证失败了，JustTrustMe并没有正常生效。

---

我们将这两个APK都放到Jadx中反编译一下看看。

![在Jadx中反编译两个样例APK](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/8.png)

可以看到混淆过的版本里，okhttp3下的所有类名已经变成了abcd这种名字。

然后我们来看一下JustTrustMe的代码。

![JustTrustMe代码中Hook okhttp3的证书验证部分](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/9.png)

可以看到它的代码中是对okhttp3.CertificatePinner类下的check方法进行Hook的，这个CertificatePinner类和check方法在没混淆过的APK中可以很清楚地看到。

![反编译检测代码1](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/10.png)

![反编译检测代码2](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/11.png)

那么现在JustTrustMe面对混淆后的版本就失效的原因已经很清晰了，因为它找不到这个okhttp3.CertificatePinner.check，所以根本就不可能Hook到检测方法，自然不会有任何效果。

所以...应该怎么办呢？这里依然是给出多种方法供读者选择：

1. 修改JustTrustMe代码中Hook的类名和方法名然后重新编译

很简单，找到对应的检测方法，把JustTrustMe代码中Hook的className和methodName改成混淆后的名字即可，比如在这个混淆后的样例APP里，okhttp3.CertificatePinner.check变成了okhttp3.f.a。

![反编译检测代码-混淆后](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/12.png)

我们修改JustTrustMe中的Hook部分，同样改为f和a。

![JustTrustMe对okhttp3的证书检测Hook](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/13.png)

![修改JustTrustMe对okhttp3的证书检测Hook](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/14.png)

改完之后编译一下，安装到手机上替换原来的就好了。

2. 使用Frida进行Hook

这个方法比方法1要更方便、更直接一些，因为需要的时候直接修改脚本马上就能用，不需要重新编译、重启手机或APP，这里直接拿[瘦蛟舞](https://github.com/WooyunDota)大佬写的[解除SSL Pinning脚本](https://github.com/WooyunDota/DroidSSLUnpinning/blob/master/ObjectionUnpinningPlus/hooks.js)修改一下，同样是修改Hook okhttp3.CertificatePinner.check的部分，改成混淆后的名字即可。

![修改瘦蛟舞的ObjectionUnpinningPlus脚本](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/15.png)

3. 魔改JustTrustMe，增加一个可以在运行时根据情况调整每种HTTP客户端的SSL Pinning检测部分的类名和方法名的功能

这个我暂时没空弄，感兴趣的同学可以自己实现一下。

4. 魔改JustTrustMe，对Hook部分增加动态适配功能，做到即使开发者对代码进行了混淆也能自动找到真实的检测类和方法

同上，实现方式可以参考[微信巫师框架部分](https://github.com/Gh0u1L5/WechatSpellbook)的自动适配代码，实现以后理论上来讲是最方便的办法之一，因为是完全自动的操作，不需要人工介入。

5. 修改反编译APP得到的代码再打包回去

我觉得应该没人会用这么蠢的办法吧...用Hook的方式做起来要方便太多了。



选择任意一种方法操作后，再打开混淆版本的APP就可以正常请求了。

---

这时候可能会有同学要问了，怎么样知道APP用的是哪个HTTP客户端？又怎么样快速定位混淆后的检测方法位置呢？

很简单，我们先关掉破解工具，连上代理然后抓个包看看混淆版本APP的请求。

![抓包查看请求](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/16.png)

![User-Agent部分](https://github.com/locoz666/spider-article/raw/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/assert/17.png)

和平时遇到SSL Pinning的情况一样，这里只会抓到一个CONNECT请求，注意右边的headers，从User-Agent中可以看出这个APP使用的是okhttp3，那么我们在混淆后的代码中定位检测部分代码的位置时，就只需要对照着okhttp3的原始代码来找就好了（其他HTTP客户端同理）。当然了，也不排除有些APP会把User-Agent改掉，如果从User-Agent上看不出来的话，那就看一下反编译出来的源代码部分结构，看看有没有像okhttp3之类的这种特别明显的HTTP客户端的名字，有的话就把它干掉就好了。

[**点我查看文中样例APP代码|下载编译好的样例APP**](https://github.com/locoz666/spider-article/tree/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%8A%93%E4%B8%8D%E5%88%B0APP%E8%AF%B7%E6%B1%82%E5%8C%85%E7%9A%84%E6%97%B6%E5%80%99%E8%AF%A5%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F%E3%80%90%E9%AB%98%E7%BA%A7%E7%AF%87-%E6%B7%B7%E6%B7%86%E5%AF%BC%E8%87%B4%E9%80%9A%E7%94%A8Hook%E5%B7%A5%E5%85%B7%E5%A4%B1%E6%95%88%E3%80%91/example)

---

最近还会有另外两篇文章发布，分别是【介绍APP逆向中的常用工具的】和【写爬虫遇到APP的请求有加密参数的解决方式的】，尽情期待。~~（听说点赞越多码字速度越快）~~

欢迎提供更多高级篇的素材，在评论或私信里告知我都可以。

如果这篇文章有帮到你，请大力点赞，谢谢~~ 欢迎关注我的知乎账号[loco_z](https://www.zhihu.com/people/loco_z)和我的知乎专栏[《手把手教你写爬虫》](https://zhuanlan.zhihu.com/webspider)，我会时不时地发一些爬虫相关的干货和黑科技，说不定能让你有所启发。