**FREE
ctl-opt nomain;

/include 'commands.RPGLEINC'

//--------------------------------------------------------------------
// Execute a CL Command
//--------------------------------------------------------------------
Dcl-Proc execCommand export;
    Dcl-PI *N;
    End-PI;
    
    Dcl-s commandString  Varchar(32702) CONST;

    monitor;
        qcmdexc( commandString : %len(commandString) );
    on-error;
    endMon;    
    
    Return;

End-Proc;