#
#   Branch.py
#
# Marco Ermini - March 2021 for ASU CSE531 Course
# Do not leech!
# Built with python 3.8 with GRPC and GRPC-tools libraries; may work with other Python versions
'''Implementation of a banking's branches/customers RPC synchronisation using GRPC, multiprocessing and Python
Branch Class'''

import time
import datetime
import sys
import multiprocessing

from concurrent import futures
from Util import setup_logger, MyLog

import grpc
import banking_pb2
import banking_pb2_grpc

try:
    import PySimpleGUI as sg                #  Better than CTRL+c
except ImportError:
    sg = NotImplemented


ONE_DAY = datetime.timedelta(days=1)
logger = setup_logger("Branch")
SLEEP_SECONDS = 3

# A constant used to indicate that the Branch must not propagate an operation. This is because a Branch receiving a message
#   cannot distinguish between an operation is coming from a client or another branch or it has been received already.
#   Without this control, the branches would keep propagating operations in an infinite loop. By setting this value after
#   the first propagation, it is not spread further.
DO_NOT_PROPAGATE = -1       

class Branch(banking_pb2_grpc.BankingServicer):

    def __init__(self, ID, balance, branches):
        # unique ID of the Branch
        self.id = ID
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # Binded address
        self.bind_address = str
        # the list of Branches including IDs and Addresses
        self.branchList = list()
        # GUI Window handle, if used
        self.window = None
        # Local logical clock
        self.local_clock = 0

    def MsgDelivery(self, request, context):

        # Keep a copy of the requests
        self.recvMsg.append(request)

        balance_result = None
        response_result = None
        
        if request.OP == banking_pb2.QUERY:
            #time.sleep(SLEEP_SECONDS)
            response_result, balance_result = self.Query()
        
        if request.OP == banking_pb2.DEPOSIT:
            response_result, balance_result = self.Deposit(request.Amount)
            #time.sleep(SLEEP_SECONDS)
        
        if request.OP == banking_pb2.WITHDRAW:
            response_result, balance_result = self.Withdraw(request.Amount)
            #time.sleep(SLEEP_SECONDS)

        if request.D_ID == DO_NOT_PROPAGATE:
            CustomerText = 'another Branch'
        else:
            CustomerText = (f'Customer {request.D_ID}')
        ResponseText = (
            f'Branch {self.id} received request ID {request.S_ID} from {CustomerText} - '
            f'Operation: {get_operation_name(request.OP)} - '
            f'Amount: {request.Amount} - '
            f'Result: {get_result_name(response_result)} - '
            f'New balance: {balance_result}'
        )
        MyLog(logger,
            ResponseText
        )

        if (sg != NotImplemented):
            if (self.window != None):
                print(
                    ResponseText
                )
                self.window.Refresh()

        response = banking_pb2.MsgDeliveryResponse(
            ID=request.S_ID,
            RC=response_result,
            Amount=balance_result,
        )
    
        ResponseText = (
            f'Branch {self.id} sent response to request ID {request.S_ID} from {CustomerText} - '
            f'Result: {get_result_name(response_result)} - '
            f'New balance: {balance_result}' 
        )    
        MyLog(logger,
            ResponseText
        )

        if (sg != NotImplemented):
            if (self.window != None):
                print(
                    ResponseText
                )
                self.window.Refresh()

        # If DO_NOT_PROPAGATE it means it has come from another branch and it must not be
        # spread further.  Also, no need to propagate query operations.
        if request.D_ID != DO_NOT_PROPAGATE and request.OP == banking_pb2.DEPOSIT:
            self.Propagate_Deposit(request.D_ID, request.Amount)
        if request.D_ID != DO_NOT_PROPAGATE and request.OP == banking_pb2.WITHDRAW:
            if response_result == banking_pb2.SUCCESS:                              # only propagates if the change has been successful 
                self.Propagate_Withdraw(request.D_ID, request.Amount)
        
        return response

    def Query(self):
        return banking_pb2.SUCCESS, self.balance

    def Deposit(self, amount):
        if amount <= 0:		                            # invalid operation - but returns the balance anyway
            return banking_pb2.ERROR, self.balance
        new_balance = self.balance + amount
        self.balance = new_balance
        return banking_pb2.SUCCESS, new_balance         # success

    def Withdraw(self, amount):
        # Distinguish between error (cannot execute a certain operation) or failure (operation is valid, but for instance
        # there is not enough balance).
        # This distinction is currently unused but can be used for further expansions of functionalities, such as overdraft.
        if amount <= 0:		        # invalid operation
            return banking_pb2.ERROR, 0
        new_balance = self.balance - amount
        if new_balance < 0:	        # not enough money! cannot widthdraw
            return banking_pb2.FAILURE, amount
        self.balance = new_balance
        return banking_pb2.SUCCESS, new_balance

    def Propagate_Deposit(self, request_id, amount):

        for stub in self.branchList:

            if self.id != stub[0]:

                LogMessage = (f'Propagate {get_operation_name(banking_pb2.DEPOSIT)} Request id {request_id} Amount {amount} to Branch #{stub[0]} @{stub[1]}')
                MyLog(logger, LogMessage)
                        
                if (sg != NotImplemented):
                    if (self.window != None):
                        print(LogMessage)
                        self.window.Refresh()

                try:
                    msgStub = banking_pb2_grpc.BankingStub(grpc.insecure_channel(stub[1]))
                    response = msgStub.MsgDelivery(
                        banking_pb2.MsgDeliveryRequest(
                            S_ID=request_id,
                            OP=banking_pb2.DEPOSIT,
                            Amount=amount,
                            D_ID=DO_NOT_PROPAGATE,          # Sets DO_NOT_PROPAGATE for receiving branches
                        )
                    )
                    LogMessage = (f'Branch {self.id} sent request {request_id} to Branch @{stub[1]} - '
                        f'Operation: {get_operation_name(banking_pb2.DEPOSIT)} - Result: {get_result_name(response.RC)} - '
                        f'New balance: {response.Amount}')
                    MyLog(logger, LogMessage)
                    if (sg != NotImplemented):
                        if (self.window != None):
                            print (LogMessage)
                            self.window.Refresh()

                except grpc.RpcError as rpc_error_call:
                    code = rpc_error_call.code()
                    details = rpc_error_call.details()

                    if (code.name == "UNAVAILABLE"):
                        ErrorMessage = (f'Error on Request #{request_id}: Branch #{self.id} likely unavailable - Code: {code} - Details: {details}')
                    else:
                        ErrorMessage = (f'Error on Request #{request_id}: Code: {code} - Details: {details}')

                    MyLog(logger, ErrorMessage)
                    if (sg != NotImplemented):
                        if (self.window != None):
                            print(ErrorMessage)
                            self.window.Refresh()


    def Propagate_Withdraw(self, request_id, amount):
        
        for stub in self.stubList:

            if self.id != stub[0]:

                LogMessage = (f'Propagating {get_operation_name(banking_pb2.WITHDRAW)} Request id {request_id} Amount {amount} to Branch #{stub[0]} @{stub[1]}')
                MyLog(logger, LogMessage)
                        
                if (sg != NotImplemented):
                    if (self.window != None):
                        print(LogMessage)
                        self.window.Refresh()

                try:
                    msgStub = banking_pb2_grpc.BankingStub(grpc.insecure_channel(stub[1]))
                    response = msgStub.MsgDelivery(
                        banking_pb2.MsgDeliveryRequest(
                            S_ID=request_id,
                            OP=banking_pb2.WITHDRAW,
                            Amount=amount,
                            D_ID=DO_NOT_PROPAGATE,          # Sets DO_NOT_PROPAGATE for receiving branches
                        )
                    )

                    LogMessage = (f'Branch {self.id} sent request {request_id} to Branch @{stub[1]} - '
                        f'Operation: {get_operation_name(banking_pb2.WITHDRAW)} - Result: {get_result_name(response.RC)} - '
                        f'New balance: {response.Amount}')
                    MyLog(logger, LogMessage)
                    if (sg != NotImplemented):
                        if (self.window != None):
                            print (LogMessage)
                            self.window.Refresh()

                except grpc.RpcError as rpc_error_call:
                    code = rpc_error_call.code()
                    details = rpc_error_call.details()

                    if (code.name == "UNAVAILABLE"):
                        ErrorMessage = (f'Error on Request #{request_id}: Branch #{self.id} likely unavailable - Code: {code} - Details: {details}')
                    else:
                        ErrorMessage = (f'Error on Request #{request_id}: Code: {code} - Details: {details}')

                    MyLog(logger,
                        ErrorMessage
                    )
                    if (sg != NotImplemented):
                        if (self.window != None):
                            print(ErrorMessage)
                            self.window.Refresh()


    def Populate_Stub_List(self):

        if len(self.stubList) == len(self.branches):  # stub list already initialized
            return

        len_bids = len(branches_addresses_ids)
        for i in range(len_bids):
            bids_id = branches_addresses_ids[i][0]
            if bids_id != self.id:
                MyLog(logger,f'Initializing Branch #{self.id} to Branch #{branches_addresses_ids[i][0]} stub at {branches_addresses_ids [i][1]}')
                self.stubList.append(banking_pb2_grpc.BankingStub(grpc.insecure_channel(branches_addresses_ids [i][1])))



