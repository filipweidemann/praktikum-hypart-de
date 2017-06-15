import pymysql

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

def mySqlConnection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 port=8889,
                                 password = 'root',
                                 db='hypart',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
