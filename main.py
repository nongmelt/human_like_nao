import argparse
from game import QuizGame

def main():
    parser = argparse.ArgumentParser(description="Run the Quiz Game in different modes.")
    parser.add_argument("--mode", choices=["robot", "human"], required=True, help="Select the mode: 'robot' or 'human'")

    args = parser.parse_args()
    game = QuizGame(mode=args.mode)
    game.quiz_loop()

if __name__ == "__main__":
    main()
