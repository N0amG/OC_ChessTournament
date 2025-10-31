from controllers import PlayerController
from managers.tournament import TournamentManager
from models import Player
from views import PlayerView, main_menu


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
                        if PlayerController.create_or_update_player(player):
                            print("Player created/updated successfully.")
                        else:
                            print("Failed to create/update player.")
                    elif user_input == "2":
                        players = PlayerController.get_all_players()
                        PlayerView.display_players(players)
                    elif user_input == "0":
                        break
            elif choice == "2":
                TournamentManager.run()
            elif choice == "0":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")
