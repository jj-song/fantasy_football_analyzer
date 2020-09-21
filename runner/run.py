from runner.utilities.data_loader import load_data
from runner.extractors.high_awareness_players import get_high_awareness_49ers

def main():
    high_awareness_players = get_high_awareness_49ers()

    print("hello")

if __name__ == "__main__":
    #load_data()
    main()
