#
#   Main.py
#
# Marco Ermini - March 2021 for ASU CSE531 Course
# Do not leech!
# Built with python 3.8 with GRPC and GRPC-tools libraries; may work with other Python versions
'''Implementation of a banking's branches/customers RPC synchronisation using GRPC, multiprocessing and Python
Main spawner'''

import logging
import multiprocessing

import contextlib
import socket
import argparse
import json
import array
import socketserver
import time

from concurrent import futures
from Branch import Branch, Run_Branch
from Customer import Customer
from Util import setup_logger, MyLog, sg

import grpc

import banking_pb2
import banking_pb2_grpc

# Multiprocessing code reused from https://github.com/grpc/grpc/tree/801c2fd832ec964d04a847c6542198db093ff81d/examples/python/multiprocessing
#

# setup a maximum number of thread concurrency following the number of CPUs x cores enumerated by Python
#THREAD_CONCURRENCY = multiprocessing.cpu_count()
THREAD_CONCURRENCY = 2
SLEEP_SECONDS = 5

def Process_Args():
    """Parse arguments."""
    all_args = argparse.ArgumentParser(description='Input and Output file names')
    all_args.add_argument('-i', '--Input', required=False, help='File name containing branches and customers, in JSON format (optional; defaults to input.json')
    all_args.add_argument('-o', '--Output', required=False, help='Output file name to use (optional; defaults to output.json)')
    args = all_args.parse_args()
    return args.Input.strip(), args.Output.strip()

# Load input file with branches and customers
#
def Load_Input_File(filename, branches_list, customers_list):
    """Load branches, customers and events from input files."""
    try:
        file = open(filename)
    except OSError:
        raise RuntimeError(f'Failed to open {filename}.')
    
    items = json.load(file)
    
    # Retrieves:
    #   the branches' list and populate IDs and balances
    #   the customers' operations and populate events
    for item in items:
        if item['type'] == 'branch':
            branch = Branch(item['id'], item['balance'], list())
            branches_list.append(branch)
        if item['type'] == 'customer':
            events = list()
            for event in item['events']:
                events.append(event)
            customer = Customer(item['id'], events)
            customers_list.append(customer)

    # Append the list of all branches to every branch - except self
    for b in branches_list:
        for b1 in branches_list:
            if b.id != b1.id:
                b.branches.append(b1.id)
        MyLog(logger, f'[Main] Branch {b.id} initialised with Balance={b.balance}; Other branches identified={b.branches}')

    # Append the list of all events to customers
    for c in customers_list:
        for e in c.events:
            MyLog(logger, f'[Main] Customer {c.id} identified event #{e["id"]} = {e["interface"]}, {e["money"]}')

    file.close()


# Utility function to reserve a port for the Branches' servers.
# Always find an usable TCP/IP port on localhost.
#
#@contextlib.contextmanager
#def Reserve_Port():
#    """Find and reserve a port for the subprocess to use."""
#    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
#    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#    if  sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
#        raise RuntimeError("Failed to set SO_REUSEPORT.")
#    sock.bind(('', 0))
#    try:
#        yield sock.getsockname()[1]
#    finally:
#        sock.close()
#
def Reserve_Port():
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
    return free_port

def main():
    """Main function."""

    MyLog(logger, f'[Main] *** Processing Arguments ***')

    input_file, output_file = Process_Args()
    if not input_file:
        input_file = 'input.json'
    if not output_file:
        output_file = 'output.json'
    branches_list = list()
    customers_list = list()

    MyLog(logger, f'[Main] *** Processing Input File ***')

    Load_Input_File(input_file, branches_list, customers_list)
    branches_addresses_ids = []
    workers = list()

    # Spawns processes for branches
    #
    # NOTE: It is imperative that the worker subprocesses be forked before
    # any gRPC servers start up. See
    # https://github.com/grpc/grpc/issues/16001 for more details.

    MyLog(logger, f'[Main] *** Starting Processes for Servers/Branches ***')

    # Reserve the addresses for Branches
    for curr_branch in branches_list:
        curr_port = Reserve_Port()
        curr_branch.bind_address = '[::]:{}'.format(curr_port)
        # save branch bind address for the customers and other branches to know
        branches_addresses_ids.append ([curr_branch.id, curr_branch.bind_address])

    # Copy the list of all the branches and PIDs to all the Branches' list
    for curr_branch in branches_list:
        curr_branch.branchList = branches_addresses_ids[:]

    for curr_branch in branches_list:
        worker = multiprocessing.Process(name=f'Branch-{curr_branch.id}', target=Run_Branch,
                                            args=(curr_branch,THREAD_CONCURRENCY))
        worker.start()
        workers.append(worker)

        MyLog(logger, f'[Main] Booting branch \"{worker.name}\" on initial balance {curr_branch.balance}), '
                        f'with PID {worker.pid} at address {curr_branch.bind_address} successfully')

    if (sg == NotImplemented):
        # Wait some seconds before initialising the clients, to give time the servers to start
        MyLog(logger, f'[Main] *** Waiting for {SLEEP_SECONDS} seconds before starting the clients ***')
        MyLog(logger, f'[Main]     (Otherwise it will sometimes fail when the computer is slow)')
        time.sleep(SLEEP_SECONDS)

    # Spawns processes for customers
    #
    # We are spawning a process for each customer, which in turn execute their events via their stubs
    # and communicates with the respectives' servers' processes.
    # We need to pass the address binded of the matching server in the Customer class constructor
    # or it won't be able to determine it.

    MyLog(logger, f'[Main] *** Starting Processes for Clients/Customers ***')

    for curr_customer in customers_list:
        # DEBUG
        #LOGGER.info(f'Processing Customer #{curr_customer.id} with Events:' )
        #for e in curr_customer.events:
        #    LOGGER.info(f'    #{e["id"]} = {e["interface"]}, {e["money"]}' )
        #sys.stdout.flush()

        # Find the bind_address of the Branch for the current Customer and pass it to the Customer Class
        for i in range(len(branches_addresses_ids)):
            if branches_addresses_ids[i][0] == curr_customer.id:
                Branch_address = branches_addresses_ids [i][1]
                break
        
        worker = multiprocessing.Process(name=f'Customer-{curr_customer.id}', target=Customer.Run_Customer,
                                            args=(curr_customer,Branch_address,output_file,THREAD_CONCURRENCY))
        worker.start()
        workers.append(worker)
        
        MyLog(logger, f'[Main] Started Customer \"{worker.name}\" with PID {worker.pid} successfully.')

    for worker in workers:
        worker.join()


logger = setup_logger("Main")
if __name__ == '__main__':
    MyLog(logger, "[Main] Logger initialised")
    main()
