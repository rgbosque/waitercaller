MOCK_USERS = [{'email': 'rgbosque@gmail.com',
               'salt': 'GmjSIKhXXDEQir57k8AY/064Paw=',
               'hashed': '75949b47c1210ed87299c235fedf5b96ba92a3c4f46f5d4a176172b1532d5c53ff4d2e275ebdda4b8c2a9837a9fda3ce8ccf83db85f067234dd77e7456479438'
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
