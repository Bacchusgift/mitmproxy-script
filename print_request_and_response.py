# -*- coding:utf-8 -*-
# !usr/bin/python3

import base64
import mitmproxy.http
from mitmproxy import ctx
import json

from decrypt_encrypt_util import decrypt

'''
  打印请求和返回值，适用于直接抓iOS包的场合，发送一个加密请求，携带 encrypt-version 和 timestamp，使用此类会自动帮你打印解密后的加密参数
  接收到后端加密返回后，也会自动解密后在控制台打印，对源请求无感，还可以做到配置钉钉直接把请求和返回值甩到钉钉群里（待升级）
'''


class PrintRequestAndResponse:

    @staticmethod
    def request(flow: mitmproxy.http.HTTPFlow):
        if "v1" == flow.request.headers.get("encrypt-version"):
            content = flow.request.get_content()
            timestamp = flow.request.headers.get("timestamp")
            json_data = json.loads(content)
            json_data = json.loads(decrypt(timestamp, json_data['data']))
            result = json.dumps(json_data)
            ctx.log.warn("request : %s" % result)

    @staticmethod
    def response(flow: mitmproxy.http.HTTPFlow):
        if flow.request.headers.get("encrypt-version") == "v1":
            content = flow.response.get_content()
            timestamp = flow.request.headers.get("timestamp")
            json_data = json.loads(content)
            ctx.log.warn("json_data : %s" % json_data['content'])
            json_data['content'] = json.loads(decrypt(timestamp, json_data['content']))
            json_data['msg'] = base64.b64decode(json_data['msg']).decode("utf-8")
            result = json.dumps(json_data)
            ctx.log.warn("response : %s" % result)
