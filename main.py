"""
该文件用于测试chatpdf接口
"""
import requests


def addExample():
    files = [
        ('file', ('file', open('./pdf/A Surrogate Modeling and Adaptive Sampling.pdf', 'rb'),
                  'application/octet-stream'))
    ]
    headers = {
        'x-api-key': 'sec_VL3Ak8ZftZYr6hVwB41LxSzGUywUiMd5'
    }

    res = requests.session()

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    if response.status_code == 200:
        print('Source ID:', response.json()['sourceId'])
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)

    res.keep_alive = False


def chatExample():
    headers = {
        'x-api-key': 'sec_IB4utx616TgY5AAW8cupSsXgOTIre4oa',
        "Content-Type": "application/json",
    }

    data = {
        'sourceId': "src_P8IxqX8OQoLjwa1h7fsxd",
        'messages': [
            {
                'role': "user",
                'content': "这篇文章的大致内容是什么",
            }
        ]
    }

    res = requests.session()

    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    if response.status_code == 200:
        print('Result:', response.json()['content'])
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)

    res.keep_alive = False


def deleteExample():
    headers = {
        'x-api-key': 'sec_VL3Ak8ZftZYr6hVwB41LxSzGUywUiMd5',
        'Content-Type': 'application/json',
    }

    data = {
        'sources': ['src_DmFYQswT31vGBWdcKkYkT'],
    }

    res = requests.session()

    try:
        response = requests.post(
            'https://api.chatpdf.com/v1/sources/delete', json=data, headers=headers)
        response.raise_for_status()
        print('Success')
    except requests.exceptions.RequestException as error:
        print('Error:', error)
        print('Response:', error.response.text)

    res.keep_alive = False


if __name__ == '__main__':
    chatExample()