import sys
import argparse

from accessors.file_management import ConfigManager
from accessors.encryption import generateKey

# TODO: Change name / action, expecting to provide a key to change the password
def changeSqlAdminPassword():
    key = str(generateKey())
    ConfigManager.setSqlAdminPassword(key)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--change-sql-admin-password",
    help="changes the sql admin password",
    action="store_true",
    default=False,
)

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

if args.change_sql_admin_password:
    if not ConfigManager.ROOT.exists():
        raise FileNotFoundError("folder {} does not exist".format(ConfigManager.ROOT))
    if not ConfigManager.SQL.exists():
        raise FileNotFoundError("file {} does not exist".format(ConfigManager.SQL))
    changeSqlAdminPassword()
