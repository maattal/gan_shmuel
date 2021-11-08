simple docker on the ec2 instance :
dont put the requirement of the request

i am  trying  with port 8085:5000  

i am trying to make another push15

i change the url of the webhook to just host and port 

Rebuild the docker on the server after the changes -> webhook works! [need to make a volume?]

run the docker ci with socket volume for the dind strategy :
sudo docker run -v /var/run/docker.sock:/var/run/docker.sock -ti container_name
