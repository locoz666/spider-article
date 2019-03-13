今天在~~摸鱼~~逛V2EX的时候，有个[帖子](https://www.v2ex.com/t/493201)引起了我的注意

帖子内容：

> 视频链接加密之后是这样的：
> lxxt6jIID2Byq541xEB6F3u71bYaE5A/A-1dMFS4o9mx8uzpm81KxH25u1E29:Cl7Wg|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_:hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_/hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_\hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_.hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7__hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_AhQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7bhQW5e|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7ChQW5e|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7dhQW5e
> 网站链接在这：
> <http://www.tvsky.tv/Industry/Show/278/33875/>
> 请问是什么加密， 求助。

作为一个助人为乐的好青年，当然要顺手帮楼主看一下啦😳

打开这个网站看看，这是一个用Flash播放器加载并播放视频的页面，传入播放器的参数如帖中所述是有加密的

![使用Chrome的开发者工具查看播放器元素](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/1.png)

传入播放器的参数：

```
flvurl=lxxt6jIID2Byq541xEB6F3u71bYaE5A/A-1dMFS4o9mx8uzpm81KxH25u1E29:Cl7Wg|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_:hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_/hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_\hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_.hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7__hQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_AhQ5Ue|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7bhQW5e|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7ChQW5e|lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7dhQW5e&isautoplay=1&adswf=
```

抓包发现有一个.flv文件的链接，应该就是播放器加载出来的视频

![使用Chrome的开发者工具查看网络请求](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/2.png)

全局搜索这个URL的部分内容是搜不到的，判断出这个URL应该是在播放器中对传入的flvurl参数进行解密，然后再加载出视频

![](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/3.png)

---

**那么，遇到这种情况的时候我们应该怎么做才能破解出这个解密URL的过程呢？**

首先，我们需要将这个页面上的Flash播放器给逆向一下，就像在爬HTML5视频网站碰到加密参数时逆向JavaScript一样。

但是Flash播放器是一个被编译后的.swf文件，我们并不能像JavaScript那样直接看到代码，需要先进行反编译。

是时候祭出**JPEXS**了，在GitHub上可以找到，传送门：https://github.com/jindrapetrik/jpexs-decompiler/releases

下载完后启动它，界面长这样：

![JPEXS启动界面](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/4.png)

默认的语言是英语，可以切换成中文，在Settings – Change language里选择

![JPEXS切换成中文](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/5.png)

然后我们将这个播放器的.swf文件给下载下来，并使用JPEXS打开

播放器文件地址在源页面的HTML中可以看到是：

```
http://www.tvsky.tv/FlvPlay/Playerx.swf
```

![用JPEXS打开播放器文件](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/6.png)

然后我们有两种方式快速定位到可能存在解密代码的位置

第一种方式：

打开后找到脚本组下frame1的DoAction脚本

![](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/7.png)

点击后窗口右侧会反编译这个脚本的内容，并展示出反编译出来的AS源代码和P代码（类似于汇编语言），我们只需要看AS源代码的部分就行了

![播放器加载状态](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/8.png)

根据在网页中播放器的样子，在加载时会有一个“正在加载Flv文件”的字样，直接按Ctrl+F搜索它

![搜索反编译出来的代码中的字符串](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/9.png)

找到init函数



第二种：

随便找一个脚本打开，然后按Ctrl+Shift+F打开全局搜索，同样搜索“正在加载Flv文件”

![](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/10.png)

![全局搜索](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/11.png)

---

快速定位出加载视频部分后，根据init函数这里的代码可以看出，_loc2_就是被传进播放器的flvurl

![](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/12.png)

那么下面的这部分就是它的解密操作了

```actionScript
# init部分:
_flvurl = _loc2_.split("|");
var _loc1_ = 0;
while(_loc1_ < _flvurl.length)
{
   _flvurl[_loc1_] = Pass2Str(_flvurl[_loc1_]);
   _loc1_ = _loc1_ + 1;
}

var PwdStr = "AbCdEfGhIjKlMnOpQrStUvWxYzaBcDeFgHiJkLmNoPqRsTuVwXyZ1234509876-_.\\/:";
var PwdStrRan = "12345678987654321";
var _PwdLen = 4;
var _PwdAddLen = 4;

function Pass2Str(Str)
{
   var _loc2_ = "";
   var _loc3_ = "";
   var _loc4_ = 0;
   var _loc1_ = 1;
   while(_loc1_ <= Str.length)
   {
      _loc2_ = Str.substr(_loc1_,1);
      if(_loc1_ % (_PwdLen + 1) != 0)
      {
         _loc3_ = _loc3_ + NumS(_loc2_,_loc4_);
      }
      else
      {
         _loc4_ = parseInt(_loc2_);
      }
      _loc1_ = _loc1_ + 1;
   }
   return _loc3_;
}
function NumS(s, _PwdAddLen1)
{
   var _loc1_ = PwdStr.indexOf(s);
   _loc1_ = _loc1_ - (_PwdAddLen + _PwdAddLen1 - 1);
   if(_loc1_ <= 0)
   {
      return PwdStr.substr(_loc1_ + PwdStr.length,1);
   }
   return PwdStr.substr(_loc1_,1);
}
```

然后将反编译出来的ActionScript代码的解密URL部分改写成Python代码：

```python
# http://www.tvsky.tv/Industry/Show/278/33875/ 的视频url解密部分
# 为方便对照AS代码阅读，这里只对反编译出来的AS代码直接进行“翻译”，没有使用Python的一些更简洁的写法

_pwd_len = 4
_pwd_add_len = 4
pwd_str = "AbCdEfGhIjKlMnOpQrStUvWxYzaBcDeFgHiJkLmNoPqRsTuVwXyZ1234509876-_.\\/:"


def decode(flv_url: str):
    """
    function init()
    {
       ......
       var _loc2_ = flvurl;
       ......
          _flvurl = _loc2_.split("|");
          var _loc1_ = 0;
          while(_loc1_ < _flvurl.length)
          {
             _flvurl[_loc1_] = Pass2Str(_flvurl[_loc1_]);
             _loc1_ = _loc1_ + 1;
          }
       ......
    }
    :param flv_url: flash参数里的flvurl部分的value
    :return: 解密后视频url列表
    """
    new_flv_url = flv_url.split("|")
    _loc1_ = 0
    while _loc1_ < len(new_flv_url):
        new_flv_url[_loc1_] = pass2str(new_flv_url[_loc1_])
        _loc1_ += 1
    return new_flv_url


def pass2str(str_: str):
    """
    function Pass2Str(Str)
    {
       var _loc2_ = "";
       var _loc3_ = "";
       var _loc4_ = 0;
       var _loc1_ = 1;
       while(_loc1_ <= Str.length)
       {
          _loc2_ = Str.substr(_loc1_,1);
          if(_loc1_ % (_PwdLen + 1) != 0)
          {
             _loc3_ = _loc3_ + NumS(_loc2_,_loc4_);
          }
          else
          {
             _loc4_ = parseInt(_loc2_);
          }
          _loc1_ = _loc1_ + 1;
       }
       return _loc3_;
    }
    :param str_: 加密的url字符串
    :return: 解密后的url字符串
    """
    _loc1_ = 1
    _loc3_ = ""
    _loc4_ = 0
    while _loc1_ <= len(str_):
        _loc2_ = str_[_loc1_ - 1]
        if _loc1_ % (_pwd_len + 1) != 0:
            _loc3_ = _loc3_ + num_s(_loc2_, _loc4_)
        else:
            _loc4_ = int(_loc2_) if _loc2_.isdigit() else 0
        _loc1_ = _loc1_ + 1
    return _loc3_


def num_s(s, _pwd_add_len1):
    """
    function NumS(s, _PwdAddLen1)
    {
       var _loc1_ = PwdStr.indexOf(s);
       _loc1_ = _loc1_ - (_PwdAddLen + _PwdAddLen1 - 1);
       if(_loc1_ <= 0)
       {
          return PwdStr.substr(_loc1_ + PwdStr.length,1);
       }
       return PwdStr.substr(_loc1_,1);
    }
    """
    _loc1_ = pwd_str.index(s)
    _loc1_ = _loc1_ - (_pwd_add_len + _pwd_add_len1 - 1)
    if _loc1_ <= 0:
        return pwd_str[_loc1_ + len(pwd_str) - 1]
    return pwd_str[_loc1_ - 1]


if __name__ == '__main__':
    url_list = decode(
        "lxxt6jIID2Byq541xEB6F3u71bYaE5A/A-1dMFS4o9mx8uzpm81KxH25u1E29:Cl7Wg|"
        "lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_:hQ5Ue|"
        "lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_/hQ5Ue|"
        "lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_\hQ5Ue|"
        "lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_.hQ5Ue|"
        "lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7__hQ5Ue|"
        "lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7_AhQ5Ue|"
        "lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7bhQW5e|"
        "lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7ChQW5e|"
        "lxxt4hGGB6F3u763zGD9i0X_4EBDh7CAC.6Irkx6q7oz7TYOL2uErB25u1E7dhQW5e"
    )
    print(url_list)
```

执行一下看看效果

![](https://raw.githubusercontent.com/locoz666/spider-article/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/assets/13.png)

BOOM!

[**代码和播放器原文件传送门**](https://github.com/locoz666/spider-article/tree/master/%E5%BD%93%E4%BD%A0%E5%86%99%E7%88%AC%E8%99%AB%E6%97%B6%E9%81%87%E4%B8%8AFlash%2B%E5%8A%A0%E5%AF%86%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E5%BC%8F/src)

---

如果这篇文章有帮到你，请大力点赞，谢谢~~ 欢迎关注我的知乎账号[loco_z](https://www.zhihu.com/people/loco_z)和我的知乎专栏[《手把手教你写爬虫》](https://zhuanlan.zhihu.com/webspider)，我会时不时地发一些爬虫相关的干货和黑科技，说不定能让你有所启发。
