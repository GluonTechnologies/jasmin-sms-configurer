from Jasmin import Jasmin
from Jasmin import JasminGroup
from Jasmin import JasminUser
from Jasmin import JasminSmppClient
from dotenv import load_dotenv

jasmin = Jasmin('jcliadmin', 'jclipwd')
jasminGroup = JasminGroup(jasmin=jasmin)
jasminGroup.add_group('ben')

jasminUser = JasminUser(jasmin=jasmin)
jasminUser.add_user('ben', 'ben', group='ben')

jasminSmpp = JasminSmppClient(jasmin=jasmin)
jasminSmpp.add_smpp(smpp_id='ben_smpp_1', username='ben', password='password', host='10.190.10.16', port=8322)
