from hooshix.api.light_server import agent


def run_ui():
    print("\n🚀 Hooshix UI Test Mode")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bye 👋")
            break

        try:
            result = agent.process_input(
                user_id="ui_user",
                message=user_input
            )

            print("\n🤖 Hooshix:")
            print(result["response"])
            print("-" * 40)

        except Exception as e:
            print("❌ Error:", str(e))


if __name__ == "__main__":
    run_ui()
