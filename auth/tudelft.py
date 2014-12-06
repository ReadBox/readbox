from social.backends import oauth


class OAuth2Backend(oauth.BaseOAuth2):
    name = 'tudelft'

    AUTHORIZATION_URL = 'https://oauth.tudelft.nl/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://oauth.tudelft.nl/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE = 'cijfers'

    def get_user_details(self, response):
        return {}

    def get_user_id(self, details, response):
        return {'username': 'TU Delft random user: ' +
                response['access_token']}

