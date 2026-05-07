import requests

def test_command(text):
    print(f"TESTING: '{text}'")
    try:
        res = requests.post("http://127.0.0.1:5000/chat", json={"message": text})
        print(f"RESPONSE: {res.json()}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_command("what time is it?")
    test_command("open calculator")
    test_command("system status")
