import pandas as pd
import time

def preprocess():
    print("loading data.........")
    df = pd.read_csv("events.csv")
    df1 = df[df['lat'].notna()]
    df1 = df1.reset_index(drop=True)
    rows = df1.shape[0]
    print("finished loading.....")
    print("length of ", df1.shape[0])
    locations = []
    print("running..............")
    for i in range(rows):
        location = ""
        if not isinstance(df1.iloc[i]['city'],float):
            print(df1.iloc[i]['city'])
            location += (df1.iloc[i]['city'] + ", ")
        if not isinstance(df1.iloc[i]['state'], float):
            location += (df1.iloc[i]['state'] + ", ")
        if not isinstance(df1.iloc[i]['country'], float):
            location += df1.iloc[i]['country']
        if location == "":
            location = str(df1.iloc[i]['lat'])+", "+str(df1.iloc[i]['lng'])
        locations.append(location)
    columns = ['event_id', 'start_time', 'lat', 'lng']
    df2 = df1.filter(items = columns)
    df2['location'] = locations
    df2.to_csv('events_processed.csv', header = ['event_id', 'start_time', 'lat', 'lng', 'location'])
    print("finished...........XD")

def event_reduce():
    df = pd.read_csv("event_ranks.csv")
    events_set = set(df['event'])
    df1 = []
    events = pd.read_csv("events_processed.csv")
    # events = events.head(10000)
    for i in range(events.shape[0]):
        if events.iloc[i]["event_id"] in events_set:
            print("running....", events.iloc[i]["event_id"])
            df1.append(events.iloc[i])
    df2 = pd.DataFrame(df1, columns=('event_id', 'start_time', 'lat', 'lng', 'location'))
    df2.to_csv("events_final.csv", header = ['event_id', 'start_time', 'lat', 'lng', 'location'], index = False)
    print("finished.........XD")

def events_edges_reduce():
    events = pd.read_csv("events_final.csv")
    edges = pd.read_csv("events_users.csv")
    scores = pd.read_csv("event_ranks.csv")
    events_set = set(events['event_id'])
    edges_new = []
    scores_new = []
    for i in range(edges.shape[0]):
        if edges.iloc[i]['event'] in events_set:
            edges_new.append(edges.iloc[i])
    for i in range(scores.shape[0]):
        if scores.iloc[i]['event'] in events_set:
            scores_new.append(scores.iloc[i])
    df_1 = pd.DataFrame(edges_new, columns=('event','user','weight'))
    df_1.to_csv("event_users_final.csv", header = ['event','user','weight'])

    df_2 = pd.DataFrame(scores_new, columns = ('event', 'score'))
    df_2.to_csv("event_ranks_final.csv", header = ['event', 'score'])

def drop_duplicates():
    df = pd.read_csv("events_final.csv")
    df1 = df[['location', 'lat', 'lng']]
    df1 = df1.drop_duplicates(keep='first')
    df1.reset_index(drop = True)
    id = "location"
    location_id = []
    for i in range(df1.shape[0]):
        location_id.append(id+str(i))
    df1['location_id'] = location_id
    location_id = []
    # df = df.head(100)
    # df1 = df1.head(100)
    for i in range(df.shape[0]):
        for j in range(df1.shape[0]):
            print(i," ",df.iloc[i]['location']," ", df1.iloc[j]['location'])
            if df.iloc[i]['location'] == df1.iloc[j]['location'] and df.iloc[i]['lat'] == df1.iloc[j]['lat'] and df.iloc[i]['lng'] == df1.iloc[j]['lng']:
                location_id.append(df1.iloc[j]['location_id'])
                break
    df['location_id'] = location_id
    writer = pd.ExcelWriter('events_final_updated.xlsx', engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name='events')
    df1.to_excel(writer, sheet_name = 'location')
    writer.save()



def main():
    # event_reduce()
    # events_edges_reduce()
    start = time.time()
    drop_duplicates()
    end = time.time()
    print("runtime: ",end-start,"minutes")
if __name__ == '__main__':
    main()
