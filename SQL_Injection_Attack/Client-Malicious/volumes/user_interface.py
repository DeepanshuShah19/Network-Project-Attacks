import requests

userid = input("Enter userid:  ")
password = input("Enter password:  ")
response_malicious =  requests.get("http://10.10.0.6:5000/login",headers={'Content-Type': 'application/json' }, json={'userid' : userid, 'password' : password})


print("Output from malicious server")
print("####################################################################")
if len(response_malicious.json()) != 0:
    for user_detail in response_malicious.json():
        for key, value in user_detail.items():
            print(f"{ key }:  { value }")
        print()
else:
    print("Please enter correct username/password")
