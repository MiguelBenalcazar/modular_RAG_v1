## Install
https://neo4j.com/docs/operations-manual/current/installation/
install desktop version too


### 1. In console
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/neotechnology.gpg
echo 'deb [signed-by=/etc/apt/keyrings/neotechnology.gpg] https://debian.neo4j.com stable latest' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update

### 2. install console - Community Edition
sudo apt-get install neo4j=1:5.22.0

## Once installed
### 1. check status

sudo systemctl status neo4j

### 2. start service
sudo systemctl start neo4j

### 3. stop serviceDefault login is username 'neo4j' and password 'neo4j'
sudo systemctl stop neo4j

### 4. Enable Neo4j to Start on Boot
sudo systemctl enable neo4j

### 5. Disable Neo4j from Starting on Boot
sudo systemctl disable neo4j


### 6. View Neo4j Logs
sudo journalctl -u neo4j


## Configure service web-browser
http://localhost:7474/browser/
Default login is username 'neo4j' and password 'neo4j'


key for load desktop app

eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ii4rQC4rIiwibWl4cGFuZWxJZCI6IiRkZXZpY2U6MTkxNWIzOTQ4NTcxNDQzLTA0OWVlYzk5ZWI3YTU4LTEwNDYyYzZmLTFiYWI4ZC0xOTE1YjM5NDg1ODE0NDMiLCJtaXhwYW5lbFByb2plY3RJZCI6IjRiZmIyNDE0YWI5NzNjNzQxYjZmMDY3YmYwNmQ1NTc1Iiwib3JnIjoiLioiLCJwdWIiOiJuZW80ai5jb20iLCJyZWciOiIgIiwic3ViIjoibmVvNGotZGVza3RvcCIsImV4cCI6MTc1NjAyMDA4NCwidmVyIjoiKiIsImlzcyI6Im5lbzRqLmNvbSIsIm5iZiI6MTcyNDQ4NDA4NCwiaWF0IjoxNzI0NDg0MDg0LCJqdGkiOiJwZGhpT0tHTUIifQ.v5ViE-n_1aju3Ghyh4l8r0UJDdyqJTHy6qZJBKRugb4j55SON5zh6WHXoHSZCtefAkAnMFWlWik5OsUMHlNr_6s2ncQnALqAWZCzy2Tt7R4JLapmo8RjRlPMZp2rxFcNFazKt2tE2vYp8jf8KlON8LpAt1Sf5I5AXjtaH0rd1ywKwU6VjxPa5CV7P-0gZ1XVGQVzHTD2FeEQu1K0sbHiWxgQ1n2aRKKGw5dmI1tKokTihrQOaiCyW67Ecq2yhgzBEhlCMqtjnsZOdKfKiAnE5Wm00mJZL8PxPs1nOx6it_b_JFhC8DVml0Eqrm5Chm5FhLGC__Ih7-Bxy_bge_r8-Q


## APOC
if error APOC please go to Desktop APP, select project and plugins tab, install APOC