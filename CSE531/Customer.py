#
#   Customer.py
#
# Marco Ermini - March 2021 for ASU CSE531 Course
# Do not leech!
# Built with python 3.8 with GRPC and GRPC-tools libraries; may work with other Python versions
'''Implementation of a banking's branches/customers RPC synchronisation using GRPC, multiprocessing and Python
Customer Class'''

import time
import datetime
import multiprocessing
import json

from concurrent import futures
from Util import setup_logger, MyLog, sg, get_operation, get_operation_name, get_result_name

import grpc
import banking_pb2
import banking_pb2_grpc   

ONE_DAY = datetime.timedelta(days=1)
logger = setup_logger("Customer")

class Customer:
    """ Customer class definition """

    def __init__(self, _id, events):
        # unique ID of the Customer
        self.id = _id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None
        # GUI Window handle, if used
        self.window = None

    # Create stub for the customer, matching them with their respective branch
    #
    def createStub(self, Branch_address, THREAD_CONCURRENCY):
        """ Boots a client (customer) stub in a subprocess
            If PySimpleGUI/TK are installed, launches a window in the Windows' Manager.

        Args:
            Self:               Customer class
            Branch_address:     TCP/IP address/port where to fund the Branch to connect to
            THREAD_CONCURRENCY: Integer, number of threads concurrency

        Returns:
            None

        """
        
        MyLog(logger, f'[Customer {self.id}] Initializing customer stub to branch stub at {Branch_address}')
        
        self.stub = banking_pb2_grpc.BankingStub(grpc.insecure_channel(Branch_address))

        if (sg != NotImplemented):
            layout = [
                [sg.Text("Operations Loaded:", size=(60,1), justification="left")],
                [sg.Listbox(values=self.events, size=(60, 3))],
                [sg.Output(size=(80,12))],
                [sg.Button("Run", tooltip='Start Customer\'s Operations')],
                [sg.Button("Close", tooltip='Terminate Customer')]
            ]

            # Create the window
            sg.theme('Dark Green 5')
            self.window = sg.Window(f"Customer #{self.id} -> To Branch @ {Branch_address}"
                , layout
                , location=(100*(self.id)+20,100*self.id)
            )

        client = grpc.server(futures.ThreadPoolExecutor(max_workers=THREAD_CONCURRENCY,),)
        client.start()

    # Iterate through the list of the customer's events, sends the messages,
    # and output to the JSON file
    #
    def executeEvents(self, output_file):
        """Execute customer's events."""
                
        record = {'id': self.id, 'recv': []}
        for event in self.events:
            request_id = event['id']
            request_operation = get_operation(event['interface'])
            request_amount = event['money']
            
            try:
                LogMessage = (
                    f'[Customer {self.id}] executing request: ID {request_id} against Branch - '
                    f'Operation: {get_operation_name(request_operation)} - '
                    f'Initial balance: {request_amount}')
                MyLog(logger, LogMessage, self)

                response = self.stub.MsgDelivery(
                    banking_pb2.MsgDeliveryRequest(
                        REQ_ID=request_id,
                        OP=request_operation,
                        Amount=request_amount,
                        D_ID=self.id,
#                        Clock=None
                    )
                )
                
                LogMessage = (
                    f'[Customer {self.id}] Received response to request ID {request_id} from Branch - '
                    f'Operation: {get_operation_name(request_operation)} - Result: {get_result_name(response.RC)} - '
                    f'New balance: {response.Amount}')
                values = {
                    'interface': get_operation_name(request_operation),
                    'result': get_result_name(response.RC),
                }
                MyLog(logger, LogMessage, self)

                if request_operation == banking_pb2.QUERY:
                    values['money'] = response.Amount
                record['recv'].append(values)
                                 
                if record['recv']:
                    # DEBUG
                    #MyLog(logger,f'Writing JSON file on #{output_file}')
                    with open(f'{output_file}', 'a') as outfile:
                        json.dump(record, outfile)
                        outfile.write('\n')
                        
            except grpc.RpcError as rpc_error_call:
                code = rpc_error_call.code()
                details = rpc_error_call.details()

                if (code.name == "UNAVAILABLE"):
                    LogMessage = (f'[Customer {self.id}] Error on Request #{request_id}: Branch {self.id} likely unavailable - Code: {code} - Details: {details}')
                else:
                    LogMessage = (f'[Customer {self.id}] Error on Request #{request_id}: Code: {code} - Details: {details}')
                MyLog(logger, LogMessage, self)
 
    # Spawn the Customer process client. No need to bind to a port here; rather, we are connecting to one.
    #
    def Run_Customer(self, Branch_address, output_file, THREAD_CONCURRENCY):
        """Start a client (customer) in a subprocess."""

        MyLog(logger,f'[Customer {self.id}] Booting...')

        Customer.createStub(self, Branch_address, THREAD_CONCURRENCY)

        if (sg != NotImplemented):
            if (self.window != None):
                
                # Start events with "Run"
                while True:
                    wevent, values = self.window.read()
                    
                    # End program if user closes window or
                    # presses the Close button
                    if wevent == "Close" or wevent == sg.WIN_CLOSED:
                        MyLog(logger,f'[Customer {self.id}] Closing windows.')
                        break
                    if wevent == "Run":
                        Customer.executeEvents(self, output_file)
                        MyLog(logger,f'[Customer {self.id}] Exiting successfully.')
                        #break

                self.window.close()
        else:
            Customer.executeEvents(self, output_file)
            MyLog(logger,f'[Customer {self.id}] Exiting successfully.')
