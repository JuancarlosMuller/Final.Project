from flask import Flask, jsonify, request
from models import User, Profile, Genero, Game, FriendRequest, Match
import requests
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
import logging
from datetime import datetime
from flask import make_response
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['ENV'] = "development"
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(filename="app.log", level=logging.INFO)

jwt = JWTManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SECRET_KEY"] = "123456"  # Mi propia clave secreta
app.config["JWT_SECRET_KEY"] = "123456"
db.init_app(app)


# Configura migraciones
migrate = Migrate(app, db)  # Configura las migraciones


# Configuracion Flask-Admin
admin = Admin(app, name="Admin", template_mode="bootstrap3")


# Modifico la clase UserAdmin para manejar la contraseña
class UserAdminView(ModelView):
    column_exclude_list = [
        "password_hash"
    ]  # Excluir el campo de contraseña en la vista
    
    def create_model(self,form):
        user=User()
        form.populate_obj(user) # Aplicar cambio password hash.
        profile=Profile()
        user.password_hash=generate_password_hash(form.password_hash.data)
        user.profile=profile
        self.session.add(user)
        self.session.commit()
        return True

# Agrego la vista personalizada de UserAdmin al admin
admin.add_view(UserAdminView(User, db.session))
admin.add_view(ModelView(Profile, db.session))

# validacion de Inicio de Sesion con metodo POST.
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password_hash, password):
            # Autenticación exitosa
            logging.info(f"Autenticación exitosa para el usuario: {username}")
            token = create_access_token(identity=user.id)  # Genera el token JWT
            user_id = user.id
            return jsonify({"token": token, "message": "Autenticación exitosa", "user_id": user_id})
        else:
            # Autenticación fallida, contraseña incorrecta
            logging.warning(
                f"Autenticación fallida para el usuario: {username} (contraseña incorrecta)"
            )
    else:
        # Autenticación fallida, usuario no encontrado
        logging.warning(
            f"Autenticación fallida para el usuario: {username} (usuario no encontrado)"
        )

    # Devuelve un mensaje de error
    return jsonify({"message": "Credenciales incorrectas"}), 401


# Ruta para obtener la lista de usuarios en formato JSON
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()  # Obtén todos los usuarios de la base de datos
    user_list = []  # Crea una lista para almacenar los usuarios en formato JSON

    # Itera sobre los usuarios y crea un diccionario JSON para cada uno
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "mail": user.mail,
            "subscription_date": user.suscription_date.strftime("%Y-%m-%d %H:%M:%S"),
            "last_name": user.last_name,
            "first_name": user.first_name
            # Asegúrate de formatear la fecha como desees
        }
        user_list.append(user_data)  # Agrega el usuario a la lista

    return jsonify(
        {"users": user_list}
    )  # Devuelve la lista de usuarios en formato JSON

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)  # Obtén el usuario por su ID
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404  # Retorna un mensaje de error si el usuario no se encuentra

    # Crear un diccionario con los datos del usuario
    user_data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "birth_date": user.birth_date.strftime("%Y-%m-%d")  # Formatea la fecha como desees
    }

    return jsonify(user_data)  # Retorna los datos del usuario en formato JSON


@app.route("/signup", methods=["POST"])
def signup():
    user=User()
    data = request.get_json()
    username = data.get("username")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    profile=Profile()
    user.profile=profile
    genero=Genero()
    user.genero=genero
    
    # Formato datetime
    birth_date_str = data.get("birth_date")
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")

    gender = data.get("gender")
    suscription_date = datetime.utcnow()
  
    # Verifica si el usuario o el correo ya existen en la base de datos
    existing_user = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(mail=email).first()

    if existing_user:
        return jsonify({"message": "El nombre de usuario ya existe"}), 400
    if existing_email:
        return jsonify({"message": "El correo electrónico ya está registrado"}), 400

    # Crea un nuevo usuario y almacena la contraseña en formato hash
    new_user = User(
        username=username,
        mail=email,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        gender=gender,
        suscription_date=suscription_date
    )
    new_user.set_password(password) 
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario creado con éxito"}), 201

#Enpoint usuario por ID
@app.route("/user/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    profile_data = {
        "nombre": user.first_name,
        "apellido": user.last_name,
        "fecha_de_nacimiento": user.birth_date.strftime("%Y-%m-%d")
    }

    return jsonify(profile_data)

#Enpoint para actualizar nombre y apellido
@app.route('/user/<int:user_id>/profile', methods=['PUT'])
def update_user_profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    # Validación del nombre
    first_name = data.get('first_name', user.first_name)
    if not first_name.isalpha():
        return jsonify({'error': 'El nombre solo puede contener letras'}), 400

    # Validación del apellido
    last_name = data.get('last_name', user.last_name)
    if not last_name.isalpha():
        return jsonify({'error': 'El apellido solo puede contener letras'}), 400

    user.first_name = first_name
    user.last_name = last_name

    db.session.commit()

    return jsonify({'message': 'Profile updated successfully'})



