import qrcode
import sqlite3

class QRGeneration:
    def __init__(self,surname,name,patronymic, klass,klassName,parents):
        self.surname = surname
        self.name = name 
        self.patronymic = patronymic
        self.klass = klass
        self.klassName = klassName
        self.parents = '-'.join(parents)
        self.QR = qrcode.QRCode(
            version=1,  
            error_correction=qrcode.constants.ERROR_CORRECT_L,  
            box_size=10,
            border=4,  
        )

    def generateQR(self):
        connection = sqlite3.connect('qrDatabase.db')
        getIDCursor = connection.cursor()
        getIDCursor.execute('SELECT * FROM students')
        stdID = str(len(getIDCursor.fetchall()) + 1)

        key = '.'.join([self.surname,
                        self.name,
                        self.patronymic,
                        self.parents,
                        self.klass,
                        self.klassName,
                        stdID])
        
        self.QR.add_data(key)
        self.QR.make(fit=True)

        QRcode = self.QR.make_image(fill_color="black", back_color="white")
        QRcode.save(f'{self.surname}_{self.name}_{self.patronymic}_{self.klass}.png')

        addStudent = None

# qr = QRGeneration('Гараев','Камиль','Раушанович','10Б','Искандер',['Эльвира','Раушан'])
# qr.generateQR()
