from flask import Flask, render_template, flash, request, session, send_file
from flask import render_template, redirect, url_for, request
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import datetime
import mysql.connector

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('stopwords')
nltk.download('punkt')
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/NewProduct")
def NewProduct():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT distinct ProductType FROM protb")
    data = cur.fetchall()
    return render_template('NewProduct.html', data=data)


@app.route("/AProductInfo")
def AProductInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb ")
    data = cur.fetchall()
    return render_template('AProductInfo.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)


@app.route("/RNewProduct", methods=['GET', 'POST'])
def RNewProduct():
    if request.method == 'POST':
        file = request.files['fileupload']
        file.save("static/upload/" + file.filename)
        ProductId = request.form['pid']
        Gender = request.form['gender']
        Category = request.form['cat']
        SubCategory = request.form['subcat']
        ProductType = request.form['ptype']
        Colour = request.form['color']
        Usage = request.form['usage']
        ProductTitle = request.form['ptitle']

        Image = file.filename
        ImageURL = "static/upload/" + file.filename

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO protb VALUES ('" + ProductId + "','" + Gender + "','" + Category + "','" + SubCategory + "','" + ProductType + "','" + Colour + "','" +
            Usage + "','" + ProductTitle + "','" + Image + "','" + ImageURL + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

    return render_template('NewProduct.html')


@app.route("/Remove", methods=['GET'])
def Remove():
    pid = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cursor = conn.cursor()
    cursor.execute("Delete from protb  where id='" + pid + "'")
    conn.commit()
    conn.close()
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    # cursor = conn.cursor()
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM protb ")
    data = cur1.fetchall()
    # return 'file register successfully'
    return render_template('AProductInfo.html', data=data)

@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['uname']
        password = request.form['psw']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)
        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


def recommend():
    # 'Recommend'
    neg = 0
    pas = 0

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cursor = conn.cursor()
    cursor.execute("Truncate table  temptb")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT Distinct ProductId,Image,ProductName,Price FROM reviewtb where Result='Postive' ")
    data1 = cur.fetchall()
    for row in data1:

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) as count FROM reviewtb WHERE ProductId  ='" + row[0] + "' and Result='Postive'  ")
        data2 = cursor.fetchone()
        if data2:
            pas = data2[0]

        else:
            pas = 0

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) as count FROM reviewtb WHERE ProductId  ='" + row[0] + "' and Result='negative'  ")
        data3 = cursor.fetchone()
        if data3:
            neg = data3[0]

        else:
            neg = 0

        if pas >= neg:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
            cur = conn.cursor()
            cur.execute(
                "SELECT ProductId,CompanyName,ProductType,ProductName,Price,Image FROM reviewtb where ProductId  ='" +
                row[0] + "' ")
            data22 = cur.fetchone()
            if data22:
                s1 = data22[0]
                s2 = data22[1]
                s3 = data22[2]
                s4 = data22[3]
                s5 = data22[4]
                s6 = data22[5]
            else:
                neg = 0

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into  temptb values('" + s1 + "','" + s2 + "','" + s3 + "','" + s4 + "','" + s5 + "','" + s6 + "')")
            conn.commit()
            conn.close()


@app.route("/Search")
def Search():
    recommend()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT ProductId,Image,ProductName,Price FROM temptb  ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT distinct ProductType FROM protb ")
    data5 = cur.fetchall()

    return render_template('Search.html', data=data, data1=data1,data5=data5)


@app.route("/typesearch", methods=['GET', 'POST'])
def typesearch():
    cname = request.form['Cname']
    ptype = request.form['ptype']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from protb where Category='" + cname + "' and ProductType='" + ptype + "'")
    data = cursor.fetchone()
    if data is None:
        alert = 'Product Not Found!'
        return render_template('goback.html', data=alert)
    else:

        recommend()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM protb where Category='" + cname + "' and ProductType='" + ptype + "' ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cur = conn.cursor()
        cur.execute(
            "SELECT ProductId,Image,ProductName,Price FROM temptb where CompanyName='" + cname + "' and ProductType='" + ptype + "' ")
        data1 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cur = conn.cursor()
        cur.execute("SELECT distinct ProductType FROM protb ")
        data5 = cur.fetchall()

        return render_template('Search.html', data=data, data1=data1,data5=data5)


