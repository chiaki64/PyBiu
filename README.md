# PyBiu
噫

## 这是什么
这是一个 Biu.Moe 的音乐上传器，使用 Python 编写。

## 它有什么特点
* 命令行上传 
 * 单个音乐文件
 * 单个文件夹的音乐文件
* 自己看不懂的杂乱代码
* 一堆不知道怎么出现的BUG

## 依赖

* Python>=3.3 || Python>=2.7 (May not work under the python version, Who knows?\_(:3」∠)\_\
* requests>=2.9
* pycurl>=7.19
* ffmpeg

## 食用方法

### 初始化[重要]
不带任何参数执行一下run.yp,会提示输入 uid(用户UID) 和 key(用户密钥),然后会自动生成配置文件 .env ,在正常时候请不要修改它.

    python run.py
   

### 上传单首音乐
可以使用相对路径(相对run.py的路径)或者绝对路径，同时如果文件名含有**特殊字符**请使用双引号将文件名包括起来.

    python run.py -f "/music/夢想歌.flac"


### 上传整个文件夹的音乐
会遍历整个文件夹的音乐文件(一层),然后利用单线程提交 (对于 python2.7 此选项或许不太稳定)

    python run.py -d "/music/"
    

### 其他
帮助

    python run.py -h
    

## 任务列表
* ~~适配Windows~~ 
* 适配Linux & MacOS
* 多线程
* 添加文件备注
* ~~进度条~~
