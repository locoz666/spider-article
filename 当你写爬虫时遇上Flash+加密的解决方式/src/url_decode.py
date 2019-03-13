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
