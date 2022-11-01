class Exception(object):
    '''Base class for all FlexMusic client errors'''
    
    class ClientException(Exception):
        '''
        Base exception for all FlexMusic errors propagated during client-side request operation\n
        This should not be raised directly.
        '''
        pass

    # Base server exception
    class ServerException(Exception):
        '''
        Base exception for all FlexMusic errors propagated during server-side request operation\n
        This should not be raised directly.
        '''
        pass

    # Base user exception
    class UserException(Exception):
        '''
        Base exception for all FlexMusic errors propagated as a result of user error\n
        This should not be raised directly.
        '''
        pass

    #
    # Client exception declarations
    #

    class NoResultsFound(ClientException):
        '''Raised when a search request returns no results'''
        pass

    #
    # Server exception declarations
    #

    class ServerRaisedError(ServerException):
        '''Raised when a server request fails on the server's end.'''
        pass

    #
    # User eception declaration
    #

    class MissingQuery(UserException):
        '''Raised when a function that requires a query does not receive one'''
        pass

    class MissingURL(UserException):
        '''Raised when a function that requires a URL does not receive one'''
        pass