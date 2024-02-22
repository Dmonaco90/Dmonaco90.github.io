from flask import Flask, render_template, request, jsonify,send_from_directory
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
from werkzeug.utils import secure_filename
import base64
import os
import json
import logging
from google.cloud import logging as cloud_logging
from google.cloud import storage

# Configura il client di logging di Google Cloud
client = cloud_logging.Client()
client.setup_logging()

app = Flask(__name__)
CORS(app)

# Configura il livello di logging di Flask
logging.basicConfig(level=logging.INFO)


def init_storage_client():
    # Inizializza il client di Google Cloud Storage
    return storage.Client()

def save_color_to_storage(data):
    print("entro save")
    bucket_name='sitolamiere.appspot.com'
    filename='colori.json'
    storage_client = init_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
     # Aggiunto il blocco try-except per il debug della serializzazione JSON
    try:
        json_string = json.dumps(data)
        print("Dati serializzati con successo:", json_string)  # Stampa per debug
    except TypeError as e:
        print("Errore nella serializzazione dei dati:", e)
        # Qui puoi decidere come gestire l'errore, ad esempio ritornare un errore al client
        return {"error": f"Impossibile serializzare i dati: {e}"}

    # Procede con il caricamento dei dati serializzati su Google Cloud Storage
    blob.upload_from_string(json_string, content_type='application/json')
    print("colori salvati")

def load_color_from_storage(bucket_name='sitolamiere.appspot.com', filename='colori.json'):
    print("entro load")
    storage_client = init_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    json_data = json.loads(blob.download_as_string(client=None))
    print("colori caricati")
    return json_data

def load_profile_from_storage(bucket_name='sitolamiere.appspot.com', filename='profili.json'):
    print("entro load profili")
    storage_client = init_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    json_data = json.loads(blob.download_as_string(client=None))
    print("profili caricati")
    return json_data

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
    #return send_from_directory('data', 'profili.json')
    return jsonify(load_profile_from_storage())

@app.route('/data/colori')
def colori():
    return jsonify(load_color_from_storage())



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
    bucket_name = 'sitolamiere.appspot.com'
    filename = 'colori.json'  # Nome del file JSON da modificare

    # Carica i dati esistenti da Google Cloud Storage
    data = load_color_from_storage(bucket_name=bucket_name, filename=filename)
   
    print(data)  # Stampa i dati per debugging

    # Supponendo che la richiesta POST invii i dati in JSON nel corpo della richiesta
    request_data = request.get_json()
    materiale = request_data.get('materiale')
    nuovo_colore = request_data.get('colore')
    
    # Trasforma "Alluminio" in "Verniciato" se necessario
    if materiale == 'Alluminio':
        materiale = 'Verniciato'

    # Aggiungi il nuovo colore alla categoria corretta
    if materiale in data:
        if nuovo_colore not in data[materiale]:
            data[materiale].append(nuovo_colore)
        else:
            return jsonify({'error': 'Colore già esistente'}), 400
    else:
        return jsonify({'error': 'Materiale non valido'}), 400

    # Salva i dati modificati su Google Cloud Storage
    save_color_to_storage(data)

    return jsonify({'message': 'Colore aggiunto con successo'})


@app.route('/modify_color', methods=['POST'])
def modify_color():
    data = request.json
    print(data)  # Stampa per debug
    materiale = data['materiale']
    coloreVecchio = data['coloreVecchio']
    colore = data['colore']
    
    try:
        # Carica il file JSON esistente da Google Cloud Storage
        colori = load_color_from_storage()
        
        if coloreVecchio in colori[materiale]:
            # Rimuove il vecchio colore e aggiunge il nuovo
            colori[materiale].remove(coloreVecchio)
            colori[materiale].append(colore)
            
            # Salva il file JSON modificato su Google Cloud Storage
            save_color_to_storage(colori)
            return jsonify({'message': 'Colore modificato con successo'}), 200
        else:
            return jsonify({'error': 'Colore non trovato'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_color', methods=['POST'])
def delete_color():
    data = request.json
    print(data)  # Stampa per debug
    materiale = data['materiale']
    colore = data['colore']
    
    try:
        # Carica il file JSON esistente da Google Cloud Storage
        colori = load_color_from_storage()
        
        if colore in colori[materiale]:
            # Rimuove il colore
            colori[materiale].remove(colore)
            
            # Salva il file JSON modificato su Google Cloud Storage
            save_color_to_storage(colori)
            return jsonify({'message': 'Colore eliminato con successo'}), 200
        else:
            return jsonify({'error': 'Colore non trovato'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/modify_profile', methods=['POST'])
def modify_profile():
    data = request.json
    profile_id = data['id']
    new_scalatures = data['scalature']

    # Percorso al file JSON dei profili
    json_file_path = 'data/profili.json'

    # Carica il JSON dei profili
    with open(json_file_path, 'r+') as file:
        data = json.load(file)  # Carica il contenuto del file JSON in un dizionario
        profili = data.get('profili', [])  # Ottieni la lista dei profili, se esiste, altrimenti usa una lista vuota

        # Trova il profilo da modificare e aggiorna le scalature
        for profilo in profili:
            if profilo['id'] == profile_id:
                profilo['scalature'] = new_scalatures
                break

        # Riporta il cursore all'inizio del file e sovrascrivi con i nuovi dati
        file.seek(0)
        json.dump(data, file, indent=4)  # Assicurati di scrivere l'oggetto 'data' completo, non solo 'profili'
        file.truncate()

    return jsonify({'message': f'Scalature per il profilo {profile_id} modificate con successo!'})

if __name__ == '__main__':
    app.run(debug=True)
    


