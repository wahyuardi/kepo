# kepo
Key Production

## How to use
1. install python 3 and add to path
2. download chromedriver, unzip it and put into /usr/bin or c:windows\system32
3. for mac user rename kepo.cpython-37m-darwin.so to kepo.so
4. for linux user rename kepo.cpython-37m-x64.so to kepo.so
5. for windows user rename kepo.cpython-37m-x64.pyd to kepo.pyd
6. run this command

```sh
pip install -r requirements.txt
python main.py
```

## For Admin
1. Rename kepo\_dev.py into kepo.py
2. Please ask for key, iv and client\_secret and set into kepo.py
3. Make sure you have install cython and gcc or visual studio
4. run compile.command or compile.bat
5. push your compile result to repo