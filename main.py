from ai.engine import generate_response, parse_action
from ai.actions import create_folder, create_file
from ai.memory import save_memory

print("Local AI Started (type 'exit' to quit)")

while True:
    try:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Shutting down AI...")
            break

        # Generate AI response
        response = generate_response(user_input)

        # If AI itself failed
        if response.startswith("[ERROR]"):
            print(response)
            continue

        # Check for actions
        action = parse_action(response)

        if action:
            if action[0] == "create_folder":
                result = create_folder(action[1])
                print(f"[SYSTEM]: {result}")

            elif action[0] == "create_file":
                result = create_file(action[1], action[2])
                print(f"[SYSTEM]: {result}")

        else:
            print(f"AI: {response}")

        # Save memory safely
        save_memory(f"User: {user_input}")
        save_memory(f"AI: {response}")

    except KeyboardInterrupt:
        print("\n[EXIT] Interrupted by user")
        break

    except Exception as e:
        print(f"[CRITICAL ERROR]: {str(e)}")