@app.route("/fullInfo")
def fullInfo():
    pid = request.args.get('pid')
    session['pid'] = pid

    rat1 = ''
    rat2 = ''
    rat3 = ''
    rat4 = ''
    rat5 = ''

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  ROUND(AVG(Rate), 1) as numRating FROM reviewtb WHERE ProductId  ='" + pid + "' ")
    data2 = cursor.fetchone()
    print(data2[0])
    if data2 is None:
        avgrat = 0


    else:

        if data2[0] == 'None':
            avgrat = 0
            if (int(avgrat) == 1):
                rat1 = 'checked'
            if (int(avgrat) == 2):
                rat2 = 'checked'
            if (int(avgrat) == 3):
                rat3 = 'checked'
            if (int(avgrat) == 4):
                rat4 = 'checked'
            if (int(avgrat) == 5):
                rat5 = 'checked'
        else:
            avgrat = data2[0]

            if (avgrat == 1):
                rat1 = 'checked'
            if (avgrat == 2):
                rat2 = 'checked'
            if (avgrat == 3):
                rat3 = 'checked'
            if (avgrat == 4):
                rat4 = 'checked'
            if (avgrat == 5):
                rat5 = 'checked'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  count(Rate)  as numRating FROM reviewtb WHERE ProductId  ='" + pid + "' ")
    data3 = cursor.fetchone()
    if data3:
        avgrat = data3[0]



    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Smile1) as count1,sum(Smile2) as count2, sum(Smile3) as count3, sum(Smile4) as count4, sum(Smile5) as count5, sum(Smile6) as count6 FROM  reviewtb where ProductId='" + pid + "' ")
    data = cursor.fetchone()
    if data:
        smile1 = data[0]
        smile2 = data[1]
        smile3 = data[2]
        smile4 = data[3]
        smile5 = data[4]
        smile6 = data[5]
    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT UserName,Review FROM reviewtb where ProductId='" + pid + "' ")
    reviewdata = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb where ProductId='" + pid + "' ")
    data1 = cur.fetchall()

    return render_template('ProductFullInfo.html', data=data1, avgrat=avgrat, rat1=rat1, rat2=rat2, rat3=rat3,
                           rat4=rat4, rat5=rat5, smile1=smile1, smile2=smile2, smile3=smile3, smile4=smile4,
                           smile5=smile5, smile6=smile6, reviewdata=reviewdata)


@app.route("/Book", methods=['GET', 'POST'])
def Book():
    if request.method == 'POST':
        import re
        from uuid import getnode as get_mac
        # mac = get_mac()

        uname = session['uname']
        pid = session['pid']

        qty = request.form['qty']
        ctype = request.form['ctype']
        cardno = request.form['cardno']
        cvno = request.form['cvno']

        Bookingid = ''
        ProductName = ''
        UserName = uname
        Mobile = ''
        Email = ''
        Qty = qty
        Amount = ''
        Mac = get_mac()

        CardType = ctype
        CardNo = cardno
        CvNo = cvno
        date = datetime.datetime.now().strftime('%d-%b-%Y')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb where  ProductId='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[3]
            price = str(int(str(data[0])[:3]))

            Amount = float(price) * float(Qty)

            print(Amount)
            session['amt'] = Amount


        else:
            return 'Incorrect username / password !'

        string = ProductName
        new_string = re.sub(r"[^a-zA-Z0-9]", "", string)
        print(new_string)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  regtb where  UserName='" + uname + "'")
        data = cursor.fetchone()

        if data:
            Mobile = data[4]
            Email = data[3]


        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  count(*) as count  FROM  booktb  ")
        data = cursor.fetchone()

        if data:
            count = data[0]

            if count == 0:
                count = 1;
            else:
                count += 1




        else:
            return 'Incorrect username / password !'
        print(count)

        Bookingid = "BOOKID00" + str(count)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO booktb VALUES ('','" + Bookingid + "','" + pid + "','" + ProductName + "','" + uname + "','" + Mobile + "','" + Email + "','" + Qty + "','" + str(
                Amount) + "','" + str(Mac) + "','" + CardType + "','" + CardNo + "','" + CvNo + "','" + date + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM booktb where  UserName= '" + uname + "' ")
        data = cur.fetchall()

    return render_template('UbookInfo.html', data=data)


@app.route("/NewReview")
def NewReview():
    from uuid import getnode as get_mac
    Mac = get_mac()

    return render_template('NewReview.html', mac=Mac)


