import configparser
import argparse
import os
from plexapi.server import PlexServer



def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

# List all Users
def list_users(plex):
    for user in plex.myPlexAccount().users():
        print("Usuario:", user.title,"\n""E-Mail: ", user.email, "\n")

# List all Libraries
def list_libraries(plex):
    for library in plex.library.sections():
        print(library.title)
        
# Block ou Resotre User's Access
def manage_access(plex, user, sections, action):
   if action == 'block':
    plex.myPlexAccount().updateFriend(user=user, server=plex, sections=['ACESSO BLOQUEADO'])
   elif action == 'restore':
    plex.myPlexAccount().updateFriend(user=user, server=plex, sections=sections)

def list_user_libraries(user, myplexuser):
    print('TO-DO')
    

def main():
    config = get_config()['PLEX']
    token = config['TOKEN']
    url = config['URL']
    plex = PlexServer(url, token)
    sections = ['Filmes', 'Animes', 'Desenhos Animados', 'Documentários', 'Filmes Animações', 'Novelas', 'Realities e TV Shows', 'Séries', 'Shows', 'Tokusatsus']

#Set args to use in cmdline
    parser = argparse.ArgumentParser()
    parser.add_argument('--list-users', action='store_true', help="List all users and email from Server")
    parser.add_argument('--list-libraries', action='store_true', help="List all Libraries from the Server")
    parser.add_argument('--libraries', action='store_true')
    parser.add_argument('--block', action='store_true', help='Block access for the specified use')
    parser.add_argument('--restore', action='store_true', help='Restore access for the specified use')
    parser.add_argument('--user', nargs='+', help='The users to modify')
    args = parser.parse_args()

    if args.list_users:    
        list_users(plex)

    if args.list_libraries:
        list_libraries(plex)

    if args.user:
        for user in args.user:
            if args.block:
                manage_access(user=user, plex=plex, sections=sections, action='block')
                print(f"Access blocked for user {user}")
            elif args.restore:
                manage_access(user=user, plex=plex, sections=sections, action='restore')
                print(f"Access restored for user {user}")
    else:
        print("No user specified")

    if args.libraries and args.user:
        for user in args.user:
            list_user_libraries(plex, user)


if __name__ == '__main__':
    main()