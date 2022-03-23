SUM        START      0
FIRST      LDX        #0                LOAD X REGISTER WITH 0
           LDA        #0                LOAD ACCUMULATOR WITH 0
LOOP       ADD        TABLE, X
           ADD        TABLE2, X
           TIX        COUNT
           JLT        LOOP
           RSUB                         RETURN TO CALLER
           LDA        C'EOFHYT'
           LDA        X'0512'
.
. This is a comment
.
           LDA        C'EOFJH'
           LDA        X'0512'
           LDA        X'0512'
COUNT      RESB       1
TABLE      RESW       2000              2000-WORD TABLE AREA
TABLE2     RESW       2000              2000-WORD TABLE2 AREA
TOTAL      RESW       1
           END        FIRST