#End point guardar intereses
@app.route('/generos', methods=['POST'])
def agregar_generos():
    try:
        data = request.json

        # Obtén el ID de usuario proporcionado en los datos (DEBE SER POR CONTEXT)
        user_id = data["user_id"]

        # Obténgo los géneros del arreglo en los datos
        genero = data["genero"]

        
        # Agrego los nuevos géneros seleccionados por el usuario
        for genero_nombre in genero:
            genero = Genero(genero=genero_nombre, user_id=user_id)  # Asigno el user_id directamente
            db.session.add(genero)

        # Guardo los cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Géneros almacenados exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/game', methods=['POST'])
def agregar_games():
    try:
        data = request.json

        # Obtén el ID de usuario proporcionado en los datos (DEBE SER POR CONTEXT)
        user_id = data["user_id"]

        # Obtén los juegos del arreglo en los datos
        juegos = data["games"] 

        # Agrega los nuevos juegos seleccionados por el usuario
        for juego_nombre in juegos: 
            juego = Game(games=juego_nombre, user_id=user_id)  # Debe ir por context
            db.session.add(juego)

        # Guarda los cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Juegos almacenados exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/Home", methods=["GET"])
@jwt_required()  # Protege la ruta con autenticación JWT
def home():
    
    return jsonify({"message": "Bienvenido a la ruta privada Home"})  

@app.route("/Intereses", methods=["GET"])
@jwt_required()  # Protege la ruta con autenticación JWT
def intereses():
    
    return jsonify({"message": "Bienvenido a la ruta privada Intereses"})  
    
@app.route("/Group", methods=["GET"])
@jwt_required()  # Protege la ruta con autenticación JWT
def group():
    
    return jsonify({"message": "Bienvenido a la ruta privada Group"})  

@app.route("/Matchpreview", methods=["GET"])
@jwt_required()  # Protege la ruta con autenticación JWT
def matchpreview():
    
    return jsonify({"message": "Bienvenido a la ruta privada Matchpreview"}) 

@app.route("/Match", methods=["GET"])
@jwt_required()  # Protege la ruta con autenticación JWT
def match():
    
    return jsonify({"message": "Bienvenido a la ruta privada Match"})  

@app.route("/Chat", methods=["GET"])
@jwt_required()  # Protege la ruta con autenticación JWT
def chat():
    
    return jsonify({"message": "Bienvenido a la ruta privada Chat"})

@app.route("/Calendar", methods=["GET"])
@jwt_required()  # Protege la ruta con autenticación JWT
def calendar():
    
    return jsonify({"message": "Bienvenido a la ruta privada Eventos"})

@app.route("/genero/<int:user_id>", methods=["GET"])
def get_generos_by_user_id(user_id):
    generos = Genero.query.filter_by(user_id=user_id).all()

    generos_data = [
        {
            "id": genero.id,
            "user_id": genero.user_id,
            "genero": genero.genero,
        }
        for genero in generos
    ]

    return jsonify(generos_data)

@app.route("/genero/<int:user_id>/<int:genero_id>", methods=["DELETE"])
def delete_genero(user_id, genero_id):
    genero = Genero.query.filter_by(user_id=user_id, id=genero_id).first()

    if not genero:
        return jsonify({"error": "Género no encontrado"}), 404

    db.session.delete(genero)
    db.session.commit()

    return jsonify({"message": "Género eliminado exitosamente"})

@app.route("/game/<int:user_id>", methods=["GET"])
def get_games_by_user_id(user_id):
    games = Game.query.filter_by(user_id=user_id).all()

    games_data = [
        {
            "id": game.id,
            "user_id": game.user_id,
            "game": game.games,
        }
        for game in games
    ]

    return jsonify(games_data)


@app.route("/game/<int:user_id>/<int:game_id>", methods=["DELETE"])
def delete_game(user_id, game_id):
    game = Game.query.filter_by(user_id=user_id, id=game_id).first()

    if not game:
        return jsonify({"error": "Juego no encontrado"}), 404

    db.session.delete(game)
    db.session.commit()

    return jsonify({"message": "Juego eliminado exitosamente"}) 

@app.route('/friend-request', methods=['POST'])
def send_friend_request():
    data = request.get_json()

    sender_id = data.get('senderId')
    receiver_id = data.get('receiverId')

    # Verifica que los campos requeridos estén presentes
    if sender_id is None or receiver_id is None:
        return jsonify({"error": "Campos senderId y receiverId requeridos"}), 400

    # Verifica si existe una solicitud de amistad recíproca
    if has_mutual_friend_request(sender_id, receiver_id):
        # Si existe una solicitud mutua, crea una entrada en la tabla Match
        create_match(sender_id, receiver_id)

    # Crea una nueva solicitud de amistad
    friend_request = FriendRequest(sender_id=sender_id, receiver_id=receiver_id, status='Aceptada')

    try:
        db.session.add(friend_request)
        db.session.commit()
        return jsonify({"message": "Solicitud de amistad creada con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear la solicitud de amistad", "details": str(e)}), 500

def has_mutual_friend_request(sender_id, receiver_id):
    # Comprueba si hay una solicitud mutua en la base de datos
    mutual_request = FriendRequest.query.filter_by(sender_id=receiver_id, receiver_id=sender_id, status='Aceptada').first()
    return mutual_request is not None

def create_match(user_id_1, user_id_2):
    # Crea una nueva entrada en la tabla Match
    match = Match(user_id_1=user_id_1, user_id_2=user_id_2)

    try:
        db.session.add(match)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    with app.app_context():
        db.drop_all()
        db.create_all()
