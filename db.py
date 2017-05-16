# dummy database
import MySQLdb
db = MySQLdb.connect("localhost","root","root","recommendation" )
cursor = db.cursor()
user_id="suryansh"
item_id="batman"
rating="8"
sql = "INSERT INTO RatingMatrix(user_id, item_id, rating) \
       VALUES ('%s', '%s', '%s' )" % \
       (user_id, item_id, rating)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
# disconnect from server
db.close()