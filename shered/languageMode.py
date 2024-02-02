
class LanguageMode:
    mode = 'english'

    translation = {
        'english': {
            "Incorrect login or password": "Incorrect login or password",
            "Server error, try later": "Server error, try later",
            "Log into your Account": "Log into your Account",
            'Username': 'Username',
            'Password': 'Password',
            "Login": "Login",

            'Welcome in your\npostcard album': 'Welcome in your\npostcard album',
            'Save your trips with our app!!!': 'Save your trips with our app!!!',
            "My postcards": "My postcards",
            "Add postcard": "Add postcard",
            "Logout": "Logout",
            "All postcards": "All postcards",
            "Edit postcard": "Edit postcard",

            'drag & drop photo': 'drag & drop',
            "Cancel": "Cancel",
            "City: ": "City: ",
            "Country: ": "Country: ",
            "Date: ": "Date: ",
            "From whom: ": "From whom: ",
            "Photo: ": "Photo: ",
            "Add": "Add",
            'city name': 'city name',
            'country name': 'country name',
            'from whom?': 'from whom?',

            "Postcard deletes:": "Postcard deletes:",
            "Edit": "Edit",
            "Delete": "Delete",

            'You are sure\nthat you want to\ndelete the postcard': 'You are sure\nthat you want to\ndelete the postcard',

            "postcard": "postcard",
            "Apply": "Apply",

            "You are logged out.": "You are logged out.",
            "Log in again or close\nthe application": "Log in again or close\nthe application",

            'English': 'English',
            'Polish': 'Polish',
            'Language': 'Language',

            'Owner: ': 'Owner: '
        },
        'polski': {
            "Incorrect login or password": "Nieprawidłowy login lub hasło",
            "Server error, try later": "Błąd serwera, spróbuj później",
            "Log into your Account": "Zaloguj się do konta",
            'Username': 'Nazwa użytkowanika',
            'Password': 'Hasło',
            "Login": "Zaloguj",

            'Welcome in your\npostcard album': 'Witaj w swoim\nalbumie pocztówek',
            'Save your trips with our app!!!': 'Zapisz swoje podróże z naszą apką!!!',
            "My postcards": "Moje pocztówki",
            "Add postcard": "Dodaj pocztówkę",
            "Logout": "Wyloguj",
            "All postcards": "Wszystkie pocztówki",
            "Edit postcard": "Edytuj pocztówkę",

            'drag & drop photo': 'przeciągnij',
            "Cancel": "Anuluj",
            "City: ": "Miasto: ",
            "Country: ": "Kraj: ",
            "Date: ": "Data: ",
            "From whom: ": "Od kogo: ",
            "Photo: ": "Zdjęcie: ",
            "Add": "Dodaj",
            'city name': 'nazwa miasta',
            'country name': 'nazwa kraju',
            'from whom?': 'od kogo?',


            "Postcard deletes:": "Szczegóły kartki:",
            "Edit": "Edytuj",
            "Delete": "Usuń",

            'You are sure\nthat you want to\ndelete the postcard': 'Czy jesteś pewien,\nże checsz usunąć\npocztówkę',

            "postcard": "pocztówka",
            "Apply": "Zatwierdź",

            "You are logged out.": "Zostałeś wylogowany.",
            "Log in again or close\nthe application": "Zaloguj się ponownie\nalbo zamknij aplikację",

            'English': 'Angielski',
            'Polish': 'Polski',
            'Language': 'Język',

            'Owner: ': 'Właściciel: '
        }
    }

    def get_phrase(self, phrase):
        return self.translation[self.mode][phrase]
