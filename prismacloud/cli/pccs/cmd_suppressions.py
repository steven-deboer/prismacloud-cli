import logging
import click

from prismacloud.cli import cli_output, pass_environment
from prismacloud.cli.api import pc_api


@click.group("suppressions", short_help="List suppression rules")
@pass_environment
def cli(ctx):
    pass


@click.command("list", short_help="List suppression rules")
def list_suppressions():
    """List suppression rules"""
    suppressions = pc_api.suppressions_list_read()
    cli_output(suppressions)


@click.command("justifications", short_help="Get suppressions justifications for all policy id and accounts")
def list_justifications():
    """Get suppressions justifications for all policy id and accounts"""
    data = []
    suppressions = pc_api.suppressions_list_read()
    for suppression in suppressions:
        logging.info("Get policy ID: %s", suppression["id"])
        if "resources" in suppression:
            accounts = []
            for account in suppression["resources"]:
                accounts.append(account["accountId"])

            query_params = {
                "accounts": accounts,
            }
            justifications = pc_api.suppressions_justifications_list_read(suppression["policyId"], query_params=query_params)
            for justification in justifications:
                if "resources" in justification:
                    data = data + [
                        {
                            "active": justification["active"],
                            "comment": justification["comment"],
                            "customer": justification["customer"],
                            "date": justification["date"],
                            "resources": justification["resources"],
                            "suppressionType": justification["suppressionType"],
                            "type": justification["type"],
                            "id": justification["id"],
                        }
                    ]

    cli_output(data)


cli.add_command(list_suppressions)
cli.add_command(list_justifications)
