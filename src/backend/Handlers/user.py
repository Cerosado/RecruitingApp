from flask import jsonify
from src.backend.DAO.userDAO import UserDao



class UserHandler:

    def map_to_User(self, row):
        user = {}
        user['username'] = row[0]
        user['password'] = row[1]
        user['first_name'] = row[2]
        user['last_name'] = row[3]
        user['email'] = row[4]
        user['is_recruiter'] = row[5]
        return user

    def createAccount(self, data):
        if len(data) != 6:
            return jsonify(Error="Missing Information")
        username = data["username"]
        password = data["password"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        is_recruiter = data["is_recruiter"]
        dao = UserDao()
        uid = dao.registerUser(username, password, first_name, last_name, email, is_recruiter)
        return jsonify(CreatedUser=uid)

    def login(self, data):
        result = {
            'email': data['email'],
            'password': data['password'],
        }
        return jsonify(result)

    def getUsersById(self, uid):
        dao = UserDao()
        result = dao.getUserById(uid)
        result = self.map_to_User(result)
        return jsonify(result)

    def getUserByUsername(self, username):
        dao = UserDao()
        result = dao.getUserByUsername(username)
        result = self.map_to_User(result)
        return jsonify(result)

    def getUserByName(self, name):
        dao = UserDao()
        result = dao.GetUserByFirstName(name)
        result = self.map_to_User(result)
        return jsonify(result)

    def getUserByLastName(self, lastName):
        dao = UserDao()
        result = dao.getUserByLastName(lastName)
        result = self.map_to_User(result)
        return jsonify(result)

    def getUserByUsername(self, email):
        dao = UserDao()
        result = dao.getuserByEmail(email)
        result = self.map_to_User(result)
        return jsonify(result)

    def editUser(self, data, user_id):
        dao = UserDao()
        original = dao.getUserById(user_id)
        for item in original:
            if (data.get(item)==None):
                data[item]=original[item]
        result = dao.editUser(data['username'], data['password'], data['first_name'], data['last_name'], data['email'],
                                data['is_recruiter'], data['user_id'])
        return jsonify(Result=result)

    def getAllUsers(self):
        result = []
        dao = UserDao()
        result = dao.getAllAccounts()
        mapped_result = []
        for r in result:
            mapped_result.append(self.map_to_User(r))
        return jsonify(mapped_result)

    def getAllRecruiters(self):
        result = []
        dao = UserDao()
        result = dao.getAllRecruiters()
        mapped_result = []
        for r in result:
            mapped_result.append(self.map_to_User(r))
        return jsonify(mapped_result)

    def getAllApplicants(self):
        result = []
        dao = UserDao()
        result = dao.getAllApplicants()
        mapped_result = []
        for r in result:
            mapped_result.append(self.map_to_User(r))
        return jsonify(mapped_result)
