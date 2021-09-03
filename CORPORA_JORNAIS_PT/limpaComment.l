%option noyywrap

%x postText
%x buscaComment

%%
^[ ]*\{[^"]*\"id\"[ ]*\:.+\n[^"]*\"user\"[ ]*\:.+\n[^"]*\"date\"[ ]*\:.+\n[^"]*\"timestamp\"[ ]*\:.+\n        { ECHO; BEGIN buscaComment; }
<buscaComment>^[ ]*\"commentText\"[ ]*\: { ECHO; BEGIN INITIAL; }
<buscaComment>^[ ]*\"likes\"[ ]*\: { printf("\"commentText\": \"NULL\",\n"); ECHO; BEGIN INITIAL; }
%%

int main(){
   yylex();
   return 0;
}
