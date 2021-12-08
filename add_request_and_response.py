# -*- coding:utf-8 -*-
# !usr/bin/python3

import base64
import mitmproxy.http
from mitmproxy import ctx
import json
from decrypt_encrypt_util import decrypt

class AddRequestAndResponse:

    @staticmethod
    def request(flow: mitmproxy.http.HTTPFlow):
        if "v1" == flow.request.headers.get("encrypt-version"):
            header_json = flow.request.headers
            content = flow.request.get_content()
            if "v1" == header_json.get('encrypt-version'):
                timestamp = header_json.get("timestamp")
                ctx.log.warn("timestamp_cls: %s" % type(timestamp))
                ctx.log.warn("timestamp_str: %s" % timestamp)
                content_json = json.loads(content)
                content_json = json.loads(decrypt(timestamp, content_json['data']))
                # 设置解密之后的数据
                header_json.setdefault("request_content_decrypt", json.dumps(content_json))
                flow.request.headers = header_json

    @staticmethod
    def response(flow: mitmproxy.http.HTTPFlow):
        header_json = flow.response.headers
        if "v1" == header_json.get("encrypt-version"):
            timestamp = flow.request.headers.get("timestamp")
            content = flow.response.get_content()
            content_json = json.loads(content)
            temp_content_json = content_json
            # 拼接解密以后的数据
            if 'msg' in temp_content_json:
                temp_content_json['msg'] = base64.b64decode(content_json['msg']).decode("utf-8")
            if 'content' in temp_content_json:
                temp_content_json['content'] = json.loads(decrypt(timestamp, content_json['content']))
            # 设置解密之后的数据
            header_json.setdefault("response_content_decrypt", json.dumps(temp_content_json))
            flow.response.headers = header_json
