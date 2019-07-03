# HackerShell
Multi-threading Reverse Shell program to connect and access Remote Computers using Command Lines

Multi-threading have been implemented in this program to connect to multiple computers/slients.

# How to Run?
To run this program we need to put our server.py file on a server so that we can get static IP for our client.py file, but if you wanted to run and test the code on your local machine you have to put your IP address in the address variable in the client.py file.

# How this works?
After we run server.py file on our machine, different machines will be able to connect to our server using the IP address of our server.
Once the clients are connected to our server the following command gives following results

```python
turtle> list
```
This command will gives the list of all the IPs that are connected to our server.

```pyhton
turtle> list
---------------Connections------------
0 FRIEND-1
1 FRIEND-2
2 FRIEND-3
.
.
.
```
Then using 

```python
turtle> select 0
```

will select client-0, and then we will be able to access client-0's computer from our computer.
