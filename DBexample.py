import sqlite3
conn = sqlite3.connect('example.db')

c = conn.cursor()

# create, insert, delete
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

values = [('2007-08-09', 'SELL','ABC',102,3), ('2007-08-09', 'SHOP','DGV',500.2,40)]
c.executemany("INSERT INTO stocks VALUES (?,?,?,?,?)", values)

#delete all rows
# c.execute('delete from stocks')

conn.commit()


# fetch
t = ('SELL','SHOP')
c.execute('SELECT * FROM stocks WHERE trans IN (?,?)', t)
print(c.fetchall())
s = ('SELL',)
c.execute('SELECT * FROM stocks WHERE trans =?', s)
print(c.fetchall())

r= (30,40)
c.execute('SELECT * FROM stocks WHERE price between ? and ?', r)
print(c.fetchall())


conn.close()
