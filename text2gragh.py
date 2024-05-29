import os
import random
import re
import networkx as nx
import matplotlib.pyplot as plt

class DirectedGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, target):
        if source in self.graph:
            if target in self.graph[source]:
                self.graph[source][target] += 1
            else:
                self.graph[source][target] = 1
        else:
            self.graph[source] = {target: 1}

    def get_neighbors(self, node):
        return self.graph.get(node, {})

def preprocess_text(text):
    # 将标点符号替换为空格
    text = re.sub(r'[\W_]+', ' ', text)
    # 将换行和回车符替换为空格
    text = text.replace('\n', ' ').replace('\r', ' ')
    return text.lower()

def build_graph_from_text(text):
    graph = DirectedGraph()
    words = text.split()
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        graph.add_edge(word1, word2)
    #graph.add_edge(words[-1], file_end)
    return graph




def showDirectedGraph(graph, filename):
    print("Directed Graph:")
    for node in graph.graph:
        neighbors = graph.graph[node]
        for neighbor in neighbors:
            #if neighbor != file_end:
            print(f"{node} -> {neighbor} (weight: {neighbors[neighbor]})")

    # drawDirectedGraph
    G = nx.DiGraph()
    for node in graph.graph:
        for neighbor in graph.graph[node]:
            #if neighbor != file_end:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, iterations=50, k=0.3)  # positions for all nodes
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=1500) # 节点大小
    # edges
    # nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, arrowstyle='-|>', arrowsize=15, node_size=1300) # node_size设置指向的节点半径
    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    plt.axis("off")
    check_filename = filename.split('.')[-1]
    if check_filename in ['eps', 'jpeg', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz', 'tif', 'tiff', 'web']:
        plt.savefig(output_dir + filename)
        plt.show()
        return f"The graph is saved as '{filename}'. "
    else:
        plt.savefig(output_dir + filename + '.png')
        plt.show()
        return f"Format '{check_filename}' is not supported. \n(supported formats: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp) \nThe graph is saved as '{filename}.png'."
    

def showDirectedGraph_withsp(graph, filename,path):
    paths = []
    for i in range(len(path)-1):
        paths.append(str(path[i])+"->"+str(path[i+1]))
    # drawDirectedGraph
    G = nx.DiGraph()
    edges = []
    colors = []
    for node in graph.graph:
        for neighbor in graph.graph[node]:
            #if neighbor != file_end:
            G.add_edge(node, neighbor)
            edges.append((node, neighbor))
            # 这里可以指定每条边的颜色，例如根据某些条件
            if( str(node)+"->"+str(neighbor) in paths):
                colors.append('red')
            else:
                colors.append('blue')  # 这里设置所有边为蓝色，可以根据需要修改

    pos = nx.spring_layout(G, iterations=300, k=0.3) # positions for all nodes
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=1500) # 节点大小
    # edges
    # nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2)
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, arrowstyle='-|>', arrowsize=15,edge_color=colors, node_size=1300) # node_size设置指向的节点半径
    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    plt.axis("off")
    check_filename = filename.split('.')[-1]
    if check_filename in ['eps', 'jpeg', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz', 'tif', 'tiff', 'web']:
        plt.savefig(output_dir + filename)
        plt.show()
        return f"The graph is saved as '{filename}'. "
    else:
        plt.savefig(output_dir + filename + '.png')
        plt.show()
        return f"Format '{check_filename}' is not supported. \n(supported formats: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp) \nThe graph is saved as '{filename}.png'."



def queryBridgeWords(word1, word2):
    if word1 not in graph.graph or word2 not in graph.graph:
        return f"No '{word1}' or no '{word2}' in the graph!"

    bridge_words = []
    for neighbor in graph.graph[word1]:
        if neighbor in graph.graph and word2 in graph.graph[neighbor]:
            bridge_words.append(neighbor)

    if not bridge_words:
        return f"No bridge words from '{word1}' to '{word2}'!"
    else:
        return f"The bridge words from '{word1}' to '{word2}' are: {', '.join(bridge_words)}."

def generateNewText(input_text):
    words = input_text.split()
    new_text = []
    for i in range(len(words) - 1):
        new_text.append(words[i])
        if words[i] in graph.graph and words[i + 1] in graph.graph:
            bridge_words = [neighbor for neighbor in graph.graph[words[i]] if neighbor in graph.graph and words[i + 1] in graph.graph[neighbor]]
            if bridge_words:
                new_text.append(random.choice(bridge_words))
    new_text.append(words[-1])
    return ' '.join(new_text)

def calcShortestPath(word1, word2):
    # 用户未输入单词
    if (word1 == '') and (word2 == ''):
        return "Please enter at least one word!"

    # 用户输入一个单词
    if (word1 == '') or (word2 == ''):
        if word1 not in graph.graph and word2 not in graph.graph:
            return f"No '{word1}' or '{word2}' in the graph!"
        
        word = word1 if word1 else word2
        shortest_paths = ""
        for end_word in graph.graph.keys():
            if end_word != word:
                visited = set()
                queue = [[word]]
                while queue:
                    path = queue.pop(0)
                    node = path[-1]
                    if node == end_word:
                        shortest_path = ' -> '.join(path)
                        shortest_paths += f"The shortest path from '{word}' to '{end_word}' is: {shortest_path}.\n"
                    if node not in visited:
                        neighbors = graph.get_neighbors(node)
                        for neighbor in neighbors:
                            new_path = list(path)
                            new_path.append(neighbor)
                            queue.append(new_path)
                    visited.add(node)
                if shortest_paths == "":
                    shortest_paths = f"No path found between '{word}' other words.\n"
       
        return shortest_paths

    # 用户输入两个单词
    if word1 not in graph.graph or word2 not in graph.graph:
        return f"No '{word1}' or no '{word2}' in the graph!"

    visited = set()
    queue = [[word1]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == word2:
            shortest_path = ' -> '.join(path)
            showDirectedGraph_withsp(graph, "sp.jpg", path)
            return f"The shortest path from '{word1}' to '{word2}' is: {shortest_path}."
        if node not in visited:
            neighbors = graph.get_neighbors(node)
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
        visited.add(node)
    return "No path found between '{word1}' and '{word2}'."

def randomWalk():
    start_node = random.choice(list(graph.graph.keys()))
    visited_nodes = [start_node]
    visited_edges = []

    while True:
        neighbors = graph.get_neighbors(start_node)
        if not neighbors:
            break
        next_node = random.choice(list(neighbors.keys()))

        visited_edges.append((start_node, next_node))
        visited_nodes.append(next_node)
        start_node = next_node
        if start_node in visited_nodes[:-1]:
            break

    return visited_nodes, visited_edges

def save_random_walk_to_file(visited_nodes, visited_edges, filename):
    with open(output_dir + filename, 'w') as f:
        f.write("Visited Nodes:\n")
        f.write(' '.join(visited_nodes) + '\n')
        f.write("Visited Edges:\n")
        for edge in visited_edges:
            f.write(f"{edge[0]} -> {edge[1]}\n")
    return f"随机游走路径是 '{filename}'."

def main():
    global data_dir
    global output_dir
    output_dir = "./output/"
    #global file_end

    global graph

    init_flag = True

    while True:

        #fileneme = input("请输入文本文件路径：")
        #if fileneme == "":
        #    fileneme = "./data/text.txt"
        with open("./data/text.txt", 'r') as file:
            text = file.read()
        #print(text)
        text = preprocess_text(text)
        print("text:",text)
        graph = build_graph_from_text(text)



        print("\nMenu:")
        print("1. 展示有向图")
        print("2. 查询桥接词")
        print("3. 生成新文本")
        print("4. 计算最短路径")
        print("5. 随机游走")
        print("6. 退出")

        choice = input("请输入你的选择: ")

        if choice == '1':     
            graphname = input("请你输入保存图的路径: ")
            if graphname == '':
                graphname = 'graph.png' 
                print(f"使用默认路径: {graphname}")
            print(showDirectedGraph(graph, filename=graphname))
        elif choice == '2':
            word1 = input("输入 word1: ").lower()
            word2 = input("输入 word2: ").lower()
            print(queryBridgeWords(word1, word2))
        elif choice == '3':
            input_text = input("请输入一段文本: ").lower()
            new_text = generateNewText(input_text)
            print("生成文本:", new_text)
        elif choice == '4':
            word1 = input("输入 word1 (或回车跳过): ").lower()
            word2 = input("输入 word2 (或回车跳过): ").lower()
            print(calcShortestPath(word1, word2))
        elif choice == '5':
            visited_nodes, visited_edges = randomWalk()
            print("访问过的节点:", visited_nodes)
            print("访问过的边:", visited_edges)
            print(save_random_walk_to_file(visited_nodes, visited_edges, "random_walk.txt"))
        elif choice == '6':
            break
        else:
            print("请输入有效数字！")

if __name__ == "__main__":
    main()
