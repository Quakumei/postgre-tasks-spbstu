import typing as tp
import yaml  
from yaml.loader import SafeLoader

import streamlit as st
import streamlit_authenticator as stauth 

DEFAULT_CONFIG_FILE = 'config.yaml'

def init_authenticator_from_yaml(yaml_config: str = DEFAULT_CONFIG_FILE) -> stauth.Authenticate:
    """ Init Streamlit authenticator from yaml config file """

    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    return authenticator

def login_if_not_authorized(display_login: tp.Literal['main', 'sidebar'] = 'main') -> bool: 
    """ Tries to authorize user if not authorized.
    Returns whether authorization was successful.
    """ 
    authenticator = init_authenticator_from_yaml() 
    name, authentication_status, username = authenticator.login('Login', display_login)
    if authentication_status == True: 
        authenticator.logout('Logout', 'main')
        st.write(f'Authorized as *{name}*')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
    return authentication_status if authentication_status is not None else False
    