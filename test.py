progress = input("Please write a progress: ")
season_index = progress.find("s")
episode_index = progress.find("e")
season = progress[season_index:episode_index]
episode = progress [episode_index:]
if season_index != 0 or not progress[season_index + 1].isdigit() or season_index == -1 or not progress[episode_index - 1].isdigit() or not progress[episode_index + 1].isdigit() or episode_index == -1:
    print("incorrect format")
else:
    print(season_index , " " , episode_index , "\n")
    print(season, " ", episode, "\n")
    print(len(progress))