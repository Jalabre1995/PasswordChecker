import requests
import hashlib
import sys

 #API key for pwnedpasswords.com. The api is working when it runs a 200 in the command line, but if not then raise a runtimeError
def request_api_data(query_char): 
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res
#Create a function where we keep count of how many times the password has been leaked.
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes: 
        if h == hash_to_check:
            return count

def read_res(response):
    print(response.text)

#using hashlib module to make sure password is hash from the last 5 character to the first 5 characters. 
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print(response)
    return get_password_leaks_count(response, tail)
#import sys to run the arguments above in a for loop and check the passwords and count. This will return an response if the count was successful or it needs to be changed.
def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times.... you should change it')
        else:
            print(f'{password} was not found. Great Security')
        return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))