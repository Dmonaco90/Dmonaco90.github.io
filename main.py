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

def save_mats_to_storage(data):
    print("entro save mats")
    bucket_name='sitolamiere.appspot.com'
    filename='materiali.json'
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
    print("materiali salvati")
   
def save_profile_to_storage(data):
    print("entro save profile")
    bucket_name='sitolamiere.appspot.com'
    filename='profili.json'
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
    print("profili salvati")

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

def load_mats_from_storage(bucket_name='sitolamiere.appspot.com', filename='materiali.json'):
    storage_client = init_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    json_data = json.loads(blob.download_as_string())
    return json_data

def upload_image_to_gcs(bucket_name, image_content, image_filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('img/' + image_filename)  # 'img/' è la cartella nel tuo bucket
    blob.upload_from_string(image_content, content_type='image/png')
    blob.make_public()
    return blob.public_url

def aggiungi_colore_a_materiale(data, materiale, colori):
    if materiale == 'Alluminio':
        materiale = 'Verniciato'
    
    if materiale not in data:
        data[materiale] = []

    for colore in colori:
        if colore not in data[materiale]:
            data[materiale].append(colore)

def save_materiale_con_colori():
    bucket_name = 'sitolamiere.appspot.com'
    filename = 'colori.json'
    data = load_color_from_storage(bucket_name=bucket_name, filename=filename)
    request_data = request.get_json()
    materiale = request_data.get('materiale')
    colori = request_data.get('colori')  # Assumi che 'colori' sia una lista di colori

    aggiungi_colore_a_materiale(data, materiale, colori)
    save_color_to_storage(data)
    return jsonify({'message': f'Materiale {materiale} e colori aggiunti con successo'})

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
        
        
        if ',' in imageSrc:
            image_data = imageSrc.split(',')[1]
            image = base64.b64decode(image_data)
        else:
            return jsonify({'error': 'Formato immagine non valido'}), 400

        profile_name = data['profileName']
        idProfile = profile_name + "_new"
        json_file_path = 'profili.json'  # Il nome del file nel bucket
        image_filename = f'{profile_name}.png'
        # Carica il file JSON dei profili da GCP
        profili = load_color_from_storage(filename=json_file_path)

        if any(profilo['id'] == profile_name for profilo in profili['profili']):
            return jsonify({'error': 'Attenzione! Nome profilo già esistente.'}), 400

        # Procedi con il salvataggio dell'immagine su bucket
        image_data = data['imageSrc'].split(',')[1]
        image = base64.b64decode(image_data)
        image_url = upload_image_to_gcs('sitolamiere.appspot.com', image, image_filename)
        
        input_boxes = []
        quote_values = data['containerInputQuoteValues']
        print(quote_values)
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
                url = "https://storage.googleapis.com/sitolamiere.appspot.com/img/freccia_interna.png"
                id = "1"
            else:
                url = "https://storage.googleapis.com/sitolamiere.appspot.com/img/freccia_esterna.png"
                id = "2"
            vern_box = {
                "id": f"scelta{id}",  # Genera un ID univoco basato sull'indice
                "top": img_values[i] + "%",  # Il valore di "top"
                "left": img_values[i + 1] + "%",  # Il valore di "left"
                "url": url
            }
            vern_boxes.append(vern_box)
            
        scalature = {}
        scala_values = data['listaSviluppoValues']
        
        # Aggiungi le coppie chiave-valore per ogni spessore
        for spessore, valore in scala_values.items():
            scalature[spessore] = int(valore)

        
        
        # Prepara i dati del nuovo profilo
        nuovo_profilo = {
            "id": idProfile,
            "imageUrl": image_url,  # Adatta se necessario per immagini caricate su GCS
            "inputBoxes": input_boxes,
            "vernBoxes": vern_boxes,
            "scalature": scalature
        }
        
        # Aggiungi il nuovo profilo ai profili esistenti e salva su GCS
        profili['profili'].append(nuovo_profilo)
        save_profile_to_storage(profili)
        
        
        return jsonify({'message': 'Profilo salvato con successo'})
    except Exception as e:
        print("Si è verificato un errore:", str(e))
        return jsonify({'error': 'Si è verificato un errore interno del server'}), 500
    
    
@app.route('/save_color', methods=['POST'])
def save_color():
    bucket_name = 'sitolamiere.appspot.com'
    filename = 'colori.json'
    data = load_color_from_storage(bucket_name=bucket_name, filename=filename)
    request_data = request.get_json()
    materiale = request_data.get('materiale')
    nuovo_colore = [request_data.get('colore')]  # Metti il colore in una lista per uniformità

    aggiungi_colore_a_materiale(data, materiale, nuovo_colore)
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

    # Nome del bucket e del file nel bucket
    bucket_name = 'sitolamiere.appspot.com'
    file_name = 'profili.json'
    
    # Inizializza il client di Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    # Leggi il contenuto esistente del file JSON dal bucket
    json_data = json.loads(blob.download_as_string(client=None))
    
    # Ottieni la lista dei profili, se esiste, altrimenti usa una lista vuota
    profili = json_data.get('profili', [])
    
    # Trova il profilo da modificare e aggiorna le scalature
    for profilo in profili:
        if profilo['id'] == profile_id:
            profilo['scalature'] = new_scalatures
            break

    # Sovrascrivi il file nel bucket con i nuovi dati
    blob.upload_from_string(json.dumps(json_data, indent=4), content_type='application/json')
    
    return jsonify({'message': f'Scalature per il profilo {profile_id} modificate con successo!'})

@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    # Ottieni l'ID del profilo da eliminare dalla richiesta
    data = request.json
    profile_id = data['id']

    # Nome del bucket e del file nel bucket
    bucket_name = 'sitolamiere.appspot.com'
    file_name = 'profili.json'
    
    # Inizializza il client di Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    # Leggi il contenuto esistente del file JSON dal bucket
    json_data = json.loads(blob.download_as_string(client=None))
    
    # Ottieni la lista dei profili
    profili = json_data.get('profili', [])
    
    # Rimuovi il profilo con l'ID specificato
    profili = [profilo for profilo in profili if profilo['id'] != profile_id]
    
    # Aggiorna la lista dei profili nel dizionario json_data
    json_data['profili'] = profili

    # Sovrascrivi il file nel bucket con i nuovi dati
    blob.upload_from_string(json.dumps(json_data, indent=4), content_type='application/json')
    
    return jsonify({'message': f'Profilo {profile_id} eliminato con successo!'})


@app.route('/carica_pesi_materiali', methods=['GET'])
def carica_pesi_materiali():
    try:
        # Carica tutti i dati dei materiali dal storage
        dati_materiali = load_mats_from_storage()  # Assumi che questa funzione carichi i dati da Google Cloud Storage
        print("dati materiali")
        print(dati_materiali)
        return jsonify(dati_materiali)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/save_mats', methods=['POST'])
@app.route('/save_mats', methods=['POST'])
@app.route('/save_mats', methods=['POST'])
def save_mats():
    # Carica i dati esistenti da Google Cloud Storage
    data = load_mats_from_storage()
   
    # Ottiene i dati dalla richiesta POST
    request_data = request.get_json()
    materiale = request_data.get('materiale')
    tipologia = request_data.get('tipologia')
    peso = request_data.get('peso')
    spessori = request_data.get('spessori')
    colori = request_data.get('colori')

    # Prepara i dati del nuovo materiale
    nuovo_materiale_data = {
        "peso": peso,
        "spessore": spessori,
        "tipologia": [tipologia]  # Assicurati che tipologia sia una lista
    }

    # Aggiungi il nuovo materiale al JSON
    if materiale not in data:
        # Se il materiale non esiste, aggiungi un nuovo array con un oggetto
        data[materiale] = [nuovo_materiale_data]
    else:
        # Se il materiale esiste già, potresti voler aggiungere nuove tipologie, spessori o aggiornare il peso
        # Qui puoi decidere la logica specifica, ad esempio aggiungere nuove tipologie o spessori
        return jsonify({'error': 'Materiale già esistente. Considerare l\'aggiunta di nuove tipologie o spessori tramite un\'altra funzione.'}), 400
    
    # Salva i dati modificati su Google Cloud Storage
    save_mats_to_storage(data)

    return jsonify({'message': 'Materiale aggiunto con successo'})



if __name__ == '__main__':
    app.run(debug=True)
    


