import requests

userid = input("Enter userid:  ")
password = input("Enter password:  ")

response_safe = requests.get("http://10.10.0.8:5000/login",headers={'Content-Type': 'application/json' }, json={'userid' : userid, 'password' : password})

print("Output from safe server")
print("################################################################")
if len(response_safe.json()) != 0:
    for user_detail in response_safe.json():
        for key, value in user_detail.items():
            print(f"{ key }:  { value }")
        print()
else:
    print("Please enter correct username/password")
