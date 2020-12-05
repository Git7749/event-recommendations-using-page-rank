import pandas as pd
def user_final():
    users = pd.read_csv("users_final.csv")
    users_new = []
    for i in range(users.shape[0]):
        users_new.append(["u"+str(users.iloc[i]['user_id'])])
    df = pd.DataFrame(users_new)
    df.to_csv("users_new.csv",header = ["user_id"])

def users_ranks_final():
    ranks = pd.read_csv("users_ranks_final.csv")
    ranks_new = []
    for i in range(ranks.shape[0]):
        ranks_new.append(["u"+str(int(ranks.iloc[i]['user'])), ranks.iloc[i]['score']])
    df = pd.DataFrame(ranks_new)
    df.to_csv("ranks_new.csv", header=["user","score"])

def event_users_final():
    edges = pd.read_csv("event_users_final.csv")
    event_users_new = []
    for i in range(edges.shape[0]):
        print(i)
        event_users_new.append(["e"+str(int(edges.iloc[i]['event'])), "u"+str(int(edges.iloc[i]['user'])), edges.iloc[i]['weight']])
    df = pd.DataFrame(event_users_new)
    df.to_csv("event_users_new.csv", header=["event","user","weight"])

def edges_new():
    edges = pd.read_csv("edges_final.csv")
    event_users_new = []
    for i in range(edges.shape[0]):
        event_users_new.append(["u"+str(int(edges.iloc[i]['user'])), "u"+str(int(edges.iloc[i]['friend']))])
    df = pd.DataFrame(event_users_new)
    df.to_csv("edges_new.csv", header=["user","friend"])

def events():
    events = pd.read_excel ('events_final_updated.xlsx', sheet_name='events')
    location = pd.read_excel ('events_final_updated.xlsx', sheet_name='location')
    events = events[['event_id', 'start_time','location_id']]
    events_new = []
    for i in range(events.shape[0]):
        events_new.append(["e"+str(int(events.iloc[i]['event_id'])), events.iloc[i]['start_time'], events.iloc[i]['location_id']])
    events_new = pd.DataFrame(events_new, columns=["event_id","start_time","location_id"])
    writer = pd.ExcelWriter('events_new.xlsx', engine = 'xlsxwriter')
    events_new.to_excel(writer, sheet_name='events')
    location.to_excel(writer, sheet_name = 'location')
    writer.save()

def event_score():
    scores = pd.read_csv("event_ranks_final.csv")
    scores_new = []
    for i in range(scores.shape[0]):
        scores_new.append(["e"+str(int(scores.iloc[i]['event'])), scores.iloc[i]['score']])
    scores_new = pd.DataFrame(scores_new, columns=["event","score"])
    writer = pd.ExcelWriter('event_ranks_new.xlsx', engine = 'xlsxwriter')
    scores_new.to_excel(writer, sheet_name='events')
    writer.save()


def main():
    event_score()
    # events()
    # edges_new()
    # event_users_final()
    # users_ranks_final()
    # user_final()

if __name__ == '__main__':
    main()
