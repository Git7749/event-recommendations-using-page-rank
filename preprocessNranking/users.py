import pandas as pd

def csv_to_edges():
    ranks = pd.read_csv("ranks.csv")
    no_users = ranks.shape[0]
    users_dict = {}
    for i in range(no_users):
        user = str(int(ranks.iloc[i]['user']))
        score = ranks.iloc[i]['score']
        users_dict[user] = [0,score]
    print(users_dict)
    df = pd.read_csv('event_attendees.csv')
    no_events = df.shape[0]
    f = open("events_users.csv", "a")
    for i in range(no_events):
        event = str(df.iloc[i]['event'])
        if not pd.isna(df.iloc[i,1]):
            yes = df.iloc[i]['yes'].split(" ")
            for user in yes:
                if user in users_dict:
                    print("event: ", event)
                    users_dict[user][0] += 1
                    f.write(event+","+user+",yes\n")
        if not pd.isna(df.iloc[i,2]):
            maybe = df.iloc[i]['maybe'].split(" ")
            for user in maybe:
                if user in users_dict:
                    users_dict[user][0] += 1
                    f.write(event+","+user+",maybe\n")
        if not pd.isna(df.iloc[i,3]):
            invited = df.iloc[i]['invited'].split(" ")
            for user in invited:
                if user in users_dict:
                    users_dict[user][0] += 1
                    f.write(event+","+user+",invited\n")
    f.close()
    return users_dict

def event_rank(users_dict):
    weights = {'yes':9, 'maybe':6, 'invited':5}
    event_rank = {}
    prev_node = -1
    rank_sum = 0
    with open("events_users.csv", encoding="utf-8") as edges:
        for edge in edges:
            edge = edge.strip("\n")
            edge = edge.split(",")
            if edge[0] != prev_node:
                if prev_node != -1:
                    event_rank[prev_node] = rank_sum;
                    print("finished event: ",prev_node)
                rank_sum = 0
                prev_node = edge[0]
            rank_sum += ((users_dict[edge[1]][1]/users_dict[edge[1]][0]) * weights[edge[2]])
    print("finished.....")
    f = open("event_ranks.csv", "a")
    f.write("events,score\n")
    for key, val in event_rank.items():
        f.write(key+","+str(val)+"\n")
    f.close()

def main():
    users_dict = csv_to_edges()
    event_rank(users_dict)


if __name__ == '__main__':
    main()
