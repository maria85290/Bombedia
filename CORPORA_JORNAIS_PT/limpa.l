
%option noyywrap


%x postText
%x views
%x likes
%x dislikes


%%
^[ ]*\"socioLingVar\"[ ]*\:[^,]+\,   { printf(" \"socioLingVar\": \"Behavioural Addictions - All\","); }
\’                              { printf("'"); }
\“                              { printf("'"); }
\”                              { printf("'"); }

^[ ]*\"postText\"[ ]*\:[ ]*\"   { ECHO; BEGIN postText; }
<postText>\"\,                  { ECHO; BEGIN INITIAL; }
<postText>\r?\n                 { printf(". "); }
<postText>\“                    { printf("'"); }
<postText>\”                    { printf("'"); }
<postText>\’                    { printf("'"); }
<postText>\"                    { printf("'"); }

^[ ]*\"views\"[ ]*\:[ ]*\"   { ECHO; BEGIN views; }
<views>\"\,                  { ECHO; BEGIN INITIAL; }
<views>[0-9]                 { ECHO; }
<views>.       { printf(""); }

^[ ]*\"likes\"[ ]*\:[ ]*\"   { ECHO; BEGIN likes; }
<likes>\"\,                  { ECHO; BEGIN INITIAL; }
<likes>[0-9|a-zA-Z, ]        { ECHO; }
<likes>.                      { printf(""); }

^[ ]*\"dislikes\"[ ]*\:[ ]*\"   { ECHO; BEGIN dislikes; }
<dislikes>\"\,                  { ECHO; BEGIN INITIAL; }
<dislikes>[0-9|a-zA-Z, ]        { ECHO; }
<dislikes>.                      { printf(""); }





%%

int main(){
   yylex();
   return 0;
}

