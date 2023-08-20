import mysql.connector


#'Recommend'
'''neg = 0
pas =0

conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
cursor = conn.cursor()
cursor.execute("Truncate table  temptb")
conn.commit()
conn.close()

conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
cur = conn.cursor()
cur.execute("SELECT ProductId,Image,ProductName,Price FROM reviewtb where Result='Postive' ")
data1 = cur.fetchall()
for row in data1:

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
    cursor = conn.cursor()
    cursor.execute( "SELECT  count(*) as count FROM reviewtb WHERE ProductId  ='" + row[0] + "' and Result='Postive'  ")
    data2 = cursor.fetchone()
    if data2:
        pas = data2[0]

    else:
        pas = 0

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  count(*) as count FROM reviewtb WHERE ProductId  ='" + row[0] + "' and Result='negative'  ")
    data3 = cursor.fetchone()
    if data3:
        neg = data3[0]

    else:
        neg = 0


    if pas >= neg:
        thislist = []
        thislist.append(row[0])




for i in thislist:

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT ProductId,ProductName,Price,Image FROM reviewtb where ProductId  ='" + i[0] + "' ")
    data22 = cur.fetchone()
    if data22:
        s1 = data22 [0]
        s2 = data22[1]
        s3 = data22[2]
        s4 = data22[3]


    else:
        neg = 0


    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
    cursor = conn.cursor()
    cursor.execute("insert into  temptb values('"+ s1 +"','"+ s2 +"','"+ s3+"','"+s4+"')")
    conn.commit()
    conn.close()



    print(i[0])'''



def recommend():
    # 'Recommend'
    neg = 0
    pas = 0

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
    cursor = conn.cursor()
    cursor.execute("Truncate table  temptb")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
    cur = conn.cursor()
    cur.execute("SELECT ProductId,Image,ProductName,Price FROM reviewtb where Result='Postive' ")
    data1 = cur.fetchall()
    for row in data1:

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) as count FROM reviewtb WHERE ProductId  ='" + row[0] + "' and Result='Postive'  ")
        data2 = cursor.fetchone()
        if data2:
            pas = data2[0]

        else:
            pas = 0

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) as count FROM reviewtb WHERE ProductId  ='" + row[0] + "' and Result='negative'  ")
        data3 = cursor.fetchone()
        if data3:
            neg = data3[0]

        else:
            neg = 0

        if pas >= neg:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
            cur = conn.cursor()
            cur.execute(
                "SELECT ProductId,CompanyName,ProductType,ProductName,Price,Image FROM reviewtb where ProductId  ='" + row[0] + "' ")
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

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrecomdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into  temptb values('" + s1 + "','" + s2 + "','" + s3 + "','" + s4 + "','" + s5 + "','" + s6 + "')")
            conn.commit()
            conn.close()





recommend()