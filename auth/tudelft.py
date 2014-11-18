from social.backends import oauth


class OAuth2Backend(oauth.BaseOAuth2):
    name = 'tudelft'

    AUTHORIZATION_URL = 'https://oauth.tudelft.nl/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://oauth.tudelft.nl/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE = 'cijfers'

    #def get_json(self, url, *args, **kwargs):
    #    response = self.request(url, *args, **kwargs)
    #    text = response.text
    #    assert text
    #    return response.json()

    def get_user_details(self, response):
        return {}
        #data = response['studievoortgang'][0]
        #return {'username': data['studentnummer']}

    #def user_data(self, access_token, *args, **kwargs):
    #    url = 'https://api.tudelft.nl/v0/studievoortgang'
    #    data = self.get_json(url, params={'oauth_token': access_token})
    #    return data['getStudievoortgangByStudentnummerResponse']

    #def get_user_id(self, details, response):
    #    data = response['studievoortgang'][0]
    #    return data['studentnummer']

