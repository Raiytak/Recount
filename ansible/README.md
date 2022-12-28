# Installation

## Ansible
You can install the application using Ansible.
For that, you need to :
-connect to your server
-create the user `user-ansible` on your server
-add it to the `sudo` group
-edit your inventory to set the `app1` as your server
-edit the variables such as paswords in `roles/recount/shared/main.yml` (use ansible-vault for that)
-launch the following command:
```
python3 -m ansible playbook -i inventory.ini --user user-ansible --become --ask-become-pass --ask-vault-password install-recount.yml
```