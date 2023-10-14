ssh
use for ssh-keygen default fileName

```
ssh-keygen -t ed25519 -C "itmolerningproject@gmail.com" 
yAoL$zrb7KqKMYhwD#bmZFo7Yq4GuX^W%wrqqpEL!mQ!7UXMHGP!iJV^$zAc@o5i6p&
```

ssh-add /root/.ssh/git.pub
eval `ssh-agent -s`
reboot

```
export ENVIRONMENT=test
cd /home
git clone git@github.com:itmolerningproject/platform.git
cd platform/

checkout git 

source ./envs/$ENVIRONMENT.env or . ./envs/$ENVIRONMENT.env
echo $CR_PAT | docker login ghcr.io -u "itmolerningproject@gmail.com" --password-stdin


docker-compose -f docker-compose.$ENVIRONMENT.yml pull
docker-compose -f docker-compose.$ENVIRONMENT.yml up -d
```

```

git stash
git pull

```

git checkout development

https://support.atlassian.com/bitbucket-cloud/docs/check-out-a-branch/

https://docs.github.com/ru/authentication/connecting-to-github-with-ssh/managing-deploy-keys#deploy-keys
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key

vpn install sudo apt-get install network-manager-l2tp-gnome
https://github.com/hwdsl2/setup-ipsec-vpn/blob/master/docs/clients.md