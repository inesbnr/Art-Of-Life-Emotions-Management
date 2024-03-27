from pylsl import StreamInlet,resolve_stream #import pylsl to use LSL and recover the data from the sensors
import time # import time to control timing
import mido # import mido to send notes to loopMidi
from mido import Message #to send message

# Obtaining output port
ports = mido.get_output_names() # liste de tout les ports ouverts
print(ports)

outport=mido.open_output(ports[1])

def initialize_stream():
    streams = resolve_stream('name', 'OpenSignals')
    stream = StreamInlet(streams[0])
    return stream

#idée logique pour le calcul du bpm
#au début on rempli la première case puis la 1ere case puis 2 e etc valeurs_minute.append(...)
#ensuite il faut supprimer la valeurs la plus ancienne valeurs_minutes.pop(0) et ajouter la nouvelle valeurs des 10 sec

#Calcul bpm sur la minute écoulée :
#il faut prendre le tableau et faire la sommes des heartbeat sur les 6 cases (car c'est les 60 secs passées)
#pour les premières cases on utilise un compteur debut=0

def calculer_bpm_debut(valeurs_minute_ecg,debut):
    # Calcul de la somme des valeurs du tableau
    bpm = sum(valeurs_minute_ecg)
    if debut==1:
        bpm=bpm*6
    if debut==2:
        bpm=bpm*3
    if debut==3:
        bpm=bpm*2
    if debut==4:
        bpm=round(bpm*1.5)
    if debut==5:
        bpm=round(bpm*1.2)
    # Affichage du résultat
    print("BPM :", bpm)
    return bpm

def calculer_resp_debut(valeurs_minute_resp,debut):
    # Calcul de la somme des valeurs du tableau
    respmin = sum(valeurs_minute_resp)
    if debut==1:
        respmin=respmin*6
    if debut==2:
        respmin=respmin*3
    if debut==3:
        respmin=respmin*2
    if debut==4:
        respmin=round(respmin*1.5)
    if debut==5:
        respmin=round(respmin*1.2)
    # Affichage du résultat
    print("Nb de resp/min :", respmin)
    return respmin

def calculer_bpm(valeurs_minute_ecg):
    # Calcul de la somme des valeurs du tableau
    bpm = sum(valeurs_minute_ecg)
    # Affichage du résultat
    print("BPM :", bpm)
    return bpm

def calculer_resp(valeurs_minute_resp):
    # Calcul de la somme des valeurs du tableau
    respmin = sum(valeurs_minute_resp)
    # Affichage du résultat
    print("Nb de resp/min :", respmin)
    return respmin

#pour la respiration, luminosité en fonction de la valeur sur opensignals
clignotement_resp=0

def map_resp_midi(value):
    # Valeur minimale et maximale de l'intervalle d'entrée
    min_input = -2
    max_input = 2

    # Valeur minimale et maximale de l'intervalle de sortie
    min_output = 0
    max_output = 127

    # Mapper la valeur à l'intervalle de sortie
    mapped_value = ((value - min_input) / (max_input - min_input)) * (max_output - min_output) + min_output

    # S'assurer que la valeur résultante est dans la plage de sortie
    mapped_value = min(max_output, max(min_output, mapped_value))

    return int(mapped_value)

in_batt=False
in_resp=False

