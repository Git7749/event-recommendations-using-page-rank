import pandas as pd

def user_final():
    ranks = pd.read_csv("ranks.csv")
    scores = {}
    for i in range(ranks.shape[0]):
        scores[str(ranks.iloc[i]['user'])] = ranks.iloc[i]['score']
    users = pd.read_csv("users.csv")
    no = 0
    user_set = set(ranks['user'])
    for i in range(users.shape[0]):
        if not(users.iloc[i]["user_id"] in user_set):
            # print(users.iloc[i]["user_id"])
            no+=1
            scores[str(users.iloc[i]["user_id"])] = 0.0
    print(len(scores), no)
    f = open("users_ranks_final.csv", "a")
    f.write("user,score\n")
    for key, val in scores.items():
        f.write(key+","+str(val)+"\n")
    f.close()

def edges():
    ranks = pd.read_csv("users_ranks_final.csv")
    scores = {}
    user_set = set(ranks['user'])
    for i in range(ranks.shape[0]):
        scores[ranks.iloc[i]['user']] = ranks.iloc[i]['score']
    friends = []
    df = pd.read_csv('user_friends.csv')
    no_users = len(df)
    print("running.......")
    f = open("edges_final.csv", "a")
    f.write("user,friend")
    for index in range(no_users):
        user = str(df['user'].iloc[index])
        if not isinstance(df['friends'].iloc[index], float):
            friends = df['friends'].iloc[index].split(" ")
            friends_n = []
            no = 0
            for friend in friends:
                if int(friend) in user_set:
                    friends_n.append(friend)
                    no+=1
            print("no of friends: ", no)
            friends_n.sort(key = lambda a : scores[int(a)], reverse = True)
            for i in range(5):
                if i<len(friends_n):
                    f.write(user+","+friends_n[i]+"\n")
    f.close()
    print("finished XD...")

def main():
    # user_final()
    edges()
if __name__ == '__main__':
    main()
