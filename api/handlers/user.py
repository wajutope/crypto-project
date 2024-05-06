from tornado.web import authenticated
from api.enc_utility import decrypt_data

from .auth import AuthHandler

class UserHandler(AuthHandler):

    @authenticated
    def get(self):
        self.set_status(200)
        self.response['email'] = decrypt_data(self.current_user['email'])
        self.response['displayName'] = decrypt_data(self.current_user['display_name'])
        self.response['dob'] = decrypt_data(self.current_user['dob'])
        self.response['phone'] = decrypt_data(self.current_user['phone'])
        self.response['handicap_level'] = decrypt_data(self.current_user['handicap_level'])       
        self.write_json()
