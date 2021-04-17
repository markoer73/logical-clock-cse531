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
from Util import setup_logger, MyLog, sg, get_operation, get_operation_name, get_result_name

import grpc
import banking_pb2
import banking_pb2_grpc

ONE_DAY = datetime.timedelta(days=1)
logger = setup_logger("Branch")
SLEEP_SECONDS = 3

# A constant used to indicate that the Branch must not propagate an operation. This is because a Branch receiving a message
#   cannot distinguish between an operation is coming from a client or another branch or it has been received already.
#   Without this control, the branches would keep propagating operations in an infinite loop. By setting this value after
#   the first propagation, it is not spread further.
DO_NOT_PROPAGATE = -1       

class Branch(banking_pb2_grpc.BankingServicer):
    """ Branch class definition """

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
        # List of events, including local clocks
        self.events = list()

    def MsgDelivery(self, request, context):
        """ Manages RPC calls coming into a branch from a
            customer or another branch

        Args:
            self:    Branch class
            request: gRPC class (the message)
            context: gRPC context

        Returns:
            MsgDeliveryResponse class (gRPC response object)

        """

        # Keep a copy of the requests
        self.recvMsg.append(request)

        balance_result = None
        response_result = None
        
        if request.D_ID == DO_NOT_PROPAGATE:
            CustomerText = 'another Branch'
        else:
            CustomerText = (f'Customer {request.D_ID}')
        LogMessage = (
            f'[Branch {self.id}] Received request ID {request.REQ_ID} from {CustomerText} - '
            f'Operation: {get_operation_name(request.OP)} - '
            f'Amount: {request.Amount}')
        MyLog(logger, LogMessage, self)
            
        if request.OP == banking_pb2.QUERY:
            response_result, balance_result = self.Query()
        
        if request.OP == banking_pb2.DEPOSIT:
            response_result, balance_result = self.Deposit(request.Amount)
        
        if request.OP == banking_pb2.WITHDRAW:
            response_result, balance_result = self.Withdraw(request.Amount)

        # If necessary, sleeps
        #time.sleep(SLEEP_SECONDS)

        if request.D_ID == DO_NOT_PROPAGATE:
            CustomerText = 'another Branch'
        else:
            CustomerText = (f'Customer {request.D_ID}')
        LogMessage = (
            f'[Branch {self.id}] Operation: {get_operation_name(request.OP)} request ID {request.REQ_ID} - '
            f'Result: {get_result_name(response_result)} - '
            f'New balance: {balance_result}'
        )
        MyLog(logger, LogMessage, self)

        response = banking_pb2.MsgDeliveryResponse(
            ID=request.REQ_ID,
            RC=response_result,
            Amount=balance_result,
            Clock=self.local_clock
        )
    
        LogMessage = (
            f'[Branch {self.id}] Sent response to request ID {request.REQ_ID} back to {CustomerText} - '
            f'Result: {get_result_name(response_result)} - '
            f'New balance: {balance_result}' 
        )
        MyLog(logger, LogMessage, self)

        # If DO_NOT_PROPAGATE it means it has arrived from another branch and it must not be
        # spread further.  Also, thre is no need to propagate query operations, in general.
        # Also, only propagates if the operation has been successful.
        if request.D_ID != DO_NOT_PROPAGATE and response_result == banking_pb2.SUCCESS: 
            if request.OP == banking_pb2.DEPOSIT:
                self.Propagate_Deposit(request.D_ID, request.Amount)
            if request.OP == banking_pb2.WITHDRAW:
                self.Propagate_Withdraw(request.D_ID, request.Amount)
        
        return response

    def Query(self):
        """ Implements the Query interface

        Args:
            Self:   Branch class
        
        Returns: The current Branch balance

        """
        return banking_pb2.SUCCESS, self.balance

    def Deposit(self, amount):
        """ Implements the Deposit interface

        Args:
            Self:   Branch class
            amount: the amount to be added to the balance

        Returns:
            banking_pb2 constant: either SUCCESS, FAILURE, or ERROR
                If the amount added is smaller than zero,
                the operation will return ERROR, otherwise SUCCESS.

            new_balance: The updated Branch balance after the amount has been added.

        """
        if amount <= 0:		                            # invalid operation - but returns the balance anyway
            return banking_pb2.ERROR, self.balance
        new_balance = self.balance + amount
        self.balance = new_balance
        return banking_pb2.SUCCESS, new_balance         # success

    def Withdraw(self, amount):
        """ Implements the Withdraw interface

        Args:
            Self:   Branch class
            amount: the amount to be removed to the balance

        Returns: 
            banking_pb2 constant: either SUCCESS, FAILURE, or ERROR.
                If the amount requested is smaller than zero,
                the operation will return ERROR.
                If the amount requested is bigger than the current balance,
                the operation will return FAILURE, otherwise SUCCESS.

            new_balance: The updated Branch balance after the amount has been withdrawn.
                If the amount requested is bigger than the current balance,
                the operation will fail and the balance returned will be the previous
                balance. 

        """
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
        """ Implements the propagation of the deposit to other branches.

        Args:
            Self:   Branch class
            request_id: the request ID of the event
            amount: the amount to be added to the balance

        Returns: The updated Branch balance after the amount added

        """
        for stub in self.branchList:

            if self.id != stub[0]:

                LogMessage = (
                    f'[Branch {self.id}] Propagate {get_operation_name(banking_pb2.DEPOSIT)} request ID {request_id} '
                    f'amount {amount} with clock {self.local_clock} to Branch {stub[0]} @{stub[1]}')
                MyLog(logger, LogMessage, self)
                        
                try:
                    msgStub = banking_pb2_grpc.BankingStub(grpc.insecure_channel(stub[1]))
                    response = msgStub.MsgDelivery(
                        banking_pb2.MsgDeliveryRequest(
                            REQ_ID=request_id,
                            OP=banking_pb2.DEPOSIT,
                            Amount=amount,
                            D_ID=DO_NOT_PROPAGATE,          # Sets DO_NOT_PROPAGATE for receiving branches
                            Clock=self.local_clock
                        )
                    )
                    LogMessage = (
                        f'[Branch {self.id}] received response to request ID {request_id} to Branch @{stub[1]} - '
                        f'Operation: {get_operation_name(banking_pb2.DEPOSIT)} - Result: {get_result_name(response.RC)} - '
                        f'New balance: {response.Amount} - Clock: {response.Clock}')
                    
                except grpc.RpcError as rpc_error_call:
                    code = rpc_error_call.code()
                    details = rpc_error_call.details()

                    if (code.name == "UNAVAILABLE"):
                        LogMessage = (f'[Branch {self.id}] Error on request ID {request_id}: Branch {stub[0]} @{stub[1]} likely unavailable - Code: {code} - Details: {details}')
                    else:
                        LogMessage = (f'[Branch {self.id}] Error on request ID {request_id}: Code: {code} - Details: {details}')

                MyLog(logger, LogMessage, self)


    def Propagate_Withdraw(self, request_id, amount):
        """ Implements the propagation of the withdraw to other branches.

        Args:
            Self:   Branch class
            request_id: the request ID of the event
            amount: the amount to be withdrawn from the balance

        Returns: The updated Branch balance after the amount withdrawn

        """        
        for stub in self.branchList:

            if self.id != stub[0]:

                LogMessage = (
                    f'[Branch {self.id}] Propagate {get_operation_name(banking_pb2.WITHDRAW)} request ID {request_id} '
                    f'amount {amount} with clock {self.local_clock} to Branch {stub[0]} @{stub[1]}')
                MyLog(logger, LogMessage, self)

                try:
                    msgStub = banking_pb2_grpc.BankingStub(grpc.insecure_channel(stub[1]))
                    response = msgStub.MsgDelivery(
                        banking_pb2.MsgDeliveryRequest(
                            REQ_ID=request_id,
                            OP=banking_pb2.WITHDRAW,
                            Amount=amount,
                            D_ID=DO_NOT_PROPAGATE,          # Sets DO_NOT_PROPAGATE for receiving branches
                            Clock=self.local_clock
                        )
                    )

                    LogMessage = (
                        f'[Branch {self.id}] received response to request ID {request_id} to Branch @{stub[1]} - '
                        f'Operation: {get_operation_name(banking_pb2.WITHDRAW)} - Result: {get_result_name(response.RC)} - '
                        f'New balance: {response.Amount} - Clock: {response.Clock}')

                except grpc.RpcError as rpc_error_call:
                    code = rpc_error_call.code()
                    details = rpc_error_call.details()

                    if (code.name == "UNAVAILABLE"):
                        LogMessage = (f'[Branch {self.id}] Error on request ID {request_id}: Branch {stub[0]} @{stub[1]} likely unavailable - Code: {code} - Details: {details}')
                    else:
                        LogMessage = (f'[Branch {self.id}] Error on request ID {request_id}: Code: {code} - Details: {details}')

                MyLog(logger, LogMessage, self)

    # Not used anymore
    #
    # def Populate_Stub_List(self):
    #
    #     if len(self.stubList) == len(self.branches):  # stub list already initialized
    #         return
    #
    #     len_bids = len(branches_addresses_ids)
    #     for i in range(len_bids):
    #         bids_id = branches_addresses_ids[i][0]
    #         if bids_id != self.id:
    #
    #             LogMessage = (
    #                 f'[Branch {self.id}] Initializing to Branch #{branches_addresses_ids[i][0]} stub at {branches_addresses_ids [i][1]}')
    #             MyLog(logger, LogMessage)
    #             self.stubList.append(banking_pb2_grpc.BankingStub(grpc.insecure_channel(branches_addresses_ids [i][1])))

    def eventReceive(self, passed_clock):
        """ Implementation of sub-interface "eventReceive".            
            This subevent happens when the Branch process receives a request
            from the Customer process. The Branch process selects the larger
            value between the local clock and the remote clock from the message,
            and increments one from the selected value.  
            
        Args:
            self:           Branch class
            passed_clock:   The clock to compare to the local one

        Returns: None

        """
        self.local_clock = max(self.local_clock, passed_clock) + 1

    def eventExecute(self):
        """ Implementation of sub-interface "eventExecute".
            This subevent happens when the Branch process executes the event
            after the subevent “Event Request”. The Branch process increments
            one from its local clock.  

        Args:
            self:           Branch class

        Returns: None

        """
        self.local_clock = self.local_clock + 1

    def propagateSend(self):
        """ Interface to set the clock tick for "propagateSend".
            This subevent happens when the Branch process receives the
            propagation request to its fellow branch processes. The Branch
            process increments one from its local clock.
            
        Returns: None

        """
        self.local_clock = self.local_clock + 1

    def propagateReceive(self, passed_clock):
        """ Implementation of sub-interface "propagateReceive".
            This subevent happens when the Branch receives the propagation request
            from its fellow branches. The Branch process selects the biggest value
            between the local clock and the remote clock from the message, and
            increments one from the selected value.            
            
        Args:
            self:           Branch class
            passed_clock:   The clock to compare to the local one

        Returns: None

        """
        self.local_clock = max(self.local_clock, passed_clock) + 1

    def propagateExecute(self):
        """ Interface to set the clock tick for "propagateExecute".
            This subevent happens when the Branch process executes
            the event after the subevent “Propogate_Request”. The
            Branch process increments one from its local clock.          
            
        Returns: None

        """
        self.local_clock = self.local_clock + 1

    def eventResponse(self):
        """ Interface to set the clock tick for "eventResponse".
            This subevent happens after all the propagation
            responses are returned from the branches. The branch
            returns success - fail back to the Customer process.
            The Branch process increments one from its local clock.

        Returns: None

        """
        self.local_clock = self.local_clock + 1



    # def register_event(self, id_, name, clock):
    #     """ Adds an event to the list of processed events by the branch process

    #     Args:
    #         id_: Event id
    #         name: Event Name
    #         clock: Clock tick

    #     Returns: None

    #     """
    #     self.events.append({'id': id_, 'name': name, 'clock': clock})



