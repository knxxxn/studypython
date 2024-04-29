import itertools
import zipfile

def un_zip(passwd_string, min_len, max_len, zfile):
    for len in range(min_len, max_len+1):
        to_attempt = itertools.product(passwd_string, repeat=len)
        for attempt in to_attempt:
            passwd=' '.join(attempt)
            print(passwd)
            try:
                zfile.extractall(pwd=passwd.encode())
                print(f"비밀번호는 {passwd}입니다")
                return 1
            except:
                pass

passwd_string="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

zfile=zipfile.ZipFile(r'압축파일 암호.zip')

min_len=1
max_len=5

unzip_result=un_zip(passwd_string, min_len, max_len, zfile)

if unzip_result==1:
    print("암호를 찾았습니다")
else:
    print("암호를 찾지 못했습니다")