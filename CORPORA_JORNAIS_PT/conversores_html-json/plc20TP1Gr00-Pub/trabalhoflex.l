%{
#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
/* Declaracoes C diversas */

int flag=0; 
int reply = 1; 
int isReply;

FILE * fp;

char* openChav = "\t{\n";
char* openChavReply = "\t\t{\n";
char* closeChav = "\t},\n\n";
char* closeChavReply = "\t\t},\n\n";

%}

INIT_ALL            \<ol[^>]+>
END_ALL             \<\/ol\>

INIT_NAME           \<h5[^>]+\> 
END_NAME            \<\/h5\>

INIT_TIME           \<time[^>]+\>
END_TIME            \<\/time\>  

INIT_INFO           \<a[^>]+\> 
END_INFO            \<\/a\>
CHECK_INFO          [^\<]+

INIT_COMM           \<p\>[[:space:]]*
END_COMM            \<\/p\>

INIT_THR            \<li
END_THR             \<\/li\>

INIT_IDE            t\-id\=\"
CHECK_IDE           [^"]+
END_IDE             \"\>

%option stack

%s COMMENT TIME NAME INFO ALL THR IDE

%%

<INITIAL>{INIT_ALL}           { BEGIN ALL ; yy_push_state(ALL) ; fprintf(fp, "\"commentThread\": [\n") ; 
                                reply = 1; isReply = 0;}

<ALL>{INIT_THR}               { yy_push_state(THR); if(isReply == 1){ fprintf(fp,"%s", openChavReply); } 
                                else {fprintf(fp, "%s", openChav); } ; reply++ ; }

<ALL>{END_ALL}                { BEGIN ALL ; fprintf(fp, "\t]\n") ; reply-- ; if(isReply != 0){ 
                                fprintf(fp, "\t\"numberOfReplies\": %d,\n\t%s",reply,closeChav) ;  }  
                                    isReply = 0 ; reply = 1 ; }

<THR>{INIT_NAME}              { yy_push_state(NAME) ; }
<NAME>{INIT_INFO}             { yy_push_state(INFO) ; flag = 0 ; }
<NAME>{END_NAME}              { yy_pop_state(); }
<THR>{INIT_TIME}              { yy_push_state(TIME) ; }
<TIME>{INIT_INFO}             { yy_push_state(INFO) ; flag = 1 ; }
<TIME>{END_TIME}              { yy_pop_state(); }
<THR>{INIT_COMM}              { yy_push_state(COMMENT) ; flag = 2 ; }

<COMMENT>{CHECK_INFO}         { if(isReply == 1){ fprintf(fp,"\t\t\"commentText\": \"%s\",\n\t\t\"likes\": NA,\n", yytext); } 
                                else {fprintf(fp, "\t\"commentText\": \"%s\",\n\t\"likes\": NA,\n", yytext); }}

<COMMENT>{END_COMM}           { yy_pop_state() ; }

<THR>{INIT_IDE}               { yy_push_state(IDE) ; }

<IDE>{CHECK_IDE}              { if(isReply == 1){ fprintf(fp,"\t\t\"id\": \"%s\",\n", yytext); } 
                                else {fprintf(fp, "\t\"id\": \"%s\",\n", yytext); }}

<IDE>{END_IDE}                { yy_pop_state();}

<THR>{END_THR}                { yy_pop_state(); if(isReply == 1){ fprintf(fp,"%s", closeChavReply); } 
                                else {fprintf(fp, "\t\"hasReplies\": false,\n\t\"replies\": [],\n\t\"numberOfReplies\": 0,\n %s", 
                                    closeChav);  } ;}

<THR>{INIT_ALL}               { yy_push_state(ALL); fprintf(fp, "\t\"hasReplies\": true,\n") ; 
                                fprintf(fp, "\t\"replies\": [\n") ; isReply = 1; reply = 1; }
             
<INFO>{CHECK_INFO}            {if(flag == 0) { if(isReply == 1){ fprintf(fp,"\t\t\"user\": \"%s\",\n", yytext); } 
                                else {fprintf(fp, "\t\"user\": \"%s\",\n", yytext); }}
                                else{if(flag == 1){ if(isReply == 1){ 
                                        fprintf(fp,"\t\t\"date\": \"%s\",\n\t\t\"timestamp\": NA,\n", yytext); } 
                                        else {fprintf(fp, "\t\"date\": \"%s\",\n\t\"timestamp\": NA,\n", yytext); }}}}

<INFO>{END_INFO}              {  yy_pop_state(); }

.|\n                          {;}

%%
int yywrap(){ 
    return(1); 
}

int main(){

    fp = fopen("out.json", "w");
    
    yylex(); 
    return 0; 
}