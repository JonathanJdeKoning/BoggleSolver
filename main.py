from boggler import Boggler

if __name__ == "__main__":
    boggler = Boggler()
    for _ in range(3):
        boggler.playPuzzle(3, "hard")