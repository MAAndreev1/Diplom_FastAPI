import bcrypt

# пример пароля
password = 'password123'

# преобразование пароля в массив байтов
bytes = password.encode('utf-8')

# генерация соли
salt = bcrypt.gensalt()

# хеширование пароля
hash = bcrypt.hashpw(bytes, salt)
print(hash, type(hash))
hash = str(hash)
print(hash, type(hash))