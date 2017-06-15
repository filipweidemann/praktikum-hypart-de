from flask import Flask, flash, redirect, url_for, sessions, logging, request
from flask import render_template
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from werkzeug.utils import secure_filename
import os
from PIL import Image
import pymysql, smtplib
"""
Further ideas for this project:

- it is currently possible for everyone to change the map layout as they like.
  This should be restricted to the trusted people, therefore this form should
  be guarded by a login page or sth..

- give everyone who wants to contribute to the project the ability to add a password
  while they're in the renting process to create a unique artist profile for them!
  They could then use their email and password to log in and set up a nice profile
  with pictures/artwork and whatnot..

- built-in messaging system for artists?

- probably code enhancements.. bet that that is quite slow in benchmarks..

"""
UPLOAD_FOLDER = 'static'
app = Flask(__name__)
app.secret_key = 'some_test_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['gif', 'jpg', 'jpeg'])
ALLOWED_EXTENSIONS_LIST = ['gif', 'jpg', 'jpeg']
LOWER_BOUND = 1
UPPER_BOUND = 3
PROJECT_NUM = '01'
SENT_FROM = 'smtpsendmailwork@gmail.com'
SEND_TO = 'filip.weidemann@outlook.de'
SUBJECT = 'New tile reservation!'
field_list = []
charArr = []

@app.route('/')
def redirect_slash():
    return redirect('main')

@app.route('/main.sh')
def redirect_sh():
    return redirect('main')

@app.route('/main')
def canvas():
    artist_list = []
    with open("HypArt/artists/artists.list", 'r') as f:
        artist_list = [line.rstrip('\n') for line in f]

    imgList = []
    idList = ['1_1', '2_1', '3_1', '1_2', '2_2', '3_2', '1_3', '2_3', '3_3']
    with open('HypArt/project' + PROJECT_NUM + '/picture.map', 'r') as f:
        field_list = [line.strip() for line in f]
        xval = 1
        yval = 1
        for line in field_list:
            for char in line:
                charArr.append(char)
                if char == 'x':
                    extension = ""
                    for ext in range(0, UPPER_BOUND):
                        curr_ext = ALLOWED_EXTENSIONS_LIST[ext]
                        if os.path.isfile('static/' + str(yval) + '_' + str(xval) + '.' + curr_ext):
                            imgList.append(str(yval) + '_' + str(xval) + '.' + curr_ext)
                elif char == 'r':
                    imgList.append('http://www.hypart.de/HypArt/defpics/rent_tile.gif')
                elif char == 'R':
                    imgList.append('http://www.hypart.de/HypArt/defpics/busy_tile.gif')
                elif char == '0':
                    imgList.append('croppedgif.gif')
                xval += 1
            xval = 1
            yval += 1

    return render_template('canvas.html', img_id_list = zip(imgList, idList), PROJECT_NUM = PROJECT_NUM, artists = artist_list )

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data ## used for allocation of the tile (mysql check)
        # check if the post request has the file part
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            ## mysql connection and determination of tile number
            connection = mySqlConnection()
            error = False
            tile = ""
            try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "SELECT tile FROM users WHERE email=%s"
                    cursor.execute(sql, email)
                    results = cursor.fetchall()
                    if not results:
                        flash('An error occured. Please check your Email and/or selected file and try again.', 'danger')
                        error = True
                        return redirect('upload')
                    else:
                        row = results[0]
                        tile = row['tile']
                        extension = file.filename.rsplit('.', 1)[1].lower()
                        command = os.path.join(app.config['UPLOAD_FOLDER'], tile.encode("utf-8") + '.' + extension.encode("utf-8"))
                        path = app.config['UPLOAD_FOLDER'] + '/' + tile.encode("utf-8") + '.' + extension.encode("utf-8")
                        file.save(command)

            finally:
                connection.close()
                if not error:
                    flash('Image uploaded successfully', 'success')

            tile_list = tile.rsplit('_')
            picture_map_old = []

            with open('HypArt/project' + PROJECT_NUM + '/picture.map', 'r') as f:
                field_list = [line.strip() for line in f]

                for line in field_list:
                    for char in line:
                        picture_map_old.append(char)

                picture_map_new = ""

                changes = calculate_blocking(tile_list[0], tile_list[1])
                #import pdb; pdb.set_trace()
                cnt = 0
                for a in range(LOWER_BOUND, UPPER_BOUND+1):
                    for b in range(LOWER_BOUND, UPPER_BOUND+1):
                        #import pdb;pdb.set_trace()
                        if a == int(tile_list[0]) and b == int(tile_list[1]):
                            picture_map_new += 'x'
                        elif (a, b) in changes and not picture_map_old[cnt] == 'x':
                            picture_map_new += 'r'
                        else:
                            picture_map_new += picture_map_old[cnt]
                        cnt += 1
                    picture_map_new += '\n'

                with open('HypArt/project' + PROJECT_NUM + '/picture.map', 'w') as f:
                    f.write(picture_map_new)

            return redirect('main')
    return render_template('upload.html', form=form)

@app.route('/artists')
def artists():
    artist_list = []
    with open("HypArt/artists/artists.list", 'r') as f:
        artist_list = [line.rstrip('\n') for line in f]
        return render_template('about.html', artistList = artist_list)

