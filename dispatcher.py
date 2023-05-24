from flask import Flask,request, jsonify
import re
import requests
import time
def validate_ip_address(ip_address):
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return bool(re.match(pattern, ip_address))

app = Flask(__name__)

players_map = {}
players_name_ip_map = {}
TMP_BANN = 3 #secondes


@app.route('/connect', methods=['POST'])
def connect():
    player_name = request.json.get('player_name')
    robot_ip_address = request.json.get('ip_address')
    requester_ip = request.remote_addr
    if not player_name != "" or not validate_ip_address(robot_ip_address):
        return jsonify({'error': 'Adresse IP invalide ou nom du player vide'}), 400
    
    if not players_name_ip_map.get(player_name) == None:
        return jsonify({'error': 'Ce nom est déja utilisé'}), 402
    
    # Todo étudier le cas de l'unicité d'une ip d'un robot
    players_map[requester_ip] = (player_name, robot_ip_address, 0)#Nom de l'équipe, ADR du robot, nombre de bonus
    players_name_ip_map[player_name] = requester_ip
   
    print((player_name, robot_ip_address, requester_ip ))
    print(players_map)
    return 'Connecté avec succès'

@app.route('/getList', methods=['GET'])
def get_list():
    response = {'data': list(players_name_ip_map.keys()), "liste":str(players_map) }
    return jsonify(response)

@app.route('/account', methods=['GET'])
def account():
    requester_ip = request.remote_addr
    
    result = players_map.get(requester_ip)
    
    if result == None:
        return jsonify({'error': 'Vous n\'etes pas inscrit'}), 400
    
    return result[2]

@app.route('/sendCommand', methods=['POST'])
def sendCommand():
    type = request.json.get('type')
    payload = request.json.get('payload')
    requester_ip = request.remote_addr
    if type == None :
        return jsonify({'error': 'type vide'}), 400 
    # Todo

    tmp_result = players_map.get(requester_ip)
    if tmp_result == None:
            return jsonify({"error":"Vous n'etes pas inscrit !! "}), 404
    
    tmp_to_dbann = banned_map.get(requester_ip)
    if tmp_to_dbann != None and tmp_to_dbann > int(time.time()):
        return jsonify({"error":"Vous êtes encore bloqué par un malus !! "}), 402
    banned_map[requester_ip] = None

    
    
    data = {
        "type":type,
        "payload":payload
    }

    response = requests.post("http://"+tmp_result[1]+':5400/sendCommand', json=data)
   
    if response.status_code < 400:
        print("commande envoyé!")
    else:
        print("Erreur lors de l'envoi de la commande. Code de statut:", response.status_code)

    print ((type, payload))
    return "ok",201


banned_map = {}  #{ip_banned : time + DUREE_DU_BANN}

@app.route('/sendPenalty', methods=['POST'])
def sendPenalty():
    
    player = request.json.get('player')
    requester_ip = request.remote_addr
    tmp_result = players_map.get(requester_ip) #(nom_robot, ip_robot, bonus (int default0))

    if tmp_result == None:
        return jsonify({'error': 'vous n\'etes pas inscrit'}), 404
    
    if tmp_result[2] == 0:
        return jsonify({'error': 'vous n\'avez pas de bonus'}), 404


    if players_name_ip_map.get(player) == None:
        return jsonify({'error': 'Le player ciblé n\'est pas inscrit'}), 404

    ip_cible = players_name_ip_map.get(player)

    banned_map[ip_cible] =  int(time.time())+TMP_BANN
    return 'bonus activé', 201

            
    


@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5500, debug=True)
