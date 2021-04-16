"""
contains main method
"""
import game_class as game
import shooting


def main():
    """
    main method that runs the game
    """
    game_stop = 0
    print("Welcome pirate!")
    print("(1)single player (2)play with a friend")
    decision = input("-->")

    if decision in ("1", "single", "single player"):
        player = game.Game(1)
        player.place_ships_one()
        player_shooting = shooting.Shooting(0, 1)
        ai_shooting = shooting.Shooting(player, 3)

        while game_stop == 0:
            player_shooting.shoot_at_ai()
            ai_shooting.shooting_ai()
            game_stop = ai_shooting.game_winner()
    elif decision in ("2", "friend", "with a friend", "play with a friend"):
        players = {"one": game.Game(1), "two": game.Game(2)}
        player_shooting = {"one": shooting.Shooting(players["two"], 1),
                           "two": shooting.Shooting(players["one"], 2)}
        players["one"].place_ships_one()
        players["two"].place_ships_two()

        while game_stop == 0:
            player_shooting["one"].shoot()
            player_shooting["two"].shoot()
            game_stop = player_shooting["two"].game_winner()


if __name__ == '__main__':
    main()
