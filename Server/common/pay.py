from alipay import AliPay

from Server import settings


class Pay:

    @staticmethod
    def alipay(order_on, amount):
        APPID = '2016101500690868'  # 应用ID
        # PID = '2088102179659163'  # 绑定的商家账号（PID）
        # 公钥和私钥
        PUBLIC_KEY = open(settings.BASE_DIR/'common/alipay_public_key.pem').read()
        PRIVATE_KEY = open(settings.BASE_DIR/'common/alipay_private_key.pem').read()

        subject = '朴朴生鲜商城订单{}支付'.format(order_on)  # 支付页面显示的标题

        # 第三步:初始化一个支付对象
        pay = AliPay(
            appid=APPID,  # 应用ID
            app_notify_url=None,  # 支付完成后回调自己系统的url(上线之后可以配置)
            app_private_key_string=PRIVATE_KEY,  # 私钥
            alipay_public_key_string=PUBLIC_KEY,  # 公钥
            debug=True,  # 沙箱环境开启Debug模式,上线之后需要关闭
        )

        # 第四步:生成支付地址
        # PC网站
        url = pay.api_alipay_trade_page_pay(
            subject=subject,  # 支付页面显示的标题
            out_trade_no=order_on,  # 商户生成的订单号
            total_amount=amount,  # 支付金额
            # 这两个上线之后再配置
            return_url=None,  # 支付成功前端跳转的页面地址
            notify_url=None   # 支付成功的回调地址
        )

        # # 手机网站
        # url = pay.api_alipay_trade_wap_pay(
        #     subject=subject,  # 支付页面显示的标题
        #     out_trade_no=order_on,  # 商户生成的订单号
        #     total_amount=amount,  # 支付金额
        #     # 这两个上线之后再配置
        #     return_url=None,  # 支付成功前端跳转的页面地址
        #     notify_url=None   # 支付成功的回调地址
        # )

        # # APP用户
        # url = pay.api_alipay_trade_app_pay(
        #     subject=subject,  # 支付页面显示的标题
        #     out_trade_no=order_on,  # 商户生成的订单号
        #     total_amount=amount,  # 支付金额
        #     # 这两个上线之后再配置
        #     return_url=None,  # 支付成功前端跳转的页面地址
        #     notify_url=None   # 支付成功的回调地址
        # )

        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + url
        return pay_url
