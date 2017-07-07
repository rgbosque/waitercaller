MOCK_USERS = [{'email': 'rgbosque@gmail.com',
               'salt': 'GmjSIKhXXDEQir57k8AY/064Paw=',
               'hashed': '3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2'
               }]


class MockDBHelper():

    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get('email') == email]
        if user:
            return user[0]
        return None

    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({'email': email,
                           'salt': salt,
                           'hashed': hashed
                           })
