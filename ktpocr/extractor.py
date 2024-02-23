import cv2
import re
import pytesseract
from ktpocr.form import KTPInformation

class KTPOCR(object):
    def __init__(self, image):
        self.image = cv2.imread(image)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.th, self.threshed = cv2.threshold(self.gray, 127, 255, cv2.THRESH_TRUNC)
        self.result = KTPInformation()
        self.master_process()

    def process(self, image):
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        raw_extracted_text = pytesseract.image_to_string((self.threshed), lang="ind")
        return raw_extracted_text

    def word_to_number_converter(self, word):
        word_dict = {
            '|' : "1"
        }

        res = ""

        for letter in word:
            if letter in word_dict:
                res += word_dict[letter]
            else:
                res += letter
        
        return res


    def nik_extract(self, word):
        word_dict = {
            'b' : "6",
            'e' : "2",
            '?' : "",
            'L' : "1",
        }
        
        res = ""
        
        for letter in word:
            if letter in word_dict:
                res += word_dict[letter]
            else:
                res += letter
        
        return res
    
    def extract(self, extracted_result):
        replace_table = str.maketrans({'—': '', '“': '', '.': '', ':': '', '|': '', '/': ''})
        remove_dash = str.maketrans({'-': ' '})
        
        for word in extracted_result.split("\n"):
            if "NIK" in word:
                word = word.split(':')
                self.result.nik = self.nik_extract(word[-1].replace(" ", "")).replace("NIK", "").translate(replace_table).translate(remove_dash)
                continue

            if "Nama" in word:
                word = word.split(':')
                self.result.nama = word[-1].replace('Nama ','').translate(replace_table).translate(remove_dash)
                continue

            if "Tempat" in word:
                word = word.split(':')
                try:
                    self.result.tanggal_lahir = re.search("([0-9]{2}\-[0-9]{2}\-[0-9]{4})", word[-1])[0].translate(replace_table)
                    self.result.tempat_lahir = word[-1].replace(". "+self.result.tanggal_lahir, '').translate(replace_table)
                except:
                    self.result.tanggal_lahir = ""
                    self.result.tempat_lahir = ""

                continue

            if 'Darah' in word:
                if re.search("(LAKI-LAKI|LAKI|LELAKI|PEREMPUAN)", word) is None:
                    self.result.jenis_kelamin = ""
                else:
                    self.result.jenis_kelamin = re.search("(LAKI-LAKI|LAKI|LELAKI|PEREMPUAN)", word)[0].translate(replace_table)

                word = word.split(':')

                try:
                    self.result.golongan_darah = re.search("(O|A|B|AB)", word[-1])[0].translate(replace_table).translate(remove_dash)
                except:
                    self.result.golongan_darah = '-'

            if 'Alamat' in word:
                self.result.alamat = self.word_to_number_converter(word).replace("Alamat ","").translate(replace_table).translate(remove_dash)

            if 'NO.' in word:
                self.result.alamat = self.result.alamat + ' '+word.translate(replace_table).translate(remove_dash)

            if "Kecamatan" in word:
                if len(word.split(':')) > 1:
                    self.result.kecamatan = word.split(':')[1].strip().translate(replace_table).translate(remove_dash)

            if "Desa" in word:
                wrd = word.split()
                desa = []
                for wr in wrd:
                    if not 'desa' in wr.lower():
                        desa.append(wr)
                self.result.kelurahan_atau_desa = ''.join(wr).translate(replace_table).translate(remove_dash)

            if 'Kewarganegaraan' in word:
                if len(word.split(':')) > 1:
                    self.result.kewarganegaraan = word.split(':')[1].strip().translate(replace_table).translate(remove_dash)

            if 'Pekerjaan' in word:
                wrod = word.split()
                pekerjaan = []
                for wr in wrod:
                    if not '-' in wr:
                        pekerjaan.append(wr)
                self.result.pekerjaan = ' '.join(pekerjaan).replace('Pekerjaan', '').strip().translate(replace_table)

            if 'Agama' in word:
                self.result.agama = word.replace('Agama',"").strip().translate(replace_table).translate(remove_dash)

            if 'Perkawinan' in word:
                self.result.status_perkawinan = word.split(':')[1].translate(replace_table).translate(remove_dash)

            if "RTRW" in word:
                word = word.replace("RTRW",'')

                if word is None:
                    self.result.rt = ""
                    self.result.rw = ""
                else:
                    try:
                        if len(word.split('/')) > 1:
                            self.result.rt = word.split('/')[0].strip().translate(replace_table).translate(remove_dash)
                            self.result.rw = word.split('/')[1].strip().translate(replace_table).translate(remove_dash)
                    except:
                        self.result.rt = ""
                        self.result.rw = ""

    def master_process(self):
        raw_text = self.process(self.image)
        self.extract(raw_text)

    def res(self):
        return self.result.__dict__



