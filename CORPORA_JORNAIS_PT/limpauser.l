%option noyywrap

%x postText
%x buscaUser

%%
^[ ]*\{[^"]*\"id\"[ ]*\:.+\n         { ECHO; BEGIN buscaUser; }
<buscaUser>^[ ]*\"user\"[ ]*\: { ECHO; BEGIN INITIAL; }
<buscaUser>^[ ]*\"date\"[ ]*\: { printf("\"user\": \"NULL\",\n"); ECHO; BEGIN INITIAL; }
%%

int main(){
   yylex();
   return 0;
}

