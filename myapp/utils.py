import os
from PIL import Image
from App import UPLOAD_PHOTOS,photos

# 上传
def upload_img(user_img,before,not_s=False):
    # 获取后缀
    img = user_img
    shuffix = img.filename.split('.')[-1]
    # 获取唯一文件名
    while True:
        # 转换图片名称
        newfileName = 'image_'+new_name(shuffix)
        # 图片image路径
        path = os.path.join(UPLOAD_PHOTOS,newfileName)
        if not os.path.exists(path):
            break
    # 压缩图片
    photos.save(img,name=newfileName)
    if not not_s:
        s_img_url = img_zoom(path,'s_')
        # 拿到压缩图片url
        img_url = photos.url('s_'+newfileName)
        # 删除未压缩的图片
        try:
            if before:
                delete_file(before,UPLOAD_PHOTOS)
            os.remove(path)
        except:
            os.remove(s_img_url)
            os.remove(path)
            print(path)
            raise OSError('删除失败')
        return img_url
    else:
        try:
            img_url = photos.url(newfileName)
        except:
            os.remove(s_img_url)
            os.remove(path)
            print(path)
            raise OSError('删除失败')
        return img_url

# 生成随机名称
def new_name(shuffix,length=32):
    import string,random
    Str = string.ascii_letters+string.digits
    newname = ''.join(random.choice(Str) for i in range(length))
    return newname+'.'+shuffix


# 缩放图片
def img_zoom(path,perfix,width=200,height=200):
    img = Image.open(path)
    img.thumbnail((width,height))
    path_tup = os.path.split(path)
    path = os.path.join(path_tup[0],perfix+path_tup[1])
    img.save(path)
    return path

# 删除文件
def delete_file(file_url,file_type):
    if file_url and file_type:
        before_filename = file_url.split('/')[-1]
        before_path = os.path.join(file_type,before_filename)
        if os.path.exists(before_path):
            os.remove(before_path)
