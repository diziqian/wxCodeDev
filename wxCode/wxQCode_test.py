from wxQCode_templateInfo import WeChat


my_wechat = WeChat("aaa", "test", "13012345678", "测试程序")
my_wechat.set_token()
my_wechat.post_data()