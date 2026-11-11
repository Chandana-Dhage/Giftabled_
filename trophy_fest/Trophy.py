
class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []

    def collect(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
            print(f"Collected: {item}")

    def has_item(self, item):
        return item in self.inventory


class Room:
    def __init__(self, name, required_item=None):
        self.name = name
        self.required_item = required_item

    def enter(self, player):
        if self.required_item and not player.has_item(self.required_item):
            print(f"FAILED: You need {self.required_item} to enter {self.name}.")
            return False

        print(f"Entered {self.name}.")
        return True


class Puzzle:
    def __init__(self, answer):
        self.__answer = answer

    def solve(self, attempt):
        return attempt.lower() == self.__answer.lower()


class Treasure:
    def __init__(self, code):
        self.lock = Puzzle(code)
        self.opened = False

    def unlock(self, attempt):
        if self.lock.solve(attempt):
            self.opened = True
            print("WIN: Congratulations! You found the hidden treasure!")
            return True

        print("FAILED: Incorrect answer. Treasure remains locked.")
        return False


def failed_route():
    print("\n--- FAILED ROUTE ---")

    player = Player("Player")

    library = Room("Library", "ancient book")
    library.enter(player)

    treasure = Treasure("moonlight")
    treasure.unlock("sunlight")


def winning_route():
    print("\n--- WINNING ROUTE ---")

    player = Player("Player")

    entrance = Room("Entrance")
    library = Room("Library", "torch")
    secret_room = Room("Secret Room", "silver key")
    treasure_room = Room("Treasure Room", "magic scroll")

    treasure = Treasure("moonlight")

    if entrance.enter(player):
        player.collect("torch")

    if library.enter(player):
        player.collect("silver key")

    if secret_room.enter(player):
        player.collect("magic scroll")

    if treasure_room.enter(player):
        print("A mysterious treasure chest appears!")

        answer = "moonlight"
        treasure.unlock(answer)


if __name__ == "__main__":
    failed_route()
    winning_route()
