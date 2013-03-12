import musicbrainzngs

oauth = musicbrainzngs.MbOAuth2('-7T_7RKflTl0jCisNjNISA', 'GsjBImiDfPHhTL6ypQHE-Q', 'urn:ietf:wg:oauth:2.0:oob')

# url = oauth.auth_request('rating')
# print url

# token, expires, ref = oauth.access_token('cwZv-EXBkJb_z3wEcvw6QA')
# print token, expires, ref

token, expires, ref = oauth.refresh_token('uF6hvK4HZq6nlAs6_CbgcQ')
print token, expires, ref