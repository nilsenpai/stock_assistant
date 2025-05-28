# orchestrator.py

import voice_agent

def main():
    print("Starting Voice Assistant Orchestrator...")
    try:
        voice_agent.main()
    except KeyboardInterrupt:
        print("\nOrchestrator stopped by user.")
    except Exception as e:
        print(f"Error in orchestrator: {e}")

if __name__ == "__main__":
    main()


