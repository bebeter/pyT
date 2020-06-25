# -*- coding: utf8 -*-
import json

import requests

msg = {
  "host": {
    "bk_supplier_account": "0"
  },
  "data": {
    "meta": {
      "model": {
        "bk_classification_id": "middelware",
        "bk_obj_id": "test1",
        "bk_obj_name": "test1n",
        "bk_supplier_account": "0"
      },
      "fields": {
        "bk_inst_name": {
          "bk_property_name": "实例名",
          "bk_property_type": "longchar"
        },
        "field1": {
          "bk_property_name": "field1",
          "bk_property_type": "longchar"
        }
      }
    },
    "data": {
      "bk_inst_key": "test1",
      "field1": "field 1",
      "bk_inst_name": "inst1"
    }
  }
}
data = {
    "name": "middleware",
    "mesg": json.dumps(msg)
}

host = "http://172.16.228.114:12140"


url = "http://127.0.0.1:12140"
response = requests.request("POST", host, data=json.dumps(data))
print(response.status_code, response.text)