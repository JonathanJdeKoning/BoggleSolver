from boggler import Boggler

if __name__ == "__main__":
    boggler = Boggler()
    for _ in range(10):
        boggler.playPuzzle(5, "easy")