from rich.console import Console

from controllers.player import PlayerController
from data_managers import PlayerManager
from managers.tournament import TournamentManager
from models import Player
from views import PlayerView, main_menu

console = Console()


class MenuManager:
    @staticmethod
    def menu_controller():

        while True:
            choice = main_menu()

            if choice == "1":

                while True:
                    user_input = PlayerView.player_menu()

                    if user_input == "1":
                        player_data = PlayerView.prompt_new_player()
                        player = Player(
                            id=player_data["id"],
                            lastname=player_data["lastname"],
                            firstname=player_data["firstname"],
                            birthday=player_data["birthday"],
                        )

                        # Valider puis sauvegarder
                        if PlayerController.validate_player(player):

                            try:
                                PlayerManager.save(player)
                                console.print(
                                    "[green]✓ Joueur créé/mis à jour "
                                    + "avec succès ![/green]"
                                )

                            except Exception as e:
                                console.print(
                                    "[red]✗ Échec de la sauvegarde "
                                    + f"du joueur : {e}[/red]"
                                )

                        else:
                            console.print(
                                "[red]✗ Validation du joueur "
                                + "échouée.[/red]"
                            )

                    elif user_input == "2":
                        players = PlayerManager.find_all()
                        PlayerView.display_players(players)
                    elif user_input == "3":
                        player_id = PlayerView.prompt_delete_player()
                        player = PlayerManager.find_by_id(player_id)
                        if player:
                            PlayerManager.delete(player_id)
                            console.print(
                                "[green]✓ Joueur supprimé avec "
                                + "succès ![/green]"
                            )
                        else:
                            console.print(
                                "[red]✗ Aucun joueur trouvé avec "
                                + "cet ID.[/red]"
                            )
                    elif user_input == "0":
                        break

            elif choice == "2":
                TournamentManager.run()

            elif choice == "0":
                console.print(
                    "\n[bold cyan]👋 Au revoir ! Merci d'avoir utilisé "
                    "OC Chess Tournaments.[/bold cyan]\n"
                )
                break

            else:
                console.print(
                    "[yellow]⚠ Choix invalide. " "Veuillez réessayer.[/yellow]"
                )
