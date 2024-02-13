from flask import Flask, render_template, request, jsonify,send_from_directory
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
from werkzeug.utils import secure_filename
import base64
import os
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def homepage():
    
    images = ["img/zeta2.png","img/omega.png","img/Ami.png","img/Amo.png","img/gancio.png","img/L.png","img/OmegaAsi.png","img/OmegaInt.png","img/OmegaIntAsi.png","img/u.png","img/Linea.png","img/OmegaAsi2.png","img/LineaAngolare.png","img/omega5.png","img/L45.png","img/Freccia.png","img/P.png","img/P_rovescia.png","img/Scatola.png","img/libero.png"]  
    return render_template('index.html',images=images)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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

@app.route('/data/colori')
def colori():
    return send_from_directory('data', 'colori.json')



@app.route('/save_profile', methods=['POST'])
def save_profile():
    try:
        data = request.json
        imageSrc = data.get('imageSrc', '')

        # Verifica e divide la stringa imageSrc
        if ',' in imageSrc:
            image_data = imageSrc.split(',')[1]
            image = base64.b64decode(image_data)
        else:
            # Gestisce il caso in cui la stringa imageSrc non è nel formato atteso
            return jsonify({'error': 'Formato immagine non valido'}), 400
    
    
        for key, value in data.items():
            print(f'{key}: {value}')
        # Controlla se tutti i campi richiesti sono presenti e non vuoti
        required_fields = ['imageSrc', 'profileName', 'containerInputQuoteValues', 'listaSviluppoValues', 'containerInputImmaginiValues']
       
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo mancante o vuoto: {field}'}), 400

        json_file_path = 'data/profili.json'
        profile_name = data['profileName']
        idProfile = profile_name+"_new"
        # Carica il file JSON dei profili per controllare se il nome esiste già
        with open(json_file_path, 'r') as json_file:
            profili = json.load(json_file)
            if any(profilo['id'] == profile_name for profilo in profili['profili']):
                # Il nome del profilo esiste già
                return jsonify({'error': 'Attenzione! Nome profilo già esistente.'}), 400

        # Procedi con il salvataggio dell'immagine
        image_data = data['imageSrc'].split(',')[1]
        image = base64.b64decode(image_data)
        image_filename = f'{profile_name}.png'
        image_filepath = os.path.join('static', 'img', image_filename)

        # Salva l'immagine
        with open(image_filepath, 'wb') as f:
            f.write(image)

        
        input_boxes = []
        quote_values = data['containerInputQuoteValues']
        for i in range(0, len(quote_values), 2):
            input_box = {
                "id": f"lato{i // 2 + 1}",  # Genera un ID univoco basato sull'indice
                "top": quote_values[i] + "%",  # Il valore di "top"
                "left": quote_values[i + 1] + "%",  # Il valore di "left"
                "placeholder": "x"
            }
            input_boxes.append(input_box)
        
        vern_boxes = []
        img_values = data['containerInputImmaginiValues']
        for i in range(0, len(img_values), 2):
            if i == 0:
                url = "static/img/freccia_interna.png"
                id = "1"
            else:
                url = "static/img/freccia_esterna.png"
                id = "2"
            vern_box = {
                "id": f"scelta{id}",  # Genera un ID univoco basato sull'indice
                "top": img_values[i] + "%",  # Il valore di "top"
                "left": img_values[i + 1] + "%",  # Il valore di "left"
                "url": url
            }
            vern_boxes.append(vern_box)
            
        scalature = []
        scala_values = data['listaSviluppoValues']
        scalatura = {"id": idProfile}  # Inizia con l'ID del profilo
        # Aggiungi le coppie chiave-valore per ogni spessore
        for spessore, valore in scala_values.items():
            scalatura[spessore] = valore

        # Aggiungi l'oggetto scalatura alla lista delle scalature
        scalature.append(scalatura)
        
        with open(json_file_path, 'r+') as json_file:
            profili = json.load(json_file)
            
            nuovo_profilo = {
                "id": idProfile,  # Genera un ID univoco
                "imageUrl": image_filepath.replace("\\", "/"),  # Sostituisci "\\" con "/"
                "inputBoxes": input_boxes , # Aggiungi la sezione "inputBoxes"
                "vernBoxes" :vern_boxes,
                "Scalature": scalature
            }   
            profili['profili'].append(nuovo_profilo)
            json_file.seek(0)  # Riposiziona all'inizio del file
            json.dump(profili, json_file, indent=4)

        return jsonify({'message': 'Profilo salvato con successo'})
    except Exception as e:
        print("Si è verificato un errore: ", str(e))
        return jsonify({'error': 'Si è verificato un errore interno del server'}), 500
    
    
@app.route('/save_color', methods=['POST'])
def save_color():
    data = request.json
   
    print(data)  # Aggiungi questa riga per stampare i dati ricevuti
    materiale = data.get('materiale')
    nuovo_colore = data.get('colore')
   # Trasforma "Alluminio" in "Verniciato" se necessario
    if materiale == 'Alluminio':
        materiale = 'Verniciato'
    # Carica il file JSON dei colori
    with open('data/colori.json', 'r+') as json_file:
        colori = json.load(json_file)
        
        # Aggiungi il nuovo colore alla categoria corretta
        if materiale in colori:
            if nuovo_colore not in colori[materiale]:
                colori[materiale].append(nuovo_colore)
            else:
                return jsonify({'error': 'Colore già esistente'}), 400
        else:
            return jsonify({'error': 'Materiale non valido'}), 400

        # Riporta il cursore all'inizio del file e sovrascrivilo con i nuovi dati
        json_file.seek(0)
        json.dump(colori, json_file, indent=4)
        json_file.truncate()  # Rimuovi il contenuto residuo del file

    return jsonify({'message': 'Colore aggiunto con successo'})

@app.route('/modify_color', methods=['POST'])
def modify_color():
    data = request.json
    print(data)  # Stampa per debug
    materiale = data['materiale']
    coloreVecchio = data['coloreVecchio']
    coloreNuovo = data['coloreNuovo']
    
    try:
        with open('data/colori.json', 'r+') as file:
            colori = json.load(file)
            if coloreVecchio in colori[materiale]:
                # Rimuove il vecchio colore e aggiunge il nuovo
                colori[materiale].remove(coloreVecchio)
                colori[materiale].append(coloreNuovo)
                file.seek(0) # Riporta il cursore all'inizio del file
                json.dump(colori, file, indent=4)
                file.truncate() # Rimuove il contenuto residuo del file
                return jsonify({'message': 'Colore modificato con successo'}), 200
            else:
                return jsonify({'error': 'Colore non trovato'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
    


