怎么使用？
---
这个脚本是配合抓包工具 mitmproxy 使用的， 现在默认有这样一样个请求、返回示例

请求值：会根据header里的头的timestamp来进行加密，用 AES-CBC-PKCS5padding 来加密
返回值：也是如此

安装 mitmproxy

```shell script
 pip3 install mitmproxy
```
安装项目依赖

```shell script 
 pip3 install -r requirements.txt
```
启动main文件 【默认使用的是打印请求解密后的值和返回解密后的值】
如需更改可以更改 main.py里的 addons 
如下：

```
addons = [
    decrypt_request.DecryptRequest()
]
```

启动抓包脚本 ，可以从控制台看请求打印值了【后文有脚本使用说明】
```shell script
 mitmweb -s main.py
```


---

### mitmproxy抓包指南

- 程序默认端口是8080，如有冲突，命令要指定端口启动
```shell script
mitmweb -s main.py -p 端口号
```

- 程序抓https包需要安装证书
    1. 手机连上代理后，浏览器打开 mitm.it  （PC、Mac同理，Mac稍微麻烦一点，自己百度吧）
    2. 安装对应的证书，信任此证书
    3. 可以开始抓包啦
  
- 遇到的问题`ImportError: No module named Crypto.Cipher`
```
sudo pip uninstall crypto
sudo pip uninstall pycrypto
sudo pip install pycrypto