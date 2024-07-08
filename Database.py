import sqlite3
import face_recognition
import cv2
import pickle

conn = sqlite3.connect('faces.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS KnownFaces3
             (id INTEGER PRIMARY KEY, name TEXT, username TEXT, password TEXT, encoding BLOB, rgb BLOB)''')
c.execute('''CREATE TABLE IF NOT EXISTS email1
             (id INTEGER PRIMARY KEY,  username TEXT, email TEXT)''')

def serialize_image(image):
    return pickle.dumps(image)

known_faces = [
    # ("Akhilesh", "21BCE1264", "akhi@123", r"C:\Users\Akhil\Project\known_people_folder\akhi.jpeg"),
    # ("Mithesh", "21BCE5553", "mithu@123", r"C:\Users\Akhil\Project\known_people_folder\mithu.jpg"),
    # ("Madhu", "21BCE1859", "madhu@123", r"C:\Users\Akhil\Project\known_people_folder\madhu.jpg"),
    # ("Neha", "21BCE5559", "neha@123", r"C:\Users\Akhil\Project\known_people_folder\neha.jpg"),
    # ("Nethra", "21BCE5053", "nethra@123", r"C:\Users\Akhil\Project\known_people_folder\nethra.jpg"),
    # ("Sivakumar", "21BCE1095", "sivu@123", r"C:\Users\Akhil\Project\known_people_folder\sivu1.jpg")
] #example

for name, username, password, image_path in known_faces:
    image = cv2.imread(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    c.execute("INSERT INTO KnownFaces3 (name, username, password, encoding, rgb) VALUES (?, ?, ?, ?, ?)", 
              (name, username, password, pickle.dumps(face_encoding), pickle.dumps(image_rgb)))

# for name, username, password, image_path in known_faces:
#     c.execute("INSERT INTO email1 (username,email) VALUES (?, ?)",(username,'nairtuttu@gmail.com'))

conn.commit()
conn.close()
