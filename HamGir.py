import requests
import config
import time
import pickle

API_URL = config.API_URL
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD
CHAIR_NUM = config.CHAIR_NUM
USER_ID = config.USER_ID

cookies_dict = ""
checkInitData = ""

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "TabId": "307",
    "ModuleId": "1217",
    "ModuleGuid": "24d48423-8970-4b42-a494-9584d95bea8b",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json;charset=utf-8",
    "Origin": "https://my.bagheketab.com",
    "Connection": "keep-alive",
    "Referer": "https://my.bagheketab.com/DesktopModules/BusinessEngine/Dashboard.aspx?d=u&page=sign-up-to-hamkara&m=reserve-chiar",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

s = requests.Session()

# # ------------------
# # Session Request
# # ------------------
def req(headers, jsonData, funcName):
    try:
        response = s.post(
            API_URL,
            headers=headers,
            json=jsonData,
        )
        return response
    except requests.RequestException as e:
        print(f"An error occurred: {e}\n Err in {funcName}")
        exit()
    except:
        print("An error occurred")

# # ------------------
# # Login
# # ------------------
def login(username=USERNAME, password=PASSWORD):
    loginHeader = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "TabId": "151",
        "ModuleId": "1166",
        "ModuleGuid": "6ee12ec8-0c32-47f3-93be-dc31739e56b0",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://my.bagheketab.com",
        "Connection": "keep-alive",
        "Referer": "https://my.bagheketab.com/Login?returnurl=%2FDesktopModules%2FBusinessEngine%2FDashboard.aspx%3F_t%3D307%26d%3Du%26page%3Dsign-up-to-hamkara%26m%3Dreserve-chiar",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    json_data = {
        "ServiceID": "a64667ae-7ddb-4889-9703-31172329f3d3",
        "Params": {
            "Username": username,
            "Password": password,
        },
    }
    response = req(loginHeader, json_data, "Login")

    if response.status_code == 200:
        print(
            "User ID: "
            + str(response.json()["Data"]["UserID"])
            + "\nLoggined Successfully"
        )

    return response.json()["Data"]["UserID"]

# ------------------
# Reserve Chair
# ------------------
def reserveChair(userId=USER_ID, chairNumber=CHAIR_NUM):
    json_data = {
        "ServiceID": "9125fa2a-30aa-4bb5-9d77-bea0eddcbf2b",
        "Params": {
            "UserID": userId,
            "LocationID": "1",
            "ChairNumber": chairNumber,
            "StartedByUserID": userId,
        },
    }

    response = req(headers, json_data, "Reserve Chair")

    print(response.json()["Data"]["MessageText"])
    if response.status_code == 200:
        time.sleep(1)
        return check()

# ------------------
# Check
# ------------------
def check(userId=USER_ID):
    json_data = {
        "ServiceID": "e9b31c16-ae0e-4575-998e-309aa3ae4566",
        "Params": {
            "@UserID": userId,
        },
    }

    response = req(headers, json_data, "Check")

    print(response.json()["Data"])
    return response.json()["Data"]

# ------------------
# Check Logged In
# ------------------
def checkLoggedIn():
    checkInitData = check()["HasSubscribe"]
    ##STUPID WAY
    if checkInitData == 1:
        return True

    login()
    checkInitData = check()["HasSubscribe"]

    if checkInitData == 1:
        return True
    else:
        return False

# ------------------
# end chair
# ------------------
def endChair(userId=USER_ID):
    json_data = {
        "ServiceID": "37a28852-6883-45bb-8cd6-35a594f326d5",
        "Params": {
            "EndByUserID": userId,
            "UserID": userId,
            "LocationID": "1",
        },
    }

    response = req(headers, json_data, "End Chair")

    if response.status_code == 200:
        time.sleep(1)
        return check()

# ------------------
# Save cookies to a file
# ------------------
def save_cookies():
    with open("session_data.pkl", "wb") as f:
        pickle.dump(s.cookies, f)
        print("Session data saved to session_data.pkl")

# ------------------
# Load cookies from file (before creating a session)
# ------------------
def load_cookies():
    with open("session_data.pkl", "rb") as f:
        s.cookies.update(pickle.load(f))

# ------------------
# init
# ------------------
def init():
    try:
        load_cookies()
    except:
        login()
        save_cookies()

    if checkLoggedIn():
        return
    else:
        print("Not Logged In")
        exit()

# ------------------
# Main
# ------------------
def main():
    load_cookies()

    while True:
        toDo = input(
            "1: Reserve Chair\n2: End Chair\n3: What is my user id?\n4: Exit\n"
        )

        if toDo == "1":
            reserveChair()
        elif toDo == "2":
            endChair()
        elif toDo == "3":
            print(login())
        elif toDo == "4":
            exit()
        else:
            print("Wrong Input")
            continue

# ------------------
if __name__ == "__main__":
    if USER_ID == "":
        print("FIRST initialization...")
        userID = login()
        with open("config.py", "w") as f:
            f.write(
                f"USERNAME = \"{USERNAME}\"\nPASSWORD = \"{PASSWORD}\"\nUSER_ID = {userID}\nCHAIR_NUM = {CHAIR_NUM}\nAPI_URL = \"{API_URL}\""
            )
            f.close()
        print("FIRST initialization done, please run again")
        exit()
    init()
    main()
# ------------------