@app.route('/artists/<name>')
def artist(name):
    connection = mySqlConnection()
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT email, homepage, quote FROM users WHERE name=%s"
            cursor.execute(sql, name)
            results = cursor.fetchall()
            row = results[0]
            email = row['email']
            homepage = row['homepage']
            quote = row['quote']
    finally:
        connection.close()

    return render_template('artist.html', artist=name, email=email, homepage=homepage, quote=quote)

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    idList = []
    for a in range(LOWER_BOUND, UPPER_BOUND+1):
        for b in range(LOWER_BOUND, UPPER_BOUND+1):
            idList.append(str(b) + ',' + str(a))
    return render_template('edit.html', PROJECT_NUM=PROJECT_NUM, ids=idList)

@app.route('/applychanges', methods = ['POST'])
def apply_changes_to_map():
    tile = request.form['tile']
    mode = request.form['mode']

    with open('HypArt/project' + PROJECT_NUM + '/picture.map', 'r') as f:
        field_list = [line.strip() for line in f]
        picture_map_old = []
        picture_map_new = ""
        for line in field_list:
            for char in line:
                picture_map_old.append(char)

        cnt = 0
        for x in range(LOWER_BOUND, UPPER_BOUND+1):
            for y in range(LOWER_BOUND, UPPER_BOUND+1):
                if (str(x) + ',' + str(y)) == tile:
                    picture_map_new += mode
                else:
                    picture_map_new += picture_map_old[cnt]
                cnt += 1
            picture_map_new += '\n'

    with open('HypArt/project' + PROJECT_NUM + '/picture.map', 'w') as f:
        f.write(picture_map_new)

    ## map layout changed
    flash('Successfully changed tile mode!', 'success')
    return redirect('main')

@app.route('/rent/<y>_<x>', methods = ['GET', 'POST'])
def rent(y, x):
    fileString = ""
    changes = []
    y = int(y)
    x = int(x)
    picture_map_old = []
    picture_map = ""
    cnt = 0
    form = RentForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        tile = str(x) + "_" + str(y)
        email = form.email.data
        homepage = form.homepage.data
        quote = form.message.data
        rented_tile = (x, y)
        connection = mySqlConnection()

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users(name, tile, email, homepage, quote) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, tile, email, homepage, quote))
                connection.commit()
        finally:
            connection.close()
            sendMail(SENT_FROM, SEND_TO, SUBJECT, \
                     'New reservation of tile ' + str(x) + ',' + str(y) + ' from ' + name + '. The artists personal homepage is ' \
                     + homepage + ' and he/she wrote: \n' + quote )

        with open("HypArt/artists/artists.list", 'a') as f:
                f.write(name+ '\n')

        with open('HypArt/project' + PROJECT_NUM + '/picture.map', 'r') as f:
            field_list = [line.strip() for line in f]
            for line in field_list:
                for char in line:
                    if char != 'x':
                        picture_map_old.append(char)
                    else:
                        picture_map_old.append('is_done')

        changes = calculate_blocking(x, y)
        for a in range(LOWER_BOUND, UPPER_BOUND+1):
            for b in range(LOWER_BOUND, UPPER_BOUND+1):
                ##import pdb;pdb.set_trace()
                if (a, b) in changes:
                    if picture_map_old[cnt] == 'is_done':
                        picture_map += 'x'
                    else:
                        picture_map += '0'
                elif (a, b) == (x, y):
                    picture_map += 'R'
                else:
                    if picture_map_old[cnt] != 'is_done':
                        picture_map += picture_map_old[cnt]
                    else:
                        picture_map += 'x'
                cnt += 1
            picture_map += '\n'
        cnt = 0

        with open('HypArt/project' + PROJECT_NUM + '/picture.map', 'w') as f:
            f.write(picture_map)

        flash('This tile now belongs to you', 'success')
        return redirect('main')

    return render_template('rent.html', form=form, x='{}'.format(x), y='{}'.format(y))

class RentForm(Form):
    name = StringField('Name', [validators.Length(min = 3, max = 50)])
    email = StringField('Email', [validators.Length(min = 6, max = 60), validators.Email()])
    homepage = StringField('Your Homepage')
    message = StringField('Message')

class UploadForm(Form):
    email = StringField('Email', [validators.Length(min = 6, max = 60), validators.Email()])

def mySqlConnection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 port=8889,
                                 password = 'root',
                                 db='hypart',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def calculate_blocking(x, y):
    changes = []
    x = int(x)
    y = int(y)
    if y > LOWER_BOUND and y < UPPER_BOUND:
            changes.append((x, y-1))
            changes.append((x, y+1))
    elif y == LOWER_BOUND:
            changes.append((x, y+1))
    elif y == UPPER_BOUND:
            changes.append((x, y-1))

    if x > LOWER_BOUND and x < UPPER_BOUND:
            changes.append((x-1, y))
            changes.append((x+1, y))
    elif x == LOWER_BOUND:
            changes.append((x+1, y))
    elif x == UPPER_BOUND:
            changes.append((x-1, y))
    return changes

def sendMail(FROM, TO, SUBJECT, TEXT):
    import smtplib
    username = 'smtpsendmailwork'
    password = 'Dummypassword123$'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(FROM, TO, TEXT)
    server.quit()

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
