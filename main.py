from bank import BANKING


# Main entry point
if __name__ == "__main__":
    try:
        app = BANKING()
        app.run()
    except Exception as e:
        print(f"Application failed to start: {e}")
        input("Press Enter to exit...")