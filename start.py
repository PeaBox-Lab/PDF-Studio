import threading, time, webbrowser
import uvicorn

def browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    threading.Thread(target=browser, daemon=True).start()
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info")
