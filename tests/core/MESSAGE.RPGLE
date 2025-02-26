**FREE

ctl-opt nomain;

/copy 'APIERROR'
/COPY 'message_h'

//***************************************************************************
//**                                                                       **
//**  msg_send : Emission d'un message programme avec choix du type de     **
//**             message                                                   **
//**                                                                       **
//**  Returns:   La clé du message généré                                  **
//******************************e*********************************************

DCL-PROC msg_send EXPORT;

    DCL-PI *n like(RCVM0300.MsgKey);
        MsgId char(7) const;
        MsgDataIn varchar(32767) const options(*omit:*nopass);
        MsgTypeIn char(10) const options(*nopass);
        MsgFileIn char(10) const options(*nopass);
        MsgLibIn char(10) const options(*nopass);
        CallStackCounterIn bindec(4) const options(*nopass);
    END-PI;

    DCL-S w_lib char(10);
    DCL-S MsgFile char(20) Inz('QCPFMSG   QSYS      ');
    DCL-S MsgData varchar(32767);
    DCL-S MsgKey char(4);
    DCL-S MsgType char(10) Inz('*ESCAPE');
    DCL-S CallStackCounter bindec(4) inz(1);
    Dcl-ds Err_Api likeds(ApiError);
          // Niveau de la pile auquel le message doit être envoyé
    if %parms() >= %parmnum(CallStackCounterIn);
        CallStackCounter = CallStackCounterIn;
    endif;

          //biblio du fichier de message
    if %parms() >= %parmnum(MsgLibIn);
        w_lib = MsgLibIn;
    endif;

          //type de message
    if %parms() >= %parmnum(MsgTypeIn);
        MsgType = MsgTypeIn;
    endif;

          //fichier de message
    if %parms() >= %parmnum(MsgFileIn);
        %subst(MsgFile:1:10) = MsgFileIn;
        if w_lib <> *blanks;
            %subst(MsgFile:11:10) = w_lib;
        else;
            %subst(MsgFile:11:10) = '*LIBL';
        endif;
    endif;

          //données de message
    if %parms() >= %parmnum(MsgDataIn) and %addr(MsgDataIn) <> *Null;
        MsgData = MsgDataIn;
    endif;

    SndPgmMsg( MsgId
              :MsgFile
              :MsgData
              :%Len(%Trimr(MsgData))
              :MsgType
              :'*'
              :CallStackCounter
              :MsgKey
              :Err_Api);
    return msgKey;

END-PROC;                  