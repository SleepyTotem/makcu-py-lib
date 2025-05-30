# makcu/__main__.py

import sys
import subprocess
import webbrowser
import os
from makcu import create_controller, MakcuConnectionError

def debug_console():
    controller = create_controller()
    transport = controller.transport

    print("🔧 Makcu Debug Console")
    print("Type a raw command (e.g., km.version()) and press Enter.")
    print("Type 'exit' or 'quit' to leave.")

    while True:
        try:
            cmd = input(">>> ").strip()
            if cmd.lower() in {"exit", "quit"}:
                break
            if not cmd:
                continue

            response = transport.send_command(cmd, expect_response=True)
            print(f"{response or '(no response)'}")

        except Exception as e:
            print(f"⚠️ Error: {e}")

    controller.disconnect()
    print("Disconnected.")

def test_port(port):
    try:
        print(f"Trying to connect to {port} (without init command)...")
        controller = create_controller(port=port, send_init=False)
        print(f"✅ Successfully connected to {port}")
        controller.disconnect()
    except MakcuConnectionError as e:
        print(f"❌ Failed to connect to {port}: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def run_tests():
    print("🧪 Running Pytest Suite...")
    subprocess.run([
        sys.executable, "-m", "pytest",
        "--html=latest_pytest.html", "--self-contained-html"
    ])

    report_path = os.path.abspath("latest_pytest.html")
    print(f"📄 Opening test report: {report_path}")
    webbrowser.open(f"file://{report_path}")

def main():
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  python -m makcu --debug")
        print("  python -m makcu --testPort COM3")
        print("  python -m makcu --runtest")
        return

    if args[0] == "--debug":
        debug_console()
    elif args[0] == "--testPort" and len(args) == 2:
        test_port(args[1])
    elif args[0] == "--runtest":
        run_tests()
    else:
        print(f"Unknown command: {' '.join(args)}")
        print("Usage:")
        print("  python -m makcu --debug")
        print("  python -m makcu --testPort COM3")
        print("  python -m makcu --runtest")

if __name__ == "__main__":
    main()