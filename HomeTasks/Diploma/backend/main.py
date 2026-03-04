import person
from DataBase import get_db


rec = person.Record()
rec.add_person("22.03.1992", "Дмитро", "Батькович", "Призвищенко")
rec.add_person("20.03.1990", "Микола", "", "")
rec.add_person("11 10 2000", "Іванка", "", "", "02 10 2010")
rec.add_person("12.10.1980", "Євген", "Михайлович", "Крут", "11.10.2001")
rec.add_person("01/02/1995", "Євгенія", "", "", "12 10 2001")
rec.add_person("3-9-2007", "Дмитро", "Євгенович", "", "02 10 2010")
print(rec)

# database = db.DB()
# database.create_table()

db = get_db()
db.create_table()
rec.save_to_db(db)
