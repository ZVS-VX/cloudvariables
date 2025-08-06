Lastest version: beta v0.1
--------------------------

Example of client:
____________________________________________________________________________________________________________________________                                                                                                                          
from cloudvariables import Net                                                                                               
                                                                                                                              
n = Net()                                               # Creating object                                                     
                                                                                                                              
n.set_port(5000)                                        # Set port of your server                                             
                                                                                                                              
n.set_server("Your server ip, works by local net.")     # Set ip of your server                                               
                                                                                                                              
n.start()                                               # Connect to the server                                              
                                                                                                                              
password = "Password for your base"                                                                                           
                                                                                                                              
token = n.create(password)                              # Creating variable base by password, returning your new token        
                                                                                                                              
n.connect(token, password)                              # Connect to your base                                                
                                                                                                                              
n.set("Name", "Value")                                  # Set new value of your variable (or make new)                        
                                                                                                                              
n.get("Name")                                           # Get the value of your variable                                      
                                                                                                                              
n.del_var("Name")                                       # Remove your variable                                                
                                                                                                                              
n.del_proj(password)                                    # Remove your base (with all variables)                               
_____________________________________________________________________________________________________________________________ 

Example for the server is server.py, recommended for your server.
