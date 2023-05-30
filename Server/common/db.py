from django.db import models


class BaseModel(models.Model):
    """抽象的模型基類: 定義一些公共的模型字段
    auto_now_add=True:表示字段第一次保存的时间,由系统自动生成,一旦设定就不可以更改,一般用作创建时间
    auto_now=True:最后一次修改时间,系统自动生成,一般用作更新时间
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    is_delete = models.BooleanField(default=False, verbose_name='刪除標記')

    class Meta:
        abstract = True  # 聲明這是一個抽象的模型,在執行遷移文件時,不會在數據庫中生成表
        verbose_name_plural = "公共字段表"  # 模型类的复数名,主要用在管理后台的展示上,不设置的话Django使用小写的模型名作为默认值并且在结尾加上s
        db_table = 'BaseTable'  # 用于指定数据表的名称
