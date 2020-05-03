from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from random import shuffle

#qianhao = [  1.,   2.,   3.,   4.,   5.]

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username


users=[]
lst_users=[]
f = open("user_name.txt", "r")
id_nums = 1
for line in f:
    line = line.strip('\n')
    users.append(User(id=id_nums,username=line, password='123456'))
    id_nums += 1
    lst_users.append(line)

# users.append(User(id=1, username='dakki', password='123'))
# users.append(User(id=2, username='dakki2', password='123'))
# users.append(User(id=3, username='dakki3', password='123'))
# users.append(User(id=4, username='dakki4', password='123'))
# users.append(User(id=5, username='dakki5', password='123'))

# lst_users = ['dakki','dakki2','dakki3','dakki4','dakki5']
# lst_user_shuffle = lst_user.copy()
# shuffle(lst_user_shuffle)
sum_nums = len(lst_users)
qianhao = list(range(1,len(lst_users)+1))
shuffle(qianhao)
qianhao.insert(0,0)
print(qianhao)
# dict_user = dict(zip(lst_user_shuffle,nums))
# print(dict_user)
dict_user = {}

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/', methods=['GET', 'POST'])
def login():
#    error = None
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
#        user = [x for x in users if x.username == username][0]
        if username == 'root' and password == 'fushichouqian':
#            a = sorted(dict_user.keys())
            return redirect(url_for('result'))
        elif username in lst_users:
            user = [x for x in users if x.username == username][0]
            if password == user.password:
                session['user_id'] = user.id
                return redirect(url_for('chouqian'))
            else:
                flash('密码错误！')
        else:
            flash('账号不存在！') 

#        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/chouqian',methods=('POST','GET'))
def chouqian():
    if not g.user:
        return redirect(url_for('login'))
    if str(g.user) in dict_user.keys():
        return redirect(url_for('profile'))
    else:
        del(qianhao[0])
        print('签号池：',qianhao)
        dict_name = str(g.user)
        dict_user[dict_name] = str(qianhao[0])
        print(dict_user)
    return render_template('chouqian.html', qianhao = qianhao)

@app.route('/profile',methods=('POST','GET'))
def profile():
    if not g.user:
        return redirect(url_for('login'))
    user_qianhao = dict_user[str(g.user)]
    return render_template('profile.html',user_qianhao = user_qianhao)

@app.route('/result',methods=('POST','GET'))
def result():
#    user_sort = sorted(dict_user.keys())
    result_lst = []
    for key in dict_user:
        result_lst.append(key + '：' + dict_user[key])
    print(result_lst)
    return render_template('result.html',result_lst = result_lst)


if __name__ == '__main__':
    app.run(debug=True)