# -*- coding:utf-8 -*-
# !usr/bin/python3

import base64
import mitmproxy.http
from mitmproxy import ctx
import json

from decrypt_encrypt_util import encrypt, decrypt

"""
 修改请求和返回值，适用于postman等场合，发送一个普通请求，携带 encrypt-version 和 timestamp，使用此类会自动帮你生成加密参数发送到后端
 接收到后端加密返回后，自动解密后展示，对测试无感
"""


class ModifyRequestAndResponse:

    @staticmethod
    def request(flow: mitmproxy.http.HTTPFlow):
        if "v1" == flow.request.headers.get("encrypt-version"):
            ctx.log.info("catch search body: %s" % flow.request.get_content().decode('utf-8'))
            content = flow.request.get_content()
            timestamp = flow.request.headers.get("timestamp")
            encrypt_data = encrypt(timestamp, json.dumps(json.loads(content)))
            request_body = {"data": encrypt_data.decode()}
            ctx.log.warn("modify request: %s" % json.dumps(request_body))
            flow.request.set_content(bytes(json.dumps(request_body), 'utf-8'))

    @staticmethod
    def response(flow: mitmproxy.http.HTTPFlow):
        if flow.request.headers.get("encrypt-version") == "v1":
            content = flow.response.get_content()
            timestamp = flow.request.headers.get("timestamp")
            json_data = json.loads(content)
            json_data['msg'] = base64.b64decode(json_data['msg']).decode("utf-8")
            json_data['content'] = json.loads(decrypt(timestamp, json_data['content']))
            result = json.dumps(json_data)
            ctx.log.info("json %s:" % json_data)
            ctx.log.info("result %s:" % result)
            flow.response.set_content(bytes(json.dumps(json_data), 'utf-8'))
