# -*- coding:utf-8 -*-
# !usr/bin/python3

import modify_request_and_response
import print_request_and_response
import add_request_and_response, api_v2_request_response

addons = [
    add_request_and_response.AddRequestAndResponse(),
    api_v2_request_response.AddApiV2RequestAndResponse()
    # print_request_and_response.PrintRequestAndResponse()
    # modify_request_and_response.ModifyRequestAndResponse()
]
