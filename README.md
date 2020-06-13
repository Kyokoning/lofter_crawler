## Abstract

这是一个基于python的爬虫项目，它的目的在于抢救性保护同人tag和同人作者作品。

目前实现的功能：

- 两种模式
    - 根据提供的lofter id保存所有blog
    - 根据提供的lofter tag保存所有tag条目下可见的blog
- filter
    - 热度阈值
    - tag屏蔽
    - title寻找
    
todo list

- 根据lofter id保存用户所有喜欢的blog
- 还在梦里的的GUI界面

联系我：微博@黑化养乐多

不要用本项目代码做不好的事情！

## Quick Start

1. 安装依赖：

`pip install -r requirements.txt`

2. 根据需要修改`config/test.yaml`配置文件

配置选项|默认值|描述|示例
:-------:|:----:|-------|----
OUTPUT_DIR|output/|保存存档的地址(绝对地址/相对地址都ok)|output/tag
TYPE|tag|脚本运行模式，可选项有tag和USER，可以保存tag和保存user的blog|'tag'
TAG|[]|如果选择了tag运行模式，那么在括号里填入目标tag|\['tag1', 'tag2'\]
USER|[]|如果选择了USER运行模式，那么目标user|\['user1', 'user2'\]

------|target细节部分|-------|-------
PICTURE|true|blog是图片的话是否保存|true
ARTICAL|true|blog是文章的话是否保存|true
HOT_THRE|0|高于多少热度的文章被保存|50
TITLE| [] |标题中有什么内容的会被保存，这是list格式的配置，意味着可以有很多个与的目标|\['论坛体', 'abo'\]
TAG_PLUS| [] |文章的tag中要有什么才会被保存。同样是list格式配置| \['三十天挑战'\]
TAG_MINUS| [] |如果文章的tag有什么，就不会被保存。同样是list格式配置 | \['游戏截图', '日常'\]

3. 运行脚本

`python tool/crawler.py --cfg config/test.yaml`

结果会产生很多html文件和一个log文件

- log文件的名字是`TYPE`-`name/id`-时间.log
- blog保存格式为html，名字是\[`blog作者名`\] `blog标题`_`lofter相对地址`.html

## 运行示例

#### ①User模式（白的毛熊：https://coldiron.lofter.com/）

![image.png](https://i.loli.net/2020/06/13/cJVedgBUXx6rFQ3.png)

![image.png](https://i.loli.net/2020/06/13/fXuybjWVKoerRSH.png)

#### ②tag模式

测试tag1：kj 

    432参与，实际爬得338

参与tag数是不算后面加入的tag，所以爬虫爬下来会少（测试了一432参与的tag，实际爬完是338）

![image.png](https://i.loli.net/2020/06/13/n3vO7tfBC8cFGSm.png)

测试tag2：sc

![范例.gif](https://i.loli.net/2020/06/13/IY3E6POxaMuemD7.gif)