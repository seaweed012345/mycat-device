# src/server/main.py
from flask import Flask
from models.user import db, User
from controllers.datacenter_api import datacenter_api
from controllers.user_controller import user_bp
from flask_cors import CORS
from controllers.captcha_api import captcha_bp
from models.datacenter import DeviceData
from controllers.device_api import device_api
from controllers.health_report_api import health_report_api
from controllers.comm_api import comm_api
from controllers.wx_api import wx_bp


from flask_migrate import Migrate   # 新增

app = Flask(__name__)
app.register_blueprint(wx_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 可替换为postgres等
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'xxxjuwosecretxxx'
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(device_api, url_prefix='/api/device')
app.register_blueprint(datacenter_api, url_prefix='/api/datacenter')
app.register_blueprint(captcha_bp)
app.register_blueprint(health_report_api)
app.register_blueprint(comm_api)

# 启用跨域，前端开发时允许跨域
CORS(app)
CORS(app, supports_credentials=True)

db.init_app(app)

# ====== Flask-Migrate 初始化 ======
migrate = Migrate(app, db)

# ====== 只保留API接口！！ 页面渲染路由全部由Vue前端负责 ======

if __name__ == "__main__":
    # 初始化数据库，没有就新建
    with app.app_context():
        db.create_all()

        # 检查是否存在超级管理员账号，没有则插入
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@your.com')
            admin.set_password('darknessray4296')
            db.session.add(admin)
            db.session.commit()
    app.run(host='0.0.0.0', port=8001, debug=True)