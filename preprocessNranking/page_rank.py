import pandas as pd
import math
import time

def out_edges_dictionary():
    df = pd.read_csv('user_friends.csv')
    no_users = len(df)
    no_of_edges = 0
    out_map = {} #this maps the nodes to no_of_outgoing edges
    for index in range(no_users):
        if isinstance(df['friends'].iloc[index], float):
            print(index, df['friends'].iloc[index])
            out_edges = 0
            # out_map[str(df['user'].iloc[index])] = [0,0,out_edges]
        else:
            out_edges = len(df['friends'].iloc[index].split(" "))
            out_map[str(df['user'].iloc[index])] = [2,0,out_edges]
        no_of_edges += out_edges
    print("no of edges: ",no_of_edges)
    return out_map

def csv_to_edges():
    df = pd.read_csv('user_friends.csv')
    no_users = len(df)
    print("running.......")
    f = open("edges.csv", "a")
    for index in range(no_users):
        user = str(df['user'].iloc[index])
        if not isinstance(df['friends'].iloc[index], float):
            friends = df['friends'].iloc[index].split(" ")
            for friend in friends:
                f.write(user+","+friend+"\n")
    f.close()
    print("finished XD...")

def page_rank(file, out_edges, iterations, damping):
    for iteration in range(iterations):
        print("Iteration :", iteration, ".......")
        prev = iteration%2
        curr = (iteration+1)%2
        prev_node = -1
        rank_sum = 0
        with open(file, encoding="utf-8") as edges:
            for edge in edges:
                edge = edge.strip("\n")
                edge = edge.split(",")
                if prev_node!=edge[0]:
                    if prev_node!=-1:
                        out_edges[prev_node][curr] = (1-damping) + (damping * rank_sum)
                    rank_sum = 0
                    prev_node = edge[0]
                if(edge[1] in out_edges):
                    rank_sum += (out_edges[edge[1]][prev]/out_edges[edge[1]][2])
            out_edges[prev_node][curr] = (1-damping) + (damping * rank_sum)
    f = open("ranks.csv", "a")
    f.write("user,score\n")
    for key, val in out_edges.items():
        score = val[iterations%2]
        f.write(key+","+str(score)+"\n")
    f.close()

def main():
    out_edges = out_edges_dictionary()
    csv_to_edges()
    # out_edges = {"1":[1,0,3], "2":[1,0,2], "3":[1,0,1], "4":[1,0,2]}
    start = time.time()
    page_rank("edges.csv", out_edges, 50, 0.85)
    end = time.time()
    print("page_rank for 30 Million edges took :",(end-start)/60," minutes")
if __name__ == "__main__":
    main()