def Wait_Loop(Branch):
    """ Implements the main waiting loop for branches.
        If PySimpleGUI/TK are installed, relies on user's interaction on graphical windows.
        Otherwise, it waits for a day unless CTRL+C is pressed.

    Args:
        Self:   Branch class

    Returns: none.
    
    """

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
    """ Boot a server (branch) in a subprocess.
        If PySimpleGUI/TK are installed, launches a window in the Windows' Manager.

    Args:
        Branch:             Branch class
        THREAD_CONCURRENCY: Integer, number of threads concurrency

    Returns: none.
    
    """

    MyLog(logger,f'[Branch {Branch.id}] Initialising @{Branch.bind_address} with local clock {Branch.local_clock}...')

    options = (('grpc.so_reuseport', 1),)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=THREAD_CONCURRENCY,), options=options)

    banking_pb2_grpc.add_BankingServicer_to_server(Branch, server)

    if (sg != NotImplemented):
        layout = [
            [sg.Text(f"Balance: {Branch.balance} - Local Clock: {Branch.local_clock}", size=(40,1), justification="left", key='-WINDOWTEXT-')],
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

    if (sg == NotImplemented):
        MyLog(logger,f'[Branch {Branch.id}] *** Press CTRL+C to exit the process when finished ***')
    
    Wait_Loop(Branch)

    if (sg != NotImplemented):
        Branch.window.close()

    server.stop(None)
    
    MyLog(logger,f'[Branch {Branch.id}] Exiting Successfully.')