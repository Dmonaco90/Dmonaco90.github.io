from flask import Flask, render_template, request, jsonify,send_from_directory
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)


@app.route('/')
def homepage():
    
    images = ["img/zeta2.png","img/omega.png","img/Ami.png","img/Amo.png","img/gancio.png","img/L.png","img/OmegaAsi.png","img/OmegaInt.png","img/OmegaIntAsi.png","img/u.png","img/Linea.png","img/OmegaAsi2.png","img/LineaAngolare.png","img/omega5.png","img/L45.png","img/Freccia.png","img/P.png","img/P_rovescia.png","img/Scatola.png","img/libero.png"]  
    return render_template('index.html',images=images)



app.config['MAIL_USERNAME'] = 'danielemonaco1990@gmail.com'
app.config['MAIL_PASSWORD'] = 'cuyccautdjwzjgvm'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465

app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Ottieni i dati dal form
        nome = request.form['nome']
        riferimento_ordine = request.form['riferimento_ordine']

        # Ottieni il file PDF
        if 'pdf' in request.files:
            pdf_file = request.files['pdf']
            pdf_filename = secure_filename(pdf_file.filename)

            # Crea l'email
            oggetto_email = f"{nome} - {riferimento_ordine}"
            msg = Message(oggetto_email, sender='danielemonaco1990@gmail.com', recipients=['info@lavorazionelamierelazio.com'])
            msg.body = "Ecco il tuo ordine in allegato."
            msg.attach(pdf_filename, "application/pdf", pdf_file.read())

            # Invia l'email
            mail.send(msg)
            return jsonify({'message': 'Email inviata con successo'})
        else:
            return jsonify({'error': 'File PDF mancante'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data/profili')
def profili():
    return send_from_directory('data', 'profili.json')

if __name__ == '__main__':
    app.run(debug=True)
