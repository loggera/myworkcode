import json


def is_json(text):
    try:
        content = json.loads(text)
        return content
    except:

        return False


def is_json_data(text, api_rep):
    try:
        jd = json.loads(text)
        return True, jd
    except ValueError:
        api_rep['status'] = 'failed'
        api_rep['message'] = '数据转换成json失败'
        return False, api_rep
