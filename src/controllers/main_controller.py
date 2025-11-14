from controllers.player import PlayerController
from controllers.tournament import TournamentController
from views import MainView
from views.logger_view import LoggerView


class MainController:
    """Point d'entrée principal l'application."""

    def __init__(self) -> None:
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()

    def run(self) -> None:
        """Boucle principale du programme."""

        while True:
            choice = MainView.main_menu()

            if choice == "1":
                self.player_controller.manage_players()
            elif choice == "2":
                self.tournament_controller.manage_tournaments()
            elif choice == "0":
                MainView.display_goodbye()
                break
            else:
                LoggerView.warning("Choix invalide. Veuillez réessayer.")
