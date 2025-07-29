from .database import SessionLocal
from .models import User
from .utils import hash_password, verify_password, create_access_token, get_user_id_from_token

def resolve_me(_, info):
     request = info.context
     auth = request.headers.get("Authorization")

     if not auth or not auth.startswith("Bearer "):
          raise Exception("Authorization header missing or invalid")
     token = auth.split(" ")[1]
     user_id = get_user_id_from_token(token)
     
     if not user_id:
          raise Exception("Invalid token")
     db= SessionLocal()
     user = db.query(User).filter(User.id == user_id).first()
     db.close()

     if not user:
        raise Exception("User not found")
     return {
          "id": user.id,
          "name": user.name,
          "email": user.email
     }

def resolve_users(_,info):
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        } for user in users
    ]
 # resolver for new user
def resolve_login_user(_, info, email, password):
     db = SessionLocal()
     user = db.query(User).filter(User.email == email).first()
     db.close()

     if not user:
          raise Exception("User not found")
     if not verify_password(password, user.password):
          raise Exception("Incorrect password")
     
     token = create_access_token(user_id=user.id)
     return token

def resolve_create_user(_, info, name, email, password):
     db = SessionLocal()

     existing_user = db.query(User).filter(User.email == email).first()
     if existing_user:
          raise Exception("User with this email already exists")
     
     hashed_pw = hash_password(password)
     new_user = User(name=name, email=email, password=hashed_pw)
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     db.close()

     return {
         "id": new_user.id,
         "name": new_user.name,
         "email": new_user.email
     }



def resolve_update_user(_, info, id, name=None, email=None):
     print("updateUser working, id:", id, type(id)) # Debugging line
     db = SessionLocal()
     user = db.query(User).filter(User.id == int(id)).first()

     if not user:
          db.close()
          return None
     
     if name:
          user.name = name

     if email:
           user.email = email

     db.commit()
     db.refresh(user)
     db.close()

     return {
          "id": user.id,
          "name": user.name,
          "email": user.email
     }

def resolve_delete_user(_, info, id):
     print("deleteUser working, id:", id, type(id))  # Debugging line
     db = SessionLocal()
     user = db.query(User).filter(User.id == int(id)).first()

     if not user:
          db.close()
          raise Exception("User not found")

     db.delete(user)
     db.commit()
     db.close()

     return True

def resolve_get_user_by_email(_, info, email):
     db = SessionLocal()
     user = db.query(User).filter(User.email == email).first()
     db.close()

     if not user:
          return None
     
     return {
          "id": user.id,
          "name": user.name,
          "email": user.email
     }