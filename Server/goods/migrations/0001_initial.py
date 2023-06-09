# Generated by Django 4.2.1 on 2023-05-30 00:19

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('is_delete', models.BooleanField(default=False, verbose_name='刪除標記')),
                ('title', models.CharField(default='', help_text='輪播圖名稱', max_length=20, verbose_name='輪播圖名稱')),
                ('image', models.ImageField(blank=True, help_text='輪播圖鏈接', null=True, upload_to='', verbose_name='輪播圖鏈接')),
                ('status', models.BooleanField(blank=True, default=False, help_text='是否啓用', verbose_name='是否啓用')),
                ('seq', models.IntegerField(blank=True, default=1, help_text='順序', verbose_name='順序')),
            ],
            options={
                'verbose_name': '首頁商品輪播',
                'verbose_name_plural': '首頁商品輪播',
                'db_table': 'banner',
            },
        ),
        migrations.CreateModel(
            name='GoodsGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名稱')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='分類圖標')),
                ('status', models.BooleanField(default=False, verbose_name='是否啓用')),
            ],
            options={
                'verbose_name': '商品分類表',
                'verbose_name_plural': '商品分類表',
                'db_table': 'goods_group',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('is_delete', models.BooleanField(default=False, verbose_name='刪除標記')),
                ('title', models.CharField(default='', help_text='標題', max_length=200, verbose_name='標題')),
                ('desc', models.CharField(help_text='商品描述', max_length=200, verbose_name='商品描述')),
                ('price', models.DecimalField(decimal_places=2, help_text='商品價格', max_digits=10, verbose_name='商品價格')),
                ('cover', models.ImageField(blank=True, help_text='封面圖鏈接', null=True, upload_to='', verbose_name='封面圖鏈接')),
                ('stock', models.IntegerField(blank=True, default=1, help_text='庫存', verbose_name='庫存')),
                ('sales', models.IntegerField(blank=True, default=0, help_text='銷量', verbose_name='銷量')),
                ('is_on', models.BooleanField(blank=True, default=False, help_text='是否上架', verbose_name='是否上架')),
                ('recommend', models.BooleanField(blank=True, default=False, help_text='是否推薦', verbose_name='是否推薦')),
                ('group', models.ForeignKey(help_text='分類', max_length=20, on_delete=django.db.models.deletion.CASCADE, to='goods.goodsgroup', verbose_name='分類')),
            ],
            options={
                'verbose_name': '商品表',
                'verbose_name_plural': '商品表',
                'db_table': 'goods',
            },
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('is_delete', models.BooleanField(default=False, verbose_name='刪除標記')),
                ('producer', models.CharField(help_text='廠商', max_length=200, verbose_name='廠商')),
                ('norms', models.CharField(help_text='規格', max_length=200, verbose_name='規格')),
                ('details', ckeditor.fields.RichTextField(blank=True, verbose_name='商品詳情')),
                ('goods', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品詳情',
                'verbose_name_plural': '商品詳情',
                'db_table': 'detail',
            },
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods', models.ForeignKey(help_text='商品ID', on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品ID')),
            ],
            options={
                'verbose_name': '收藏商品',
                'verbose_name_plural': '收藏商品',
                'db_table': 'collect',
            },
        ),
    ]
