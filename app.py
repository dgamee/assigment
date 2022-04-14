from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup-account', methods=['post'])
def signup_account():
    name = request.form.get('name')
    email = request.form.get('email')
    pwd = request.form.get('password')
    gender = request.form.get('gender')
    age = request.form.get('age')
    genre1 = request.form.get('genre1')
    genre2 = request.form.get('genre2')
    genre3 = request.form.get('genre3')
    arr = []
    arr.extend([name,email,pwd,gender,age,genre1,genre2,genre3])
    write_to_file('customer.txt',arr)
    return 'Account created successfully'


@app.route('/login-account', methods=['post'])
def loginAccount():
    name = request.form.get('email')
    pwd = request.form.get('password')
    result = ''
    users = read_file('customer.txt')
    for i in users:
        user = i.split(',')
        if name == user[1] and pwd == user[2]:
            result = user
            break
    if result:
        return render_template('dashboard.html',username = result[0], email = result[1], most_selected_category = most_selected_category(),most_watched_age = most_watched_age(),watched_by_each_age = watched_by_each_age())
    else:
        return 'Wrong credential'
    



def most_selected_category():
    f_data = read_file('customer.txt')
    category = []
    for i in f_data:
        data = i.split(',')
        category.extend([data[5],data[6],data[7].replace('\n','')])
    most_watched_category = count_most_watched_movie(category)
    return most_watched_category

def count_most_watched_movie(list):
    default_category = ['action','horror','animation','romance','thriller','comedy']
    num_of_comedy =list.count('comedy')
    num_of_thriller = list.count('thriller')
    num_of_action =list.count('action')
    num_of_horror = list.count('horror')
    num_of_animation =list.count('animation')
    num_of_romance = list.count('romance')
    num_of_category = []
    num_of_category.extend([num_of_action,num_of_horror,num_of_animation,num_of_romance,num_of_thriller,num_of_comedy])
    max_item = max(num_of_category)
    if max_item == 0:
        return 'none'
    most_selected_category = default_category[num_of_category.index(max_item)]
    return most_selected_category

def most_watched_age():
    f_data = read_file('customer.txt')
    default_age_bracket = ['18-25','26-39','40-59','60-above']
    age_bracket = []
    for i in f_data:
        data = i.split(',')
        age_bracket.append(data[4])
    num_of_18_25 =age_bracket.count('18-25')
    num_of_26_39 = age_bracket.count('26-39')
    num_of_40_59 =age_bracket.count('40-59')
    num_of_60_above = age_bracket.count('60-above')
    num_of_age_bracket = []
    num_of_age_bracket.extend([num_of_18_25,num_of_26_39,num_of_40_59,num_of_60_above])
    max_item = max(num_of_age_bracket)
    most_watched_age_bracket = default_age_bracket[num_of_age_bracket.index(max_item)]
    return most_watched_age_bracket

def watched_by_each_age():
    f_data = read_file('customer.txt')
    num_18_25 = []
    num_26_39 = []
    num_40_59 = []
    num_60_above = []
    for i in f_data:
        data = i.split(',')
        if data[4] == '18-25':
            num_18_25.extend([data[5],data[6],data[7].replace('\n','')])
        if data[4] == '26-39':
            num_26_39.extend([data[5],data[6],data[7].replace('\n','')])
        if data[4] == '40-59':
            num_40_59.extend([data[5],data[6],data[7].replace('\n','')])
        if data[4] == '60-above':
            num_60_above.extend([data[5],data[6],data[7].replace('\n','')])
    most_watched_by_18_25 = count_most_watched_movie(num_18_25)
    most_watched_by_26_39 = count_most_watched_movie(num_26_39)
    most_watched_by_40_59 = count_most_watched_movie(num_40_59)
    most_watched_by_60_above = count_most_watched_movie(num_60_above)

    return [most_watched_by_18_25,most_watched_by_26_39,most_watched_by_40_59,most_watched_by_60_above]

            
def write_to_file(filename,arr):
    data = ','.join(arr)
    with open(filename,'a') as file_handler:
        file_handler.write(data+'\n')
    return 'okay'

def read_file(filename):
    with open(filename) as file_handler:
        data = file_handler.readlines()
    return data

if __name__ == '__main__':
    app.run(port=5000, debug=False,host='0.0.0.0')

# ,host='0.0.0.0'