def process_data(stream,debut,valeurs_minute_ecg,valeurs_minute_resp,data_eda): #return bpm, rpm, eda_value
    global clignotement_batt, in_batt, in_resp,in_batt_mm
    if debut<=6:
                print ("debut", debut)
                n = 0
                peak_count=0
                resp_count=0
                while n < 1000 :
                    values, timestamp = stream.pull_sample()

                    #respiration
                    if in_resp == True:
                        if values[3] < -0.1:
                            in_resp = False

                    else :
                        if values[3] > 0.1:
                            resp_count+=1
                            in_resp = True
                            print("respiration")
                            print("resp count", resp_count)
                    #mapper la valeur 3 en clignotement entre 0 et 127
                    clignotement_resp=map_resp_midi(values[3])
                    outport.send(mido.Message('control_change', control=1, value=clignotement_resp, channel=5))

                    #ecg
                    if in_batt == True:
                        if values[1] < 0:
                            in_batt = False

                    else :
                        if values[1] > 1:
                            peak_count+=1
                            in_batt = True
                            in_batt_mm=True
                            print("heartbeat")
                    #eda
                    data_eda.append(values[2])
                    n=n+1

                print("10SEC")

                valeurs_minute_resp.append(resp_count)
                valeurs_minute_ecg.append(peak_count)
                bpm=round(calculer_bpm_debut(valeurs_minute_ecg,debut))
                rpm=round(calculer_resp_debut(valeurs_minute_resp,debut))

                eda_value = sum(data_eda)/len(data_eda)
                eda_value=round(eda_value,2)
                print("EDA :", eda_value)
                return bpm, rpm, eda_value

    else:
                print ("debut>6")
                n = 0
                peak_count=0
                resp_count=0
                while n < 1000 :
                    values, timestamp = stream.pull_sample()
                    #respiration
                    if in_resp == True:
                        if values[3] < -0.1:
                            in_resp = False

                    else :
                        if values[3] > 0.1:
                            resp_count+=1
                            in_resp = True
                            print("respiration")

                    #mapper la valeur 3 en clignotement entre 0 et 127
                    clignotement_resp=map_resp_midi(values[3])
                    outport.send(mido.Message('control_change', control=1, value=clignotement_resp, channel=5))

                    #ecg
                    if in_batt == True:
                        if values[1] < 0:
                            in_batt = False

                    else :
                        if values[1] > 1:
                            peak_count+=1
                            in_batt = True
                            print("heartbeat")

                    #eda
                    data_eda.append(values[2])
                    n=n+1

                valeurs_minute_ecg.pop(0)
                valeurs_minute_ecg.append(peak_count)
                bpm=calculer_bpm(valeurs_minute_ecg)

                valeurs_minute_resp.pop(0)
                valeurs_minute_resp.append(resp_count)
                rpm=calculer_resp(valeurs_minute_resp)

                eda_value = sum(data_eda)/len(data_eda)
                eda_value=round(eda_value,2)
                print("EDA :", eda_value)
                return bpm, rpm, eda_value

#INITIALISATION OF CODE
# part of y CALM/EXCITED
stream=initialize_stream()
debut=1

#Battements du coeur
valeurs_minute_ecg=[] # liste avec 6 cases 60sec/10=6 # ECG
#Electrodermal activity of skin
data_eda = [] #create an empty list to recover the data
#Respiration
valeurs_minute_resp=[] # liste avec 6 cases 60sec/10=6 # Resp

y = 50 #initialisation du y entre 0 et 100 = on prend 50

bpm_current, resp_current, eda_current=process_data(stream,debut,valeurs_minute_ecg,valeurs_minute_resp,data_eda)

bpm_value = bpm_current
resp_value = resp_current
eda_value = eda_current

#Sends bpm value rythm
outport.send(mido.Message('control_change', control=1, value=int(((bpm_value/60)*127)/4), channel=6))

def actualiser_y(debut,stream, bpm_value, resp_value, eda_value):
    global valeurs_minute_ecg
    global data_eda
    global valeurs_minute_resp
    global y
    bpm_current, resp_current, eda_current=process_data(stream,debut,valeurs_minute_ecg,valeurs_minute_resp,data_eda)
    # Calcul des pourcentages de variation de chaque paramètres
    bpm_variation = ((bpm_current - bpm_value) /bpm_value) * 100
    resp_variation = ((resp_current - resp_value) /resp_value) * 100
    eda_variation = ((eda_current - eda_value) /eda_value) * 100

    # Moyenne des variations (faut-il faire une moyenne pondérée??)
    variation_totale = (bpm_variation + resp_variation + eda_variation) / 3

    # Mise à jour de y
    y = y + y * (variation_totale / 100)  # Diviser par 100 car les variations sont en pourcentage
    #empêcher y d'être inf à 0 et sup à 100
    if y<0:
        y=0
    if y>100:
        y=100

    # Mise à jour des valeurs pour la prochaine itération
    bpm_value = bpm_current
    resp_value = resp_current
    eda_value = eda_current

    return y, bpm_value, resp_value, eda_value

#Madmapper part :

#pour les couleurs des 3 differentes zones
def send_color(color, where):
    red_value= color[0]
    green_value= color[1]
    blue_value= color[2]

    # For each MIDI channel, send the corresponding RGB value
    if where=='bpm': #CANAL 8
        send_color_change(red_value, green_value, blue_value,7)
    if where=='rpm': #CANAL 3 et 4
        send_color_change(red_value, green_value, blue_value,2)
        send_color_change(red_value, green_value, blue_value,3)
    if where=='eda': #CANAL 5
        send_color_change(red_value, green_value, blue_value,4)

#pour la vitesse des lignes extérieures en fonction du y
def send_speed_y(y): #CANAL 2
    y=round(y)
# Sending speed values in MadMapper
    outport.send(mido.Message('control_change', control=1, value=y, channel=1))