@app.route("/ureview", methods=['GET', 'POST'])
def ureview():
    if request.method == 'POST':
        from uuid import getnode as get_mac

        feedr = 0
        starr = 0
        emojr = 0

        result = ''

        bookid = request.form['bookid']
        email = request.form['email']
        Mac = get_mac()
        star = request.form['star']
        emoj = request.form['ar']
        print(emoj)
        uname = session['uname']

        feedback = request.form['feed']

        sta = 0



        example_sent = feedback

        mlp = SentimentIntensityAnalyzer()

        # polarity_scores method of SentimentIntensityAnalyzer
        # object gives a sentiment dictionary.
        # which contains pos, neg, neu, and compound scores.
        sentiment_dict = mlp.polarity_scores(example_sent)

        string = str(sentiment_dict['neg'] * 100) + "% Negative"
        # negativeField.insert(10, string)

        string = str(sentiment_dict['neu'] * 100) + "% Neutral"
        # neutralField.insert(10, string)

        string = str(sentiment_dict['pos'] * 100) + "% Positive"
        # positiveField.insert(10, string)

        # decide sentiment as positive, negative and neutral
        if sentiment_dict['compound'] >= 0.05:
            string = "Positive"
            i = 0;

        elif sentiment_dict['compound'] <= - 0.05:
            string = "Negative"

            i = 1;


        else:
            string = "Neutral"
            i = 0;

        if string == 'Negative':
            feedr = 0
        else:
            feedr = 1

        if (int(star) > 2):
            starr = 1
        else:
            starr = 0
        if (int(emoj) >= 3):
            emojr = 1
        else:
            emojr = 0

        total = int(feedr) + int(starr) + int(emojr)

        if (total > 1):
            result = 'Postive'
        else:
            result = 'negative'

        print(result)

        em1 = 0
        em2 = 0
        em3 = 0
        em4 = 0
        em5 = 0
        em6 = 0

        if (int(emoj) == 6):
            em1 = 1
        if (int(emoj) == 5):
            em2 = 1
        if (int(emoj) == 4):
            em3 = 1
        if (int(emoj) == 3):
            em4 = 1
        if (int(emoj) == 2):
            em5 = 1
        if (int(emoj) == 1):
            em6 = 1

        print(em1, em2, em3, em4, em5, em6)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  *  FROM  booktb where  Bookingid='" + bookid + "' and Email='" + email + "' and Mac='" + str(
                Mac) + "'")
        data = cursor.fetchone()
        if data:
            proid = data[2]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM  protb where  ProductId='" + proid + "'")
            data = cursor.fetchone()
            if data:
                cname = data[2]
                ptype = data[4]
                pname = data[3]
                price = str(int(str(data[0])[:3]))
                img = data[9]

            else:
                alert = 'No Record Found!'

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT  *  FROM   reviewtb  where  Bookid='" + bookid + "' and Email='" + email + "' and MacAddress='" + str(
                    Mac) + "'")
            data = cursor.fetchone()
            if data:
                flash("Already Your  Review Enter This Product")
                return render_template('NewReview.html')

            else:

                print(proid)

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO  reviewtb VALUES ('','" + str(proid) + "','" + str(cname) + "','" + str(
                        ptype) + "','" + str(pname) + "','" + str(price) + "','" + str(img) + "','" + str(
                        bookid) + "','" + str(email) + "','" +
                    str(Mac) + "','" + str(uname) + "','" + str(star) + "','" + str(feedback) + "','" + str(
                        em1) + "','" + str(em2) + "','" + str(em3) + "','" + str(em4) + "','" + str(em5) + "','" + str(
                        em6) + "','" + str(result) + "')")
                conn.commit()
                conn.close()

                flash("Review Enter Successfully")
                return render_template('NewReview.html')


        else:

            alert = 'No Record Found'

            return render_template('goback.html', data=alert)


@app.route("/UBookInfo")
def UBookInfo():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM booktb  where UserName='" + uname + "'  ")
    data = cur.fetchall()
    return render_template('UBookInfo.html', data=data)


@app.route("/ABookInfo")
def ABookInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM booktb   ")
    data = cur.fetchall()
    return render_template('ABookInfo.html', data=data)


@app.route("/UReviewInfo")
def UReviewInfo():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute(
        "SELECT Bookid,ProductId,ProductName,UserName,MacAddress,Rate,Review,smile1,smile2,smile3,smile4,smile5,smile6 FROM reviewtb  where UserName='" + uname + "'  ")
    data = cur.fetchall()
    return render_template('UReviewInfo.html', data=data)


@app.route("/AReviewInfo")
def AReviewInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3productrecomdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT Bookid,ProductId,ProductName,UserName,MacAddress,Rate,Review,smile1,smile2,smile3,smile4,smile5,smile6 FROM reviewtb   ")
    data = cur.fetchall()
    return render_template('AReviewInfo.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
