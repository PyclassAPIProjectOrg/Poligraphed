from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class SavedGraph(db.Model):
    __tablename__ = 'graphs'
    id = db.Column(db.Integer, primary_key=True)
    graph_name = db.Column(db.String(240))
    keyword_1 = db.Column(db.String(240))
    keyword_2 = db.Column(db.String(240))
    date_low = db.Column(db.String(10))
    date_high = db.Column(db.String(10))
    granularity = db.Column(db.String(5))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, graph_name, keyword_1, keyword_2, date_low, date_high, granularity, user_id):
        self.graph_name = graph_name
        self.keyword_1 = keyword_1
        self.keyword_2 = keyword_2
        self.date_low = date_low
        self.date_high = date_high
        self.granularity = granularity
        self.user_id = user_id

    def __repr__(self):
        return '<Graph %r>' % self.id

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    graphs = db.relationship('SavedGraph', backref='user', lazy='dynamic')
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
