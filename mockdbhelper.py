MOCK_USERS = [{'email': 'rgbosque@gmail.com',
               'salt': 'GmjSIKhXXDEQir57k8AY/064Paw=',
               'hashed': '3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2'
               }]

MOCK_TABLES = [{"_id": "1", "number": "1", "owner": "test@example.com", "url": "mockurl"}]


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

    def add_table(self, number, owner):
        MOCK_TABLES.append({"_id": number, "number": number, "owner": owner})
        return number

    def update_table(self, _id, url):
        for table in MOCK_TABLES:
            if table in MOCK_TABLES:
                if table.get("_id") == _id:
                    table["url"] = url
                    break

    def get_table(self, owner_id):
        return MOCK_TABLES

    def delete_table(self, table_id):
        for i, table in enumerate(MOCK_TABLES):
            if table.get("_id") == table_id:
                del MOCK_TABLES[i]
                break