def determine_color_bpm(value): #bpm value entre quoi et quoi ?
    # pour bpm min = 40 <=> 0% ; max = 170 <=> 100% ; pour 127 --> ?
    n=6
    liste_couleur = [
    [0, 0, 255],    # Bleu pur
    [0, 26, 230],
    [0, 51, 204],
    [0, 77, 178],
    [0, 102, 153],
    [0, 128, 128],
    [0, 153, 102],
    [0, 178, 77],
    [0, 204, 51],
    [0, 230, 26],
    [0, 255, 0],    # Vert pur
    [128, 255, 0],  # Jaune - Vert
    [255, 255, 0],  # Jaune pur
    [255, 230, 0],
    [255, 204, 0],
    [255, 178, 0],
    [255, 153, 0],
    [255, 128, 0],
    [255, 102, 0],
    [255, 77, 0],
    [255, 51, 0],
    [255, 26, 0],
    [255, 0, 0]   ]  # Rouge pur

    if value<40 or value>170:#si hors champs --> noir
        return [0,0,0]
    else:
        for i in range (22):
            if value < 40+(n*(i+1)):
                color = liste_couleur[i]
                for j in range (3):
                    c =color[j]
                    color[j]= int(c*127/255)
                return [color[0],color[1],color[2]]
#détermine la couleur resp
def determine_color_rpm(value):
     # pour rpm min = 10 <=> 0% ; max = 50 <=> 100% ; pour 127 --> ?
    couleurs = [
    # Rouge foncé
    [139, 0, 0],
    # Rouge
    [255, 0, 0],
    # Orange
    [255, 165, 0],
    # Jaune
    [255, 255, 0],
    # Bleu clair
    [173, 216, 230],
    # Bleu vert
    [0, 128, 128],
    # Lilas
    [182, 102, 210],
    # Violet
    [138, 43, 226],
    # Bleu turquoise
    [64, 224, 208],
    # Bleu foncé
    [0, 0, 139],
    # Vert foncé
    [0, 100, 0],
    # Vert clair
    [144, 238, 144],
    # Jaune clair
    [255, 255, 102]]
    n=3
    if value<10 or value>49:#si hors champs --> noir
        return [0,0,0]
    else:
        for i in range (13):
            if value < 10+(n*(i+1)):
                color = couleurs[i]
                for j in range (3):
                    c =color[j]
                    color[j]= int(c*127/255)
                return [color[0],color[1],color[2]]
#détermine la couleur eda
def determine_color_eda(value):
     # pour rpm min = 0 <=> 0% ; max = 8 <=> 100% ; pour 127 --> ?
    colors = [
    [255, 0, 0],      # Rouge pur
    [255, 64, 0],     # Rouge orangé
    [255, 128, 0],    # Orange
    [255, 191, 0],    # Jaune orangé
    [255, 255, 0],    # Jaune pur
    [191, 255, 0],    # Jaune verdâtre
    [128, 255, 0],    # Jaune vert
    [64, 255, 0],     # Vert clair
    [0, 255, 0],      # Vert pur
    [0, 255, 64],     # Vert bleuté
    [0, 255, 128],    # Vert azuré
    [0, 255, 191],    # Vert cyan
    [0, 255, 255],    # Cyan pur
    [0, 191, 255],    # Cyan bleuté
    [0, 128, 255],    # Cyan clair
    [0, 64, 255],     # Bleu cyan
    [0, 0, 255],      # Bleu pur
    [64, 0, 255],     # Bleu violet
    [128, 0, 255],    # Violet
    [191, 0, 255]  ]   # Violet foncé
    n=1
    if value<5 or value>25:#si hors champs --> noir
        return [0,0,0]
    else:
        for i in range (20):
            if value < 5+(n*(i+1)):
                color = colors[i]
                for j in range (3):
                    c =color[j]
                    color[j]= int(c*127/255)
                    
                    
                return [color[0],color[1],color[2]]
            
#send RGB values to MadMapper (0-127)
def send_color_change(red, green, blue, canal):
    outport.send(mido.Message('control_change', control=1, value=red, channel=canal))    # Red channel on channel 1
    outport.send(mido.Message('control_change', control=2, value=green, channel=canal))  # Green channel on channel 2
    outport.send(mido.Message('control_change', control=3, value=blue, channel=canal))   # Blue channel on channel 3

while True:
    if debut<=6:
        debut=debut+1

    y, bpm_value, resp_value, eda_value = actualiser_y(debut,stream, bpm_value, resp_value, eda_value)

    #BPM value speed
    outport.send(mido.Message('control_change', control=1, value=int(((bpm_value/60)*127)/4), channel=6))

    #Envoie la valeur du y : calm/excited pour déterminer la vitesse des lignes
    send_speed_y(y)
    
    # Sending color variations for each zone to MadMapper
    couleur_bpm = determine_color_bpm(bpm_value)
    send_color(couleur_bpm,'bpm')

    couleur_rpm = determine_color_rpm(resp_value)
    send_color(couleur_rpm,'rpm')

    couleur_eda = determine_color_eda(eda_value)
    send_color(couleur_eda,'eda')
