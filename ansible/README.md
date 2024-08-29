# Installation

You can install the application using Ansible.
For that, you need to :
-connect to your server
-create the user `user-ansible` on your server
-add it to the `sudo` group
-edit the variables such as paswords in `roles/recount/shared/main.yml` (use ansible-vault for that)
-launch the following command:
```
ansible-playbook --user user-ansible --become --ask-become-pass --ask-vault-password playbook.yml
```