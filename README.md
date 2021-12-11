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