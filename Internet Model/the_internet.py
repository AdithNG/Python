"""
File:    the_internet.py
Author:  Adith Nishanth Gunaseelan
Date:    12/2/2021
Description:
  Mini model of the internet
"""

# NOTE : SOME PARTS OF THE CODE USED FOR TESTING PURPOSES HAVE BEEN COMMENTED OUT !!!

#SERVERS = {'twitter.com': '104.244.42.193', 'facebook.com': '157.240.241.35', 'amazon.com': '172.5.12.128', 'netflix.com': '158.69.7.238', 'wikipedia.org': '208.80.154.244', 'umbc.edu': '143.204.151.121', 'twitch.tv': '151.101.210.167', 'discord.gg': '162.159.134.234'}
#DICT = {'twitter.com': [['facebook.com', 34], ['netflix.com', 31], ['wikipedia.org', 12]], 'facebook.com': [['twitter.com', 34], ['amazon.com', 14]], 'amazon.com': [['netflix.com', 22], ['facebook.com', 14]], 'netflix.com': [['amazon.com', 22], ['twitter.com', 31]], 'umbc.edu': [['twitch.tv', 33], ['wikipedia.org', 5]], 'twitch.tv': [['umbc.edu', 33]], 'wikipedia.org': [['umbc.edu', 5], ['twitter.com', 12]]}
#HOME = 'netflix.com'

def run_the_internet():

    
    servers = {}
    connections = {}
    home = ""
    
    user_input = input(">>> ")
    
    while user_input.lower() != 'quit':
        flag = 1
        input_split = user_input.split(" ")

        

        # Creating server
        
        
        if input_split[0] == "create-server":

            # Check for duplicates
            for key in servers:
                if input_split[2] in servers[key][0]:
                    flag = 0
                    
            # check if ip address is ipv4
            if len(input_split[2].split(".")) == 4:
                if flag:
                    servers[input_split[1]] = input_split[2]
                    print("Success: A server with name",input_split[1],"was created at ip",input_split[2])
                    #print(servers)
                    

        # Creating connection
        
        elif input_split[0] == "create-connection":
            
            if input_split[1] in servers and input_split[2] in servers:
                
                if input_split[1] in connections:
                    connections[input_split[1]].append([input_split[2],int(input_split[3])])

                if input_split[2] in connections:
                    connections[input_split[2]].append([input_split[1],int(input_split[3])])
                    
                if input_split[1] not in connections:
                    connections[input_split[1]] = [[input_split[2],int(input_split[3])]]

                if input_split[2] not in connections:
                    connections[input_split[2]] = [[input_split[1],int(input_split[3])]]

                print("Success: A server with name",input_split[1],"is now connected to",input_split[2])
                #print(connections)

            else:
                print("One or more servers are not reachable")


        # Setting up home server

        elif input_split[0] == "set-server":
            
            home_flag = 0
            if len(input_split[1].split(".")) == 2:
                if input_split[1] in servers:
                    home = input_split[1]
                    print("Server",home,"selected")
                
            elif len(input_split[1].split(".")) == 4:
                for element in servers.keys():
                    if servers[element] == input_split[1]:
                        home_flag = 1
                        home = element
                        
                if home_flag == 1:
                    print("Server",home,"selected")
                else:
                    print("Unrecognized IP address")
                    
            else:
                print("Unable to recognize server name or IP address")



        # Calculating ping from destination

        elif input_split[0] == "ping":
            ping_flag = 0
            
            if home:
    
                if len(input_split[1].split(".")) == 4:
                    
                    for element in servers.keys():
                        if servers[element] == input_split[1]:
                            end_server = element
                            ping_flag = 1
                            
                elif len(input_split[1].split(".")) == 2:
                    end_server = input_split[1]
                    ping_flag = 1

                else:
                    print("Destination unrecognizable")
                
                if ping_flag == 1:
                    
                    if end_server not in servers:
                        print("Unable to find server")
                        
                    else:
                        ping_time = ping(connections, home, end_server)
                        if ping_time == None:
                            print("Unable to receive ping from requested server")
                        else:
                            print("Reply from",servers[home],"time =",ping_time,"ms")
            else:
                print("Please set home-server first")


        # Show current server
                
        elif input_split[0] == 'ip-config':
            if home:
                print(home,'  ',servers[home])
            else:
                print("Home server not yet defined")



        # Trace path to requested server

        elif input_split[0] == 'traceroute' or input_split[0] == 'tracert' :
            
            trace_flag = 0
            
            if home:
            
                if len(input_split[1].split(".")) == 4:
                    
                    for element in servers.keys():
                        if servers[element] == input_split[1]:
                            end_server = element
                            trace_flag = 1
                            
                elif len(input_split[1].split(".")) == 2:
                    end_server = input_split[1]
                    trace_flag = 1
                    

                else:
                    print("Unable to resolve target system name",input_split[1])
                
                if trace_flag == 1:
                    
                    if end_server not in servers:
                        print("Unable to find path to server")
                        
                    else:
                        path = tracert(connections, home, end_server, servers, [input_split[1]])
                        
            else:
                print("Please set home-server first")

                


        # Displaying all servers       

        elif  input_split[0] == 'display-servers':
            
            for server in servers:
                print(server,"   ",servers[server])

                if server in connections:
                    for node in connections[server]:
                        print("\t",node[0],"   ",servers[node[0]],"   ",node[1])

                        
        else:
            print("Command not recognized")

            
            
        user_input = input(">>> ")
        

def tracert(web_map, starting_place, destination, servers, user_input):

    found = False
    
    if starting_place in web_map:
        
        for node in web_map[starting_place]:
            #print("Using node:",node)
                
            visited = [starting_place]
                
            if node[0] not in visited:
                found = path_finder_rec(web_map, node[0], destination, visited)
                #print("found:",found)
                    
                if found == True:
                        visited.append(destination)
                        #print(visited)

                        print("Tracing route to",destination,user_input)

                        # To print out routes
                        for i in range(len(visited)):
                            if i == 0:
                                print(0,"   ",0,"   ",servers[visited[i]],"   ",visited[i])
                            else:
                                for node in web_map[visited[i-1]]:
                                    if visited[i] == node[0]:
                                        print(i,"   ",node[1],"   ",servers[node[0]],"   ",node[0])
                                        
                        print("Trace Complete")
                        
                        return visited
                
    if found == False:
        print("Unable to resolve target system name",destination)

        

def ping(web_map, starting_place, destination):
    
    ping = 0
    if starting_place in web_map:
        
        for node in web_map[starting_place]:

            #print("Using node:",node)
                
            visited = [starting_place]
                
            if node[0] not in visited:
                found = path_finder_rec(web_map, node[0], destination, visited)
                #print("found:",found)
                    
                if found == True:
                        visited.append(destination)
                        #print(visited)

                        # To calculate ping
                        for i in range(1,len(visited)):
                            for node in web_map[visited[i-1]]:
                                if visited[i] == node[0]:
                                    ping += node[1]
                                    
                        return ping




def path_finder_rec(web_map, starting_place, destination, visited):
    
    # base case
    if starting_place == destination:
        #print("destination reached:", destination)
        return True

    # base case 2
    if starting_place in visited:
        return False
    
    visited.append(starting_place)
    #print("Visited:",visited)
    
    # recursive case
    result = False
    for node in web_map[starting_place]:
        #print("Node: ",node[0])
        
        if node[0] not in visited:
            if path_finder_rec(web_map, node[0], destination, visited):
                result = True
                return True
        #print("result:",result)
    return result



if __name__ == '__main__':
    run_the_internet()
