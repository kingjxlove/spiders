# spiders
#### 1. [爬取boss直聘上的Python岗位](https://github.com/kingjxlove/spiders/blob/master/spiders/zhipin.py)
    构造URL, 获取网页上的数据, 解析URL, 获取需要的信息存入字典
#### 2. [爬取蘑菇街网站上所有种类的商品(未去重)](https://github.com/kingjxlove/spiders/blob/master/spiders/mogujie_all.py)
    爬取蘑菇街网站上的所有商品比较复杂, 想获取全部的商品, 突破口就是商品的种类.
   - 1. 首先随便选取一个商品种类,点进去后,可以发现这里面直接就会出现很多商品
   - 2. 蘑菇街并没有使用url进行分页处理, 更多的数据是放在一个个XHR文件中的list.mogujie.com/search?
	(获取这个文件, 你可以使用Chrome打开开发者模式,在Network中, 你向下滑动, 页面就会加载新的元素, 带有数据的文件就找到了)
   - 3. 我们会发现这个文件后面跟的参数, 就是对应的商品的分类,有很大一部分参数是没用的, 所以可以自己剔除掉,方便后面自己构建URL. 我发现区分种类的参数是'fcid'后面跟的参数, 所以就去寻找该参数在哪里出现的.
   - 4. 分析得出, 商品种类应该是和首页里面的栏目里面的数据是对应的 所以去蘑菇街首页找到存放所有种类的'fcid'的文件(mce.mogucdn.com/jsonp/multiget/3?pids=110119), 这样就可以得到所有的种类了.
   - 5. 循环遍历,构造单个种类页面的URL. 同一种类的商品是通过改变page来实现页面加载的, 所以将页面page与种类fcid一起传入url, 就能得到商品的详细信息.
   - 6. 通过python连接数据库, 构造SQL语句,将爬取的内容存入数据库(数据量有点大,我最终爬了下来的数据共2107275条(未去重))
   ![蘑菇街所有商品数据](https://github.com/kingjxlove/img/blob/master/spiders_img/%E8%98%91%E8%8F%87%E8%A1%97%E6%95%B0%E6%8D%AE.png)
#### 3. [爬取虾米音乐排行榜前100的歌曲(下载)](https://github.com/kingjxlove/spiders/blob/master/spiders/xiami.py)
###### - [凯撒密码](https://github.com/kingjxlove/spiders/blob/master/spiders/kaisha.py)
	 通过URL打开虾米音乐的排行榜, 进入开发者模式, 找到歌曲信息的位置.
	 网页构成中, 有一个table里面的tr有'data-mp3'属性.
	 应该能猜到, 歌曲的数据应该就和这个有关系了, 但是这里面的文字杂乱无章, 很明显不是歌曲的直接URL
	 该地址是加密过的, 通过凯撒密码解密,能得到它真正的URL
	 获取到歌曲地址的url就能直接解析歌曲了, 然后通过二进制存储该数据, 就能把歌曲下载下来了
#### 4. [破解1KKK漫画的图像旋转点击验证](https://github.com/kingjxlove/spiders/blob/master/spiders/img_check.py)
![未点击时的验证码](https://github.com/kingjxlove/img/blob/master/spiders_img/1kkk%E9%AA%8C%E8%AF%81%E7%A0%81.png)

	 1KKK漫画网站, 登录注册时是通过点击动漫人物头像,使头像转正后完成验证. 每次点击, 图像会顺时针旋转90°.
	 但是电脑并不能自己识别图像的正反, 所以涉及到简单的机器学习.
	 首先去查看图像验证码的地址, 发现每个头像都是由四个不同方向的小图组成.
	 通过对图像地址的URL的反复调用,可以得到新的图像.所以, 循环执行url,尽可能得到验证码图库里面的头像.
	 裁剪获得小头像(和验证码中的头像等大), 通过代码去重, 去重的主要目的是为了提高代码的执行效率.
	 将所有的头像都转正. 通过selenium 模拟登录, 打开界面后截取,第一张小图, 然后和自己得到的正向头像图库一一对比.
	 如果有相同的图片,则说明验证码图片为正向, 不必旋转; 若比较完成后,没有相同的图片,模拟点击该图片一次.
	 后面三张验证码道理同上; 若旋转三次后, 验证都未通过, 则有可能是图库中的头像没有获取完全, 此时模拟点击换一组, 重新执行验证
![验证完成后的图片](https://github.com/kingjxlove/img/blob/master/spiders_img/1kkk%E9%AA%8C%E8%AF%81%E7%A0%81(%E6%AD%A3).png)
#### 5. [天天基金网3344法则筛选](https://github.com/kingjxlove/spiders/blob/master/spiders/jijin.py)
    通过3344法则，筛选优质基金（但是去年年底入的，筛的再好，也改不了我目前还是亏损状态的事实）
   ![天天基金网](https://github.com/kingjxlove/img/blob/master/%E5%A4%A9%E5%A4%A9%E5%9F%BA%E9%87%91%E7%BD%913344%E7%AD%9B%E9%80%89.png)
	
