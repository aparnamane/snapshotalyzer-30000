import boto3
import click
# import sys


session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_istances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Commands for instances"""


@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag project:<name>)")
def list_instnaces(project):
    "List EC2 instnaces"

    instances = filter_istances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(','.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('project', '<no project>')
            )))

    return

@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project (tag project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_istances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,
    help="Only instances for project (tag project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_istances(project)
    
    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return


if __name__ == '__main__':
    # print(sys.argv)
    instances()