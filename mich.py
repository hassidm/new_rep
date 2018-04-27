from fuzzywuzzy import fuzz
from googletrans import Translator
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imghdr

def best_word(list_of_words, word_to_find):
    """
    picks the closest worf from the list to the word to find
    :return: the best word or None if not found any close enough.
    """
    best_ratio = 0
    bst_word = None

    for word in list_of_words:
        if fuzz.partial_ratio(word, word_to_find) > best_ratio:
            best_ratio = fuzz.partial_ratio(word, word_to_find)
            bst_word = word
    if bst_word is not None and best_ratio > 50:
        return bst_word
    return None

def my_trans(word):
    tran = Translator(service_urls=['translate.google.com',
                                    'translate.google.co.il',])
    new = tran.translate(word)
    return new.text


def send_mail(address_mail, name, subject_text, body_text):

    # Specifying the from and to addresses

    fromaddr = 'meditakeisrael@gmail.com'
    toaddrs = address_mail

    # Writing the message (this message will appear in the email)

    final_msg = MIMEMultipart('alternative')
    final_msg["Subject"] = name + ", " + subject_text

    img_url = "https://media.giphy.com/media/UJg0aZmim0Yc8/giphy.gif"
    header = "שלום " + name
    msgText = MIMEText(
        """<html><head></head><body style='font-family="Alef Hebrew";'>
        <div align="right">
        <br>
        <h1>%s</h1>
        <br>
        %s
        <br><br><br>
        <img src="https://i.imgur.com/e2MDDEt.png"/>
        </div>
        </body></html>""" %(header, body_text), 'html')
    final_msg.attach(msgText)

    # Gmail Login

    username = 'meditakeisrael'
    password = 'netta1234'

    # Sending the mail

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)

    server.sendmail(fromaddr, [toaddrs], final_msg.as_string())
    server.quit()


if __name__ == "__main__":
    send_mail("hassidm@gmail.com", "דורון", "מצאנו לך מחלה!", "נא לתקשר עם:")