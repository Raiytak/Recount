import sys
import argparse

from accessors.file_management import Config
from accessors.encryption import generateKey


def changeSqlAdminPassword():
    key = str(generateKey())
    Config.setSqlAdminPassword(key)


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
    if not Config.ROOT.exists():
        raise FileNotFoundError("folder {} does not exist".format(Config.ROOT))
    if not Config.SQL.exists():
        raise FileNotFoundError("file {} does not exist".format(Config.SQL))
    changeSqlAdminPassword()
