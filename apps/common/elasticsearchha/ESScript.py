#!/usr/bin/env python

class ESMetaData:
    DictA={
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1,
            "analysis": {
                "analyzer": {
                    "ik": {
                        "tokenizer": "ik_max_word"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "address_ip": {
                    "type": "text"
                },
                "beat": {
                    "type": "text"
                },
                "client_port": {
                    "type": "text"
                },
                "department": {
                    "type": "text",
                    "analyzer": "ik",
                    "search_analyzer": "ik_max_word"
                },
                "display_name": {
                    "type": "text"
                },
                "es_id": {
                    "type": "text",
                    "index": "true"
                },
                "exception_info": {
                    "type": "text",
                    "analyzer": "ik",
                    "search_analyzer": "ik_max_word"
                },
                "log_code_info": {
                    "type": "text"
                },
                "logtype": {
                    "type": "integer"
                },
                "media_name": {
                    "type": "text"
                },
                "media_type": {
                    "type": "integer"
                },
                "operate_desc": {
                    "type": "text",
                    "analyzer": "ik",
                    "search_analyzer": "ik_max_word"
                },
                "operate_used_time": {
                    "type": "text"
                },
                "operator_info": {
                    "type": "text",
                    "analyzer": "ik",
                    "search_analyzer": "ik_max_word"
                },
                "operator_ip": {
                    "type": "text"
                },
                "operator_time": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "source": {
                    "type": "text"
                },
                "source_address": {
                    "type": "text"
                },
                "tenantId": {
                    "type": "text"
                }
            }

        }
    }





   
