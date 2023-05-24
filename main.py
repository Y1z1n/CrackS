try:
    import crack
except:
    pass
else:
    obj = crack.Crack(gameName=input("[?] Search for : "))

    def main():
        obj.steamcrackedgames()
        obj.fitgirl_repacks()
        obj.gog_site()
        obj.game_2u()
        obj.gamestatus()

    if __name__ == '__main__':
        main()