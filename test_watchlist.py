import unittest

from watchlist import app,db
from watchlist.models import User,Movie


class WatchlistTestCase(unittest.TestCase):
    def setUp(self):
        #更新配置  在开发和测试时候通常配置不一样
        app.config.update(
            TESTING = True,  #开启测试模式   出错时候不会输出多余消息
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  #SQLite内存型数据库，不会
        )
        #创建数据库和表
        db.create_all()
        #创建测试数据，一个用户，一个电影信息
        user = User(name = 'Test',username = 'Test')
        user.set_password('123456')
        movie = Movie(title = '测试电影名称',year = '2020')
        db.session.add_all([user,movie])
        db.session.commit()

        self.client = app.test_client() #创建测试客户端（模拟客户端请求）
        self.runner = app.test_cli_runner()#创建测试命令运行期（触发自定义命令）



    def tearDown(self):
        db.session.remove()#清除数据库会话
        db.drop_all()#删除数据库表


    #测试程序实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)
    
    
    #测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])


    #定义404页面
    def test_404_page(self):
        response = self.client.get('/lalala')  #传入一个不存在的路由
        data = response.get_data(as_text = True)    #获取Unicode格式的响应主体
        self.assertIn('404 - 页面跑丢了',data)
        self.assertIn('返回首页',data)
        self.assertEqual(response.status_code,404)  #判断响应状态码

    #测试主页
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text = True)
        self.assertIn('Test\'s WatchList',data)
        self.assertIn('测试电影名称',data)
        self.assertEqual(response.status_code,200)
    #测试登录
    def login(self):
        self.client.post('/login',data = dict(
            username = 'Test',
            password = '123456'
        ),follow_redirects = True)

    #删除
    def test_delete_item(self):
        self.login()
        response = self.client.post('/movie/delete/1',follow_redirects = True)
        data = response.get_data(as_text=True)
        self.assertIn('删除数据成功',data)
    


if __name__ == '__main__':
    unittest.main()



