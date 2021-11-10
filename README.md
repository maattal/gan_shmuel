Welcome Blue team -
Here our repository for the week,few steps before you can pull/push files into it.

Adding a ssh key:
cd ~/.ssh
ssh-keygen -o -t rsa -C "your-mail@gmail.com"
enter password : the best is to make it empty, type enter twice.
ssh-add ~/.ssh/<private_key_file> (give a file name of your own, publickey for example)

Cloning our ganshmuel_blue repo:
go to the folder you want to work from
run the command :git clone git@github.com:maattal/gan_shmuel.git
enter the cloned folder : cd gan_shmuel
connect your local branch to the remote branch git checkout -b <branch> --track origin/<branch>  [three branchs for the three teams, 'billing' 'weight' 'devops']
enter the folder of your team 
  
From this point, you can work into your branch :
connect to your branch git checkout -b <branch>
add your files locally git add .
commit your files git commit -m "message" <commit>
set your remote origin git remote add origin git@github.com:maattal/gan_shmuel.git
set your remote branch git push --set-upstream origin <branch>
push your files to the remote git push

test
test
final test?
final test?
test
test
miracle
miracle
Hachem
Hachem
test
sss
aaaa
test-demo-shay
asaad try
