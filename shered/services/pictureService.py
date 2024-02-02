from PIL import Image
import io

class PictureService:

    def picture_to_bytes_path(self, path_to_file):
        try:
            with open(path_to_file, 'rb') as image_file:
                image_bytes = image_file.read()
            return image_bytes
        except FileNotFoundError:
            print(f"File not found: {path_to_file}")
            return None

    def bytes_to_picture(self, bytes_picture):
        try:
            image = Image.open(io.BytesIO(bytes_picture))
            return image
        except Exception as e:
            print(f"Error converting bytes to image: {e}")
            return None

    def picture_to_bytes1 (self, image_object):
        try:
            if image_object.mode != 'RGB':
                image_object = image_object.convert('RGB')

            image_bytes = image_object.tobytes()
            image_with_header = self.add_header(image_bytes, image_object.width, image_object.height, image_object.mode)

            return image_with_header
        except Exception as e:
            print(f"Error converting image to bytes: {e}")
            return None

    def bytes_to_picture1 (self, bytes_picture):
        try:
            # Pobierz rozmiar obrazu
            width, height, mode,  image_bytes = self.remove_header(bytes_picture)

            # Utwórz obraz z ciągu bajtów
            image = Image.frombytes(mode=mode, size=(width, height), data=bytes_picture)

            return image
        except Exception as e:
            print(f"Error converting bytes to image: {e}")
            return None

    def add_header(self, image_bytes, width, height, mode):
        # Konwertuj szerokość i wysokość na bajty
        width_bytes = width.to_bytes(4, byteorder='big')  # Przyjmuję, że szerokość mieści się w 4 bajtach
        height_bytes = height.to_bytes(4, byteorder='big')  # Przyjmuję, że wysokość mieści się w 4 bajtach

        # Koduj tryb kolorów do bajtów
        mode_bytes = mode.encode('utf-8')

        # Utwórz nagłówek
        header = width_bytes + height_bytes + mode_bytes

        # Dołącz nagłówek do danych obrazu
        image_with_header = header + image_bytes

        return image_with_header

    def remove_header(self, image_with_header):
        # Pobierz szerokość i wysokość z nagłówka
        width = int.from_bytes(image_with_header[:4], byteorder='big')
        height = int.from_bytes(image_with_header[4:8], byteorder='big')

        # Odczytaj tryb kolorów z nagłówka
        mode = image_with_header[8:11].decode('utf-8')

        # Odetnij nagłówek, aby uzyskać same dane obrazu
        image_bytes = image_with_header[11:]

        return width, height, mode, image_bytes