# If PySimpleGUI/TK are installed, launches a window in the Windows' Manager.
# Otherwise, it waits for a day unless CTRL+C is pressed
#
def Wait_Loop(Branch):

    if (sg != NotImplemented):
        
        # Create an event loop
        while True:
            event, values = Branch.window.read()

            # End program if user closes window or
            # presses the Close button
            if event == "Close" or event == sg.WIN_CLOSED:
                break
    else:
        try:
            while True:
                time.sleep(ONE_DAY.total_seconds())
        except KeyboardInterrupt:
            return


# Spawn the Branch process server
#
def Run_Branch(Branch, THREAD_CONCURRENCY):
    """Start a server (branch) in a subprocess."""

    MyLog(logger,f'Initialising branch at {Branch.bind_address}...')

    options = (('grpc.so_reuseport', 1),)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=THREAD_CONCURRENCY,), options=options)

    #Branch.bind_address = binding_address
    banking_pb2_grpc.add_BankingServicer_to_server(Branch, server)

    if (sg != NotImplemented):
        layout = [
            [sg.Text(f"Initial Balance: {Branch.balance}", size=(40,1), justification="left")],
            [sg.Output(size=(90,15))],
            [sg.Button("Close", tooltip='Terminates Branch')]
        ]

        # Create the window
        sg.theme('Dark Blue 3')
        Branch.window = sg.Window(f"Branch #{Branch.id} at Address {Branch.bind_address}"
            , layout
            , location=(900+100*Branch.id, 100*Branch.id)
        )

        Branch.window.refresh()

    server.add_insecure_port(Branch.bind_address)
    server.start()

    if (sg != NotImplemented):
        MyLog(logger,'*** Press CTRL+C to exit the process when finished ***')
    
    Wait_Loop(Branch)

    if (sg != NotImplemented):
        Branch.window.close()

    server.stop(None)


# Utility functions, used for readability
#
def get_operation(operation):
    """Returns the message type from the operation described in the input file."""
    if operation == 'query':
        return banking_pb2.QUERY
    if interface == 'deposit':
        return banking_pb2.DEPOSIT
    if interface == 'withdraw':
        return banking_pb2.WITHDRAW

def get_operation_name(operation):
    """Returns the operation type from the message."""
    if operation == banking_pb2.QUERY:
        return 'QUERY'
    if operation == banking_pb2.DEPOSIT:
        return 'DEPOSIT'
    if operation == banking_pb2.WITHDRAW:
        return 'WITHDRAW'

def get_result_name(name):
    """Return state of a client's operation."""
    if name == banking_pb2.SUCCESS:
        return 'SUCCESS'
    if name == banking_pb2.FAILURE:
        return 'FAILURE'
    if name == banking_pb2.ERROR:
        return 'ERROR'
