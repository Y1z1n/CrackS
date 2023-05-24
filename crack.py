try:
    from bs4 import BeautifulSoup as bs
    from colorama import Fore, Back, Style, init
    import requests
    import json
    init()
except ModuleNotFoundError:
    from os import system
    system("pip install beautifulsoup4")
    system("pip install colorama")
    system("pip install requests")
    print("[!] - An exception occured please restart the program\n[!] - make sure \"crack.py\" is in the same directory  ")

class Crack:
    def __init__(self, gameName):
        self.parser = "html.parser"
        self.gname = gameName
        self.result_list = []

    def steamcrackedgames(self):
        soup = bs(requests.get(
            f"https://steamcrackedgames.com/search/?q={self.gname}").text, self.parser)
        result = soup.find_all("a", class_="text-white")
        soup2 = bs(str(soup.find_all("tr"))[1:-1], self.parser)
        all_children2 = soup2.find_all("span")
        for index, val in enumerate(result):
            # print(i.attrs['href'], type(i))
            if str(val.attrs['href']).rfind("/games/") != -1:
                self.result_list.append(
                    [val.attrs['title'], all_children2[index].text])
        self.makeFile("steamcrackedgames.com") 
        self.Notify("steamcrackedgames.com")
        self.result_list = []

    def fitgirl_repacks(self):
        soup = bs(requests.get(
            f"https://fitgirl-repacks.site/?s={self.gname}").text, self.parser)
        soup1 = bs(str(soup.find_all("h1", class_="entry-title")), self.parser)
        for game in soup1.find_all("a"):
            self.result_list.append([game.text, game.attrs['href']])
        self.makeFile("fitgirl-repacks.site")
        self.Notify("fitgirl-repacks.site")
        self.result_list.clear()

    def gog_site(self):
        soup = bs(requests.get(
            f'https://gog-games.com/search/{self.gname}').text, self.parser)
        fin = soup.find_all("a", class_="block")
        for i in fin:
            self.result_list.append([str(i.attrs['href']).split(
                "/")[-1], "If you see the game title its probably cracked"])
        self.makeFile("gog-games.com")
        self.Notify("gog-games.com")
        self.result_list.clear()

    def game_2u(self):  # PS4 games
        soup = bs(requests.get(
            f"https://game-2u.com/?s={self.gname}").text, self.parser)
        soup1 = bs(str(soup.find_all("h2", class_="entry-title")), self.parser)
        fin = soup1.find_all("a")
        for i in fin:
            self.result_list.append([i.text, i.attrs['href']])
        self.makeFile("game-2u.com - For PS4 games")
        self.Notify("game-2u.com")
        self.result_list = []

    def gamestatus(self): ##1st get results from search /back/api/gameinfo/game/search_title/
        data = json.dumps({'title':self.gname})
        headers = {    
            "Host": "gamestatus.info",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
            "Accept": "application/json",
            "Accept-Language": "ar,en-US;q=0.7,en;q=0.3",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://gamestatus.info/?lg=en",
        }
        cook = requests.session() #start cookies session (since they give it away)
        cook.headers.update({ #set cookies (in an easier way liek headers)
            "s_version": "2.3.0",
            "lg":"en",
            "csrftoken":"WwdlhXB2WSuJ7JEl7g6lUw0hUrItwDx5gmuPkZyjrDUjoKs3QUcfIaKourQ3Pgli"
        })
        r = cook.post("https://gamestatus.info/back/api/gameinfo/game/search_title/", data=data, headers=headers)
        resp = r.content
        names = []
        for index, val in enumerate(json.loads(resp)):
            print('[{}] - {}'.format(index+1, val['slug']))
            names.append(val['slug'])
        if len(names) >= 1:
            userchoice= input(Style.RESET_ALL + "[?] - Enter one of the games shown -> ")
            game = names[int(userchoice)-1]
            #2nd getting game status
            resp = json.loads(requests.get("https://gamestatus.info/back/api/gameinfo/game/{}/?lg=en/".format(game)).content)
            self.result_list.append([game, resp['readable_status']])
            self.makeFile("gamestatus.info")
            self.Notify("gamestatus.info")
            self.result_list.clear()
        else:
            print(Fore.RED + "[!] - No result were found on gamestatus.info")

    def makeFile(self, website):  # file to put status on different files
        with open(f"{self.gname}.txt", "a") as f:
            f.write(f"\t\t{website} Results\n" + "=" + ("-"*50) + "=" + "\n")
            for val in self.result_list:
                f.write(f" [*] {val[-2]} : {val[-1]}\n")
            f.write("\n\n")

    def Notify(self, website):
        print(Fore.GREEN + f"[*] - {website} results has been written in \'{self.gname}.txt\' file\n")