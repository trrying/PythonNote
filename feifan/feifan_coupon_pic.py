import util.time_utils
import ffan_db_config
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import feifan.qiniu_upload
import os


def get_pic(data_list):
    # https://timg.ffan.com/convert/resize/url_T1_cYvB4b_1RCvBVdK/width_284/height_160/tfs/xxx.webp
    base_url = "https://timg.ffan.com/convert/resize/url_%(logo)s/width_284/height_160/tfs/xxx.webp"

    # 打开数据库连接
    db, cursor = ffan_db_config.get_db_config()

    base_update_sql = """update ffan_coupon set 
                                    fc_local_logo='%(fc_local_logo)s',
                                    fc_update_time='%(fc_update_time)s' 
                                    WHERE fp_p_id = '%(fp_p_id)s' and fc_aid = '%(fc_aid)s'
                                    """

    # 失败重试次数
    retry_time = 2

    path_name = "pic/feifan/coupon/"
    base_file_name = "ffan_c_%s.webp"

    logo_space = "http://opbbasjan.bkt.clouddn.com/"

    if not os.path.exists(path_name):
        os.makedirs(path_name)

    for data_bean in data_list:
        fc_aid = data_bean[0]
        fp_p_id = data_bean[1]
        fc_logo = data_bean[2]
        for retry in range(retry_time):
            update_count = 0
            try:
                pic_url = base_url % {'logo': fc_logo}
                # print("pic_url : " + pic_url)
                response = ffan_db_config.request_response(pic_url)
                if response.status_code == 200:
                    image_content = response.content
                    file_name = base_file_name % fc_logo
                    local_file = path_name + file_name
                    with open(local_file, 'wb') as f:
                        f.write(image_content)
                    info = feifan.qiniu_upload.upload_imgs(local_file, file_name)
                    if info.status_code == 200:
                        try:
                            fc_local_logo = logo_space + file_name
                            update_sql = base_update_sql % {
                                'fc_local_logo': fc_local_logo,
                                'fc_update_time': util.time_utils.get_current_time(),
                                'fp_p_id': fp_p_id,
                                'fc_aid': fc_aid
                            }
                            # print(update_sql)
                            update_count = cursor.execute(update_sql)
                            db.commit()
                        except Exception as e:
                            print(e)
            except Exception as e:
                print(e)
            print("ffan_coupon  update logo  "
                  "data.len : %d  "
                  "updateCount : %d  "
                  "retry_count : %d  "
                  "fp_p_id : %s  "
                  "fc_aid : %s"
                  %
                  (len(data_list),
                   update_count,
                   retry,
                   fp_p_id,
                   fc_aid,
                   ))
            if update_count:
                break
    db.close()


def get_data():
    # 打开数据库连接
    db, cursor = ffan_db_config.get_db_config()

    select_sql = "SELECT fc_aid,fp_p_id,fc_logo FROM ffan_coupon WHERE fc_logo IS NOT NULL AND fc_local_logo IS NULL"
    cursor.execute(select_sql)
    sql_result = cursor.fetchall()
    db.close()
    get_pic(sql_result)


if __name__ == '__main__':
    get_data()














