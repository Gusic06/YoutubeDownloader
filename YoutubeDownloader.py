import os
import sys
import time
import shutil
import logging as log
from mega import Mega
from pytube import YouTube
from cryptography.fernet import Fernet
from dependencies.divider import *
from dependencies.hashGen import hashGen
import hashlib

class InputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

def terminalClear():
    os.system("cls")

def YoutubeDownloader(): 

    originalKeyPath = ".\\encryption.key"
    targetKeyPath = ".\\key\\encryption.key"

    keyPath = ".\\key"

    if os.path.exists(keyPath):
        pass
    else:
        os.mkdir("key")

    megaCredentialCheck = ".\\megaCredentialSave.py"

    if os.path.exists(megaCredentialCheck):

        with open("megaCredentialSave.py", "r")as file:
            megaLogin = file.read()

    else:
        pass
    
    divider()

    megaQuery = input("This app can let you upload the files you download onto mega, do you want to use this feature? (Y/N) -> ").title()

    divider()

    if megaQuery == "Y" or megaQuery == "Yes":

        megaCredentialCheck1 = ".\\Created Logins\\email.json"
        megaCredentialCheck2 = ".\\Created Logins\\password.json"

        if os.path.exists(megaCredentialCheck1) and os.path.exists(megaCredentialCheck2):

            print("It seems you have a login already saved on your system")
            savedLoginQuery = input("Do you want to login on your saved account? (Y/N) -> ").title()
            try:
                if savedLoginQuery == "Yes" or savedLoginQuery == "Y":

                    with open("megaCredentialSave.py", "r")as file:
                        megaLogin = file.read()

                    if megaLogin == "True":
        
                        with open(".\\key\\encryption.key", "rb")as key:
                            key = key.read()

                        key = Fernet(key)
                
                        emailFilePath = ".\\Created Logins\\email.json"
                        passwordFilePath = ".\\Created Logins\\password.json"

                        with open(".\\Created Logins\\email.json", "rb")as file:
                            emailFile = file.read()
                
                        with open(".\\Created Logins\\password.json", "rb")as file:
                            passwordFile = file.read()

                        decryptedEmail = key.decrypt(emailFile)
                        decryptedPassword = key.decrypt(passwordFile)

                        with open(".\\Created Logins\\email.json", "wb")as file:
                            file.write(decryptedEmail)
                
                        with open(".\\Created Logins\\password.json", "wb")as file:
                            file.write(decryptedPassword)

                        with open(".\\Created Logins\\email.json", "r")as file:
                            email = file.read()
                
                        with open(".\\Created Logins\\password.json", "r")as file:
                            password = file.read()

                        mega = Mega()
                        m = mega.login(email, password)

                        divider()

                        print("Logging in...")

                        with open(".\\Created Logins\\email.json", "rb")as file:
                            emailContents = file.read()

                        with open(".\\Created Logins\\password.json", "rb")as file:
                            passwordContents = file.read()

                        reEncryptedEmail = key.encrypt(emailContents)
                        reEncryptedPassword = key.encrypt(passwordContents)

                        with open(".\\Created Logins\\email.json", "wb")as file:
                            file.write(reEncryptedEmail)
                        
                        with open(".\\Created Logins\\password.json", "wb")as file:
                            file.write(reEncryptedPassword)

                        megaConfirmation = True

                    else:
                        log.DEBUG("megaCredentialSave.py was corrupted or changed.")
                        os.remove(megaCredentialCheck1, megaCredentialCheck2)
                        terminalClear()

                if savedLoginQuery == "No" or savedLoginQuery == "N":

                    megaConfirmation = True

                    divider()

                    email = input("What is your email? (Case Sensitive) -> ")
                    password = input("What is your password? (Case Sensitive) -> ")

                    print("Logging in...")

                    mega = Mega()
                    m = mega.login(email, password)

                    print("Successfully logged in!")
                    time.sleep(1)
                    terminalClear()

            except:

                raise InputError("That wasn't a valid input.")

        else:
    
            megaConfirmation = True

            email = input("What is your email? (Case Sensitive) -> ") 
            password = input("What is your password? (Case Sensitive) -> ")

            print("Logging in...")

            mega = Mega()
            m = mega.login(email, password)

            divider()

            megaCredentialSave = input("Do you want to save your login to a file? (Y/N) -> ").title()

            if megaCredentialSave == "Y" or megaCredentialSave == "Yes":

                if os.path.exists(".\\Created Logins"):
                    x=1 #Placeholder
                else:
                    os.mkdir("Created Logins")

                if os.path.exists(".\\settings"):
                    x=1 #Placeholder
                else:
                    os.mkdir("settings")

                #hashGen(email, password)

                with open(".\\Created Logins\\email.json", "w")as file:
                    file.write(email)

                with open(".\\Created Logins\\password.json", "w")as file:
                    file.write(password)

                key = Fernet.generate_key()

                with open("encryption.key", "wb")as Key:
                    Key.write(key)

                """
                startPathEmail = ".\\email.json"
                startPathPassword = ".\\password.json"

                targetPathEmail = ".\\Created Logins\\email.json"
                targetPathPassword = ".\\Created Logins\\password.json"

                shutil.move(startPathEmail, targetPathEmail)
                shutil.move(startPathPassword, targetPathPassword)
                """

                with open("encryption.key", "rb")as file:
                    key = file.read()

                key = Fernet(key)

                with open(".\\Created Logins\\email.json", "rb")as emailRead:
                    encryptedEmail = emailRead.read()

                with open(".\\Created Logins\\password.json", "rb")as passwordRead:
                    encryptedPassword = passwordRead.read()

                encryptedEmailFile = key.encrypt(encryptedEmail)
                encryptedPasswordFile = key.encrypt(encryptedPassword)

                with open(".\\Created Logins\\email.json", "wb")as file:
                    file.write(encryptedEmailFile)

                with open(".\\Created Logins\\password.json", "wb")as file:
                    file.write(encryptedPasswordFile)

                megaCredential = "True"

                with open(".\\settings\\megaCredentialSave.py", "w")as save:
                    save.write(megaCredential)

                shutil.move(".\\encryption.key", ".\\key\\encryption.key")

                print("Successfully saved login.")
                time.sleep(1)
                terminalClear()
        
            if megaCredentialSave == "N" or megaCredentialSave == "No":

                if os.path.exists(".\\settings"):
                    x = 1
                else:
                    os.mkdir("settings")

                megaCredential = "False"

                with open(".\\settings\\megaCredentialSave.py", "w")as save:
                    save.write(megaCredential)

                time.sleep(1)
                terminalClear()

        divider()

        megaFolderQuery = input("Do you have a folder you want to download to? (Y/N) -> ").title()
        
        if megaFolderQuery == "Y" or megaFolderQuery == "Yes":

            megaFolderName = input("What is the name of the folder you want to download to? (Case Sensitive) -> ")
            
            divider()

            mFolder = m.find(megaFolderName)

            megaFolder = True

            time.sleep(1)
            terminalClear()

        elif megaFolderQuery == "N" or megaFolderQuery == "No":

            megaFolder = False

            time.sleep(1)
            terminalClear()

        else:
            print("That wasn't a correct input.")
            time.sleep(1)
            terminalClear()
        
    elif megaQuery == "N" or megaQuery == "No":
    
        megaConfirmation = False
        time.sleep(1)
        terminalClear()

    else:
        print("That wasn't a correct input.")
        time.sleep(1)
        terminalClear()

    downloadPathVideos = ".\\Downloaded Videos"
    downloadPathMusic = ".\\Downloaded Music"

    userSettingHigher = True

    if os.path.exists(downloadPathVideos) and os.path.exists(downloadPathMusic):
        x=1
    else:
        os.mkdir("Downloaded Videos")
        os.mkdir("Downloaded Music")
    
    loop = True

    while loop == True:

        topMenuDivider()
        print("""    1. Download Video                                                                                     V1.0
    2. Download Music
    3. Settings
    4. Change Mega Folder / Login to Mega Account
    5. Exit Program""")
        bottomMenuDivider()

        userChoice = int(input("""
    What mode do you want to select (1-5) -> """))

        if userChoice == 1:

            time.sleep(0.5)
            terminalClear()
    
            divider()
    
            link = input("What is the link you want to download? -> ")
    
            divider()
    
            yt = YouTube(link)
    
            print("Title:", yt.title)
            print("Views:", yt.views)
    
            divider()
    
            userConfirmation = input("Is this the correct video? (Y/N) -> ").title()
    
            if userConfirmation == "Y" or userConfirmation == "Yes":

                if userSettingHigher == True:

                    divider()
                    print("Downloading...")
                    time.sleep(0.2)
                    print("Please wait.")
                    divider()
                    videoDownload = yt.streams.get_highest_resolution()
                    videoUpload = videoDownload.download(downloadPathVideos)

                    if megaConfirmation == True and megaFolder == True:
                        m.upload(videoUpload, mFolder[0])
                        time.sleep(0.1)
                    elif megaConfirmation == True and megaFolder == False:
                        m.upload(videoUpload)
                        time.sleep(0.1)
                    else:
                        videoDownload.download(downloadPathVideos)
                    
                    print("The download is complete.")
                    divider()

                    time.sleep(1)
                    terminalClear()

                    #divider()

                elif userSettingHigher == False:
                
                    print("Downloading...")
                    time.sleep(0.2)
                    print("Please wait.")
                    videoDownload = yt.streams.get_lowest_resolution()
                    videoUpload = videoDownload.download(downloadPathVideos)

                    if megaConfirmation == True and megaFolder == True:
                        m.upload(videoUpload, mFolder[0])
                        time.sleep(0.1)
                    elif megaConfirmation == True and megaFolder == False:
                        m.upload(videoUpload)
                        time.sleep(0.1)
                            
                    print("The download is complete.")

                    time.sleep(1)
                    terminalClear()

                    #divider()
        
            if userConfirmation == "N" or userConfirmation == "No":

                #divider()
                time.sleep(1)
                terminalClear()

                continue

            continue

        if userChoice == 2:

            time.sleep(0.5)
            terminalClear()

            divider()

            link = input("What is the link you want to download? -> ")

            divider()

            yt = YouTube(link)

            print("Title:", yt.title)
            print("Views:", yt.views)

            divider()

            userConfirmation = input("Is this the correct video? (Y/N) -> ").title()

            divider()

            if userConfirmation == "Y" or userConfirmation == "Yes":
                
                musicDownload = yt.streams.get_audio_only()
                musicFile = musicDownload.download(downloadPathMusic)
                
                print("Downloading...")
                time.sleep(0.1)
                print("Please wait.")

                divider()

                
                base, ext = os.path.splitext(musicFile, )
                newMusicFile = base + ".mp3"
                os.rename(musicFile, newMusicFile)
                uploadedMusicFile = newMusicFile
                #os.remove(f".//Downloaded Music//{yt.title}.mp4")
                            
                if megaConfirmation == True and megaFolder == True and os.path.exists(f".\\Downloaded Music\\{yt.title}.mp3") == True:
                    musicFile = os.path(f".\\Downloaded Music\\{yt.title}.mp3")
                    print(yt.title)
                    m.upload(musicFile, mFolder[0])
                elif megaConfirmation == True and megaFolder == False and os.path.exists(f".\\Downloaded Music\\{yt.title}.mp3") == True:
                    musicFile = os.path(f".\\Downloaded Music\\{yt.title}.mp3")
                    print(yt.title)
                    m.upload(musicFile)

                print("The download is complete.")

                divider()
                time.sleep(1)
                terminalClear()

                continue

            if userConfirmation == "N" or userConfirmation == "No":

                terminalClear()
                continue

            terminalClear()    

        if userChoice == 3:

            settingMenuLoop = True

            while settingMenuLoop == True:

                time.sleep(0.5)
                terminalClear()

                divider()
                print("""1. Prioritize Higher Quality
2. Return to Menu""")
                divider()

                userSettingChoice = int(input("What setting do you want to select? (1-2) -> "))

                if userSettingChoice == 1:

                    terminalClear()

                    divider()
                    userSetting1 = str(input("Do you want to prioritise higher video/audio quality? (Y/N) -> ")).title()
                    

                    if userSetting1 == "Y" or userSetting1 == "Yes":
                    
                        userSettingHigher = "True"

                        with open("settings.py", "w")as settings:
                            settings.write(userSettingHigher)

                        time.sleep(0.5)
                        terminalClear()

                    if userSetting1 == "N" or userSetting1 == "No":

                        userSettingHigher = "False" 

                        with open("settings.py", "w")as settings:
                            settings.write(userSettingHigher)

                        time.sleep(0.5)
                        terminalClear()

                if userSettingChoice == 2:

                    terminalClear()
                    divider()
                    print("Returning to menu.")
                    divider()
                    settingMenuLoop = False
                    time.sleep(0.5)
                    terminalClear()

        if userChoice == 4:

            terminalClear()

            divider()
            print("""1. Login to Mega
2. Change Download Folder
3. Change Saved Login
4. Return to Menu""")
            divider()
            
            mUserChoice = int(input("What mode do you want to select? (1-4) -> "))

            megaSettingsLoop = True

            while megaSettingsLoop == True: 

                if mUserChoice == 1:

                    time.sleep(0.5)
                    terminalClear()

                    megaCredentialCheck1 = ".\\Created Logins\\email.json"
                    megaCredentialCheck2 = ".\\Created Logins\\password.json"

                    if os.path.exists(megaCredentialCheck1) and os.path.exists(megaCredentialCheck2):

                        print("It seems you have a login already saved on your system")
                        savedLoginQuery = input("Do you want to login on your saved account? (Y/N) -> ").title()
            
                        if savedLoginQuery == "Yes" or savedLoginQuery == "Y":

                            with open("megaCredentialSave.py", "r")as file:
                                megaLogin = file.read()

                        if megaLogin == "True":
        
                            with open(targetKeyPath, "rb")as key:
                                key = key.read()

                            key = Fernet(key)
                
                            emailFilePath = ".\\Created Logins\\email.json"
                            passwordFilePath = ".\\Created Logins\\password.json"

                            with open(emailFilePath, "rb")as file:
                                emailFile = file.read()
                
                            with open(passwordFilePath, "rb")as file:
                                passwordFile = file.read()

                            decryptedEmail = key.decrypt(emailFile)
                            decryptedPassword = key.decrypt(passwordFile)

                            with open(emailFilePath, "wb")as file:
                                file.write(decryptedEmail)
                
                            with open(passwordFilePath, "wb")as file:
                                file.write(decryptedPassword)

                            with open(emailFilePath, "r")as file:
                                email = file.read()
                
                            with open(passwordFilePath, "r")as file:
                                password = file.read()

                            print("Logging in...")

                            mega = Mega()
                            m = mega.login(email, password)

                            with open(emailFilePath, "rb")as file:
                                emailContents = file.read()

                            with open(passwordFilePath, "rb")as file:
                                passwordContents = file.read()

                            reEncryptedEmail = key.encrypt(emailContents)
                            reEncryptedPassword = key.encrypt(passwordContents)

                            with open(emailFilePath, "wb")as file:
                                file.write(reEncryptedEmail)
                        
                            with open(passwordFilePath, "wb")as file:
                                file.write(reEncryptedPassword)

                            megaConfirmation = True

                        else:
                            os.remove(megaCredentialCheck1, megaCredentialCheck2)
                            terminalClear()
                            raise Exception("megaCredentialSave.py was corrupted or changed.")
                    else:

                        divider()

                        email = input("What is your email? (Case Sensitive) -> ")
                        password = input("What is your password? (Case Sensitive) -> ")
                        print("Logging in...")

                        divider()

                        mega = Mega()
                        m = mega.login(email, password)

                        print("Successfully logged in!")

                        time.sleep(1)
                        terminalClear()

                        megaConfirmation = True

                        continue

                if mUserChoice == 2:

                    time.sleep(0.5)
                    terminalClear()

                    divider()
                    megaFolderChange = input("What is the name of the folder you want to download to? (Case Sensitive) -> ")
                    divider()
                    try:
                        mFolder = m.find(megaFolderChange)

                        if mFolder == True:
                            megaFolder = True

                        if mFolder == False:
                            megaFolder = False

                    except:
                        raise Exception("An error has occured.")

                    time.sleep(1)
                    terminalClear()

                if mUserChoice == 3:

                    loop = True

                    while loop == True:

                        time.sleep(0.5)
                        terminalClear()

                        divider()

                        savedEmailChange = input("Do you want to change your email or keep it the same? (Change/Keep) -> ").title()

                        if savedEmailChange == "Change":

                            emailChange = input("What is the email you want to change to? -> ")
                            emailChange = emailChange.encode("utf-8")

                            with open(targetKeyPath, "rb")as file:
                                key = file.read()

                            Key = Fernet(key)

                            emailChangeEncrypted = Key.encrypt(emailChange)


                            with open(".\\Created Logins\\email.json", "wb")as file:
                                file.write(emailChangeEncrypted)

                            divider()

                            print("Your email has been successfully changed.")

                        elif savedEmailChange == "Keep":

                            divider()

                            print("Your email has been kept the same.")

                        divider()

                        savedPasswordChange = input("Do you want to change your password or keep it the same? (Change/Keep) -> ").title()

                        if savedPasswordChange == "Change":

                            with open(targetKeyPath, "rb")as file:
                                key = file.read()

                            Key = Fernet(key)
                    
                            passwordChange = input("What do you want to change your password to? (Case Sensitive) -> ")
                            passwordChange = passwordChange.encode("utf-8")

                            passwordChangeEncrypted = Key.encrypt(passwordChange)

                            with open(".\\Created Logins\\password.json", "wb")as file:
                                file.write(passwordChangeEncrypted)

                            print("Your password has been successfully changed.")

                            time.sleep(1)
                            loop = False
                            terminalClear()
                            

                        elif savedPasswordChange == "Keep":

                            print("Your password has been kept the same.")

                            time.sleep(1)
                            terminalClear()
                        

                if mUserChoice == 4:
                    print("Returning to menu.")
                    megaSettingsLoop = False
                    time.sleep(0.5)
                    terminalClear()
                    

        if userChoice == 5:
            time.sleep(0.8)
            terminalClear()
            divider()
            print("Thank you for using my program.")
            divider()
            time.sleep(0.2)
            sys.exit()

if __name__ == "__main__":
    YoutubeDownloader()