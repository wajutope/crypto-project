from json import dumps
from logging import info
from tornado.escape import json_decode, utf8
from tornado.gen import coroutine

from api.enc_utility import encrypt_data, encrypt_password

from .base import BaseHandler

class RegistrationHandler(BaseHandler):

#This is for getting Data posted
    @coroutine
    def post(self):
        try:
            body = json_decode(self.request.body)
            email = body['email'].lower().strip()
            if not isinstance(email, str):
                raise Exception()
            password = body['password']
            if not isinstance(password, str):
                raise Exception()   
            displayName = body['displayName']
            if not isinstance(displayName, str):
                raise Exception()          
            dob = body['dob']
            if not isinstance(dob, str):
                raise Exception()      
            phone = body['phone']
            if not isinstance(phone, str):
                raise Exception()      
            handicap_level = body['handicap_level']
            if not isinstance(handicap_level, str):
                raise Exception()                     
            email = body.get('email')  
            password = body.get('password')      
            display_name = body.get('displayName')
            dob = body.get('dob')
            phone = body.get('phone')
            handicap_level = body.get('handicap_level')
            print("Data entered :", email, password, display_name, dob, phone, handicap_level)
            if not isinstance(display_name, str):
                raise Exception()
#Checking Data Requirements
        except Exception as e:
            self.send_error(400, message='You must provide an email address, password, phone number, dob and display name!')
            return

        if not email:
            self.send_error(400, message='The email address is invalid!')
            return
        if not password:
            self.send_error(400, message='The password is invalid!')
            return
        if not display_name:
            self.send_error(400, message='The display name is invalid!')
            return
        if not dob:
            self.send_error(400, message='Date of Birth not provided!')
        if not phone:
            self.send_error(400, message='Phone number not provided!')
        if not handicap_level:
            self.send_error(400, message='The handicap_level was not provided!')

#This is to verify if email address exists in the database
        user = yield self.db.users.find_one({
          'email': encrypt_data(email)
        }, {})

        if user is not None:
            self.send_error(409, message='A user with the given email address already exists!')
            return

#Adding data to database
	        yield self.db.users.insert_one({
            'email': encrypt_data(email),
            'password': encrypt_password(password),
            'displayName': encrypt_data(display_name),
            'dob': encrypt_data(dob),
            'phone': encrypt_data(phone),
            'handicap_level': encrypt_data(handicap_level)
        })

#This shows the report
        self.set_status(200)
        self.response['email'] = email
        self.response['displayName'] = display_name
        self.response['dob'] = dob
        self.response['phone'] = phone
        self.response['handicap_level'] = handicap_level
        self.response['phone'] = phone
        self.response['handicap_level'] = handicap_level
        self.write_json()
