# -*- coding:utf-8 -*-
# !usr/bin/python3

import base64
import mitmproxy.http
from mitmproxy import ctx
import json
from decrypt_encrypt_util import decrypt

path_list = [
    "/user/quickRegV3",
    "/user/userRegV3",
    "/user/telRegCode",
    "/user/telReg",
    "/oauth/authorize",
    "/user/sendCode",
    "/user/changeUserInfo",
    "/oauth/notice",
    "/user/gift_detail",
    "/user/gift_num",
    "/user/captcha/userRegV3",
    "/noncore/redirect"
]


# 是否需要解密
def need_decrypt(url) -> bool:
    if 'api/v2' in url:
        return True
    return False


# 是否需要access_token加密
def need_access_token_encrypt(path) -> bool:
    for temp_path in path_list:
        if temp_path in path:
            return False
    return True


class AddApiV2RequestAndResponse:

    @staticmethod
    def request(flow: mitmproxy.http.HTTPFlow):
        if need_decrypt(flow.request.url):
            header_json = flow.request.headers
            content_str = flow.request.get_content().decode("utf-8")
            timestamp = header_json.get("timestamp")
            if need_access_token_encrypt(flow.request.url):
                access_token = header_json.get("access-token")
                ext_info = header_json.get("ext-info")
                ext_info = decrypt(timestamp, ext_info)
                access_token = decrypt(ext_info, access_token)
                content_json = json.loads(decrypt(access_token, content_str))
                header_json.setdefault("request_content_decrypt", json.dumps(content_json))
                ctx.log.warn("%s的请求数据是: %s" % (flow.request.url, json.dumps(content_json)))
                flow.request.headers = header_json
            else:
                ext_info = header_json.get("ext-info")
                # 通过time解密出ext_info
                ext_info = decrypt(timestamp, ext_info)
                # content_str = decrypt(ext_info, content_str)
                content_json = json.loads(decrypt(ext_info, content_str))
                header_json.setdefault("request_content_decrypt", json.dumps(content_json))
                # ctx.log.warn("解密数据2: %s" % content_str)
                ctx.log.warn("%s的请求数据是: %s" % (flow.request.url, json.dumps(content_json)))
                flow.request.headers = header_json

    @staticmethod
    def response(flow: mitmproxy.http.HTTPFlow):
        if need_decrypt(flow.request.url):
            header_json = flow.response.headers
            request_header_json = flow.request.headers
            content_str = flow.response.get_content().decode("utf-8")
            timestamp = request_header_json.get("timestamp")
            content_json = json.loads(decrypt(timestamp, content_str))
            header_json.setdefault("response_content_decrypt",
                                   json.dumps(content_json).encode('utf-8').decode('unicode_escape'))
            ctx.log.warn("%s的响应数据是: %s" % (flow.request.url, json.dumps(content_json)))
            flow.response.headers = header_json
