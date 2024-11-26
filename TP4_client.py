"""\
GLO-2000 Travail pratique 4 - Client
Noms et numéros étudiants:
-
-
-
"""

import argparse
import getpass
import json
import socket
import sys

import glosocket
import gloutils

def _input_choice(max_number : int) -> int:
        while True:
            choice: int = None
            try:
                choice: int = int(input())
            except ValueError:
                print("Invalid choice, please input a valid number")
                continue
            if choice > max_number or choice == 0:
                print("Please input a number within the permitted range")
                continue
            return choice

class Client:
    """Client pour le serveur mail @glo2000.ca."""

    def __init__(self, destination: str) -> None:
        """
        Prépare et connecte le socket du client `_socket`.

        Prépare un attribut `_username` pour stocker le nom d'utilisateur
        courant. Laissé vide quand l'utilisateur n'est pas connecté.
        """
        self._username = ""

    def _send_message_to_server(message : gloutils.GloMessage) -> gloutils.GloMessage:
        return gloutils.GloMessage

    def _register(self) -> None:
        """
        Demande un nom d'utilisateur et un mot de passe et les transmet au
        serveur avec l'entête `AUTH_REGISTER`.

        Si la création du compte s'est effectuée avec succès, l'attribut
        `_username` est mis à jour, sinon l'erreur est affichée.
        """
        print("Entrez un nom d'utilisateur : ")
        username:str = input()
        password:str = getpass.getpass("Entrez votre mot de passe :") 
        message = gloutils.GloMessage(
            header=gloutils.Headers.AUTH_REGISTER,
            payload=gloutils.AuthPayload(
                username=username,
                password=password
            )
        )
        server_answer:gloutils.GloMessage = self._send_message_to_server(message)
        if server_answer.header == gloutils.Headers.ERROR:
            error_payload : gloutils.ErrorPayload = server_answer.payload
            print(error_payload.error_message)
        elif server_answer.header == gloutils.Headers.OK:
            self._username = username
        else :
            raise RuntimeError("An unexpected message type was returned when handling register")


    def _login(self) -> None:
        """
        Demande un nom d'utilisateur et un mot de passe et les transmet au
        serveur avec l'entête `AUTH_LOGIN`.

        Si la connexion est effectuée avec succès, l'attribut `_username`
        est mis à jour, sinon l'erreur est affichée.
        """
        print("Entrez un nom d'utilisateur : ")
        username:str = input()
        password:str = getpass.getpass("Entrez votre mot de passe :") 
        
        login_message = gloutils.GloMessage(
            header=gloutils.Headers.AUTH_LOGIN,
            payload=gloutils.AuthPayload(
                username=username,
                password=password
            )
        )
        server_answer : gloutils.GloMessage = self._send_message_to_server(login_message)
        if server_answer.header == gloutils.Headers.ERROR:
            error_payload : gloutils.ErrorPayload = server_answer.payload
            print(error_payload.error_message)
        elif server_answer.header == gloutils.Headers.OK:
            self._username = username
        else :
            raise RuntimeError("An unexpected message type was returned when handling login")

    def _quit(self) -> None:
        """
        Préviens le serveur de la déconnexion avec l'entête `BYE` et ferme le
        socket du client.
        """
        quit_message = gloutils.GloMessage(
            header = gloutils.Headers.BYE
        )
        response : gloutils.GloMessage = self._send_message_to_server(quit_message)
        if response.header == gloutils.Headers.OK:
            print("Quit")
            sys.exit(1)
        else:
            raise RuntimeError("Failure to quit " + response.header)

    def _read_email(self) -> None:
        """
        Demande au serveur la liste de ses courriels avec l'entête
        `INBOX_READING_REQUEST`.

        Affiche la liste des courriels puis transmet le choix de l'utilisateur
        avec l'entête `INBOX_READING_CHOICE`.

        Affiche le courriel à l'aide du gabarit `EMAIL_DISPLAY`.

        S'il n'y a pas de courriel à lire, l'utilisateur est averti avant de
        retourner au menu principal.
        """

    def _send_email(self) -> None:
        """
        Demande à l'utilisateur respectivement:
        - l'adresse email du destinataire,
        - le sujet du message,
        - le corps du message.

        La saisie du corps se termine par un point seul sur une ligne.

        Transmet ces informations avec l'entête `EMAIL_SENDING`.
        """

    def _check_stats(self) -> None:
        """
        Demande les statistiques au serveur avec l'entête `STATS_REQUEST`.

        Affiche les statistiques à l'aide du gabarit `STATS_DISPLAY`.
        """

    def _logout(self) -> None:
        """
        Préviens le serveur avec l'entête `AUTH_LOGOUT`.

        Met à jour l'attribut `_username`.
        """
        logout_message = gloutils.GloMessage(
            header = gloutils.Headers.AUTH_LOGOUT
        )
        response : gloutils.GloMessage = self._send_message_to_server(logout_message)
        if response.header == gloutils.Headers.OK:
            print("Logged out")
            self._username = ""
        else:
            raise RuntimeError("Failure to logout" + response.header)

    def _menu_authentification(self):
        """"
        Ouvre le menu textuel permettant d'obtenir l'authentification de l'utilisateur
        """
        print(gloutils.CLIENT_AUTH_CHOICE)
        choice : int = _input_choice(3)
        match choice:
            case 1:
                self._register()
            case 2:
                self._login()
            case 3:
                sys.exit(0)

    def _main_menu(self) -> None:
        """"
        Ouvre le menu principal
        """
        print(gloutils.CLIENT_USE_CHOICE)
        choice : int = _input_choice(4)
        match choice:
            case 1:
                self._read_email()
            case 2:
                self._send_email()
            case 3:
                self._check_stats()
            case 4:
                self._logout()

    def run(self) -> None:
        """Point d'entrée du client."""
        should_quit = False

        while not should_quit:
            if not self._username:
                self._menu_authentification()
            else:
                self._main_menu()
                pass

def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destination", action="store",
                        dest="dest", required=True,
                        help="Adresse IP/URL du serveur.")
    args = parser.parse_args(sys.argv[1:])
    client = Client(args.dest)
    client.run()
    return 0


if __name__ == '__main__':
    sys.exit(_main())

