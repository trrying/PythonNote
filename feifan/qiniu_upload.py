from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config


def upload_imgs(local_file, key):
    access_key = 'VBvN33BnrqcaAqrbOHLD4EbTuIwxwjA_VSdUo6B5'
    secret_key = 'fdSgoq2c71UX8rJ8luX5zf3BsC03TmDmbOdKnr7e'
    q = Auth(access_key, secret_key)
    bucket_name = 'spider-data'
    # key = 'my-python-logo.png';
    # 上传文件到七牛后， 七牛将文件名和文件大小回调给业务服务器。
    token = q.upload_token(bucket_name, key, 3600)
    # localfile = './sync/bbb.jpg'
    ret, info = put_file(token, key, local_file)
    assert ret['key'] == key
    assert ret['hash'] == etag(local_file)
    return info




