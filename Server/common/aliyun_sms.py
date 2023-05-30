class AliyunSMS:
    """模擬發送手機驗證碼"""

    @staticmethod
    def send(mobile: str, code: str):
        print("假裝發送手機驗證碼[手機號:{}, 驗證碼:{}]".format(mobile, code))
        return {'code': "OK", "message": "短信發送成功"}


if __name__ == '__main__':
    result = AliyunSMS().send(mobile="18170626385", code="123456")
    print(result)
