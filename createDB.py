import sqlite3

conn = sqlite3.connect('medicine_db.db')
c = conn.cursor()
# c.execute('''CREATE TABLE meds
#              (uid integer, med_name text, expiration_date text, amount real,
#               is_closed integer, city text, owner_mail text, owner_name text)''')

#c.execute("INSERT INTO meds VALUES (1, 'Malarone', '2018-05-01', 10, 0, 'Haifa', 'shahar.aizenbud@gmail.com')")

# values = [(2, 'Acamol', '2018-06-22', 20, 1, 'Jerusalem', 'avisagal41@gmail.com'),
#           (3, 'Advil', '2019-01-01', 15, 0, 'Jerusalem', 'netta.barak@gmail.com')]
# c.executemany("INSERT INTO meds VALUES (?,?,?,?,?,?,?)", values)

# c.execute('''CREATE TABLE meds_data
#              (med_name text, picture text)''')

# values = [('Malarone', 'https://www.doctorfox.co.uk/imgs-products/zoom/malarone-pills.jpg'),
#           ('Acamol', 'http://www.pilula.co.il/~pilula5/images/stories/virtuemart/product/acamol%20caps.jpg'),
#           ('Advil', 'https://images-na.ssl-images-amazon.com/images/I/917DL6AA0PL._SY355_.jpg'),
#           ('Meliane', 'http://www.drug.co.il/ps/109-12-29094-00.jpg'),
#           ]
# c.executemany("INSERT INTO meds_data VALUES (?,?)", values)

#c.execute("INSERT INTO meds VALUES (4, 'Malarone', '2018-07-04', 15, NULL, 'Raanana', 'netta.barak@gmail.com')")

#c.execute('''ALTER TABLE meds ADD COLUMN owner_name text;''')

# values = [(2, 'Acamol', '2018-06-22', 20, 1, 'Jerusalem', 'avisagal41@gmail.com', 'avi'),
#           (3, 'Advil', '2019-01-01', 15, 0, 'Jerusalem', 'netta.barak@gmail.com', 'netta'),
#           (1, 'Malarone', '2018-05-01', 10, 0, 'Haifa', 'shahar.aizenbud@gmail.com', 'shahar'),
#           (4, 'Malarone', '2018-07-04', 15, 1, 'Raanana', 'netta.barak@gmail.com', 'netta')]
# c.executemany("INSERT INTO meds VALUES (?,?,?,?,?,?,?,?)", values)
#
# c.execute('''ALTER TABLE meds_data ADD COLUMN amount real;''')
# c.execute('''ALTER TABLE meds_data ADD COLUMN description text;''')
# c.execute('''ALTER TABLE meds_data ADD COLUMN manufacturer text;''')

# values = [('avisagal41@gmail.com',"אבי", "acamol"), ('netta.barak@gmail.com',"נטע", "acamol"),
#           ('shahar.aizenbud@gmail.com', "שחר", "acamol")]
#
# c.executemany("INSERT INTO waiting VALUES (?,?,?)", values)



# c.execute('''CREATE TABLE waiting
#              (mail text, name text, med_name text)''')

# c.execute('''drop table meds''')
#
c.execute('''delete from meds where uid between 5 and 14''')


conn.commit()

conn.close()
