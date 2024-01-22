import smtplib

try:
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login('monacodaniele1990@live.it', 'Oblivion2024!')
    server.sendmail('monacodaniele1990@live.it', 'monacodaniele1990@live.it', 'Test email body')
    server.quit()
    print("Email inviata con successo")
except Exception as e:
    print("Errore nell'invio dell'email:", e)

