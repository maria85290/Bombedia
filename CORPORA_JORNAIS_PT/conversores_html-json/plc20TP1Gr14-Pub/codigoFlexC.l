%{
/* Declaracoes C diversas */
#include <string.h>
#include <stdio.h>
#include <stdlib.h>



typedef struct commentThread
{
    char *id;
    char *userid;
    char *date;
    char *commentText;
    struct commentThread *prox;
    int count;

}*Comment;




Comment newcomment(int x){

Comment l = malloc(sizeof(struct commentThread));
    l->prox =NULL;
    l->count =x;

    return l;
}   


Comment inicio,*frente;
int numero=0;



%}

%option stack

digit [0-9]
alphanum [0-9a-zA-Z]
id_formatt {alphanum}{8}-{alphanum}{4}-{alphanum}{4}-{alphanum}{4}-{alphanum}{12}
date_formatt {digit}{2}\.{digit}{2}\.{digit}{4}
texto_comentario (.|\n)


com_id_init              data-comment-id=
com_section_init         li[' ']+class=\"comment\"[' ']+
com_section_fim          \<\/li\>

user_info_init           \/utilizador\/perfil\/
user_info_fim            \<\/a\>

com_content_init         \<p\>['\n']*[' ']*(\t)*
com_content_fim          [' ']*(\t)*\<\/p\>

resp_section_init        \<ol[' ']+class=\"comments__list\"
resp_section_fim         \<\/ol\>

date_init                \<a[' ']class=\"comment__permalink\">


com_id_fim               \>


%s COMENTARIO USER TEXTO IDCOMENTARIO DATA

%%

{resp_section_init}         {   numero++;  }
{resp_section_fim}          {   numero--; }



{com_section_init}                      {  yy_push_state(COMENTARIO); frente=&((*frente)->prox); (*frente)=newcomment(numero); }
<COMENTARIO>{com_section_fim}           {  yy_pop_state(); }



<COMENTARIO>{com_id_init}               {  yy_push_state(IDCOMENTARIO);  }
<IDCOMENTARIO>{id_formatt}              {  (*frente)->id =strdup( yytext);  }
<IDCOMENTARIO>{com_id_fim}              {  yy_pop_state(); }


<COMENTARIO>{user_info_init}            {  yy_push_state(USER);  }
<USER>{id_formatt}                      {  (*frente)->userid =strdup( yytext); }
<USER>{user_info_fim}                   {  yy_pop_state(); } 


<COMENTARIO>{date_init}     {  yy_push_state(DATA); }
<DATA>{date_formatt}        {  (*frente)->date =strdup( yytext); }
<DATA>{user_info_fim}       {  yy_pop_state(); }


<COMENTARIO>{com_content_init}          {  yy_push_state(TEXTO); }
<TEXTO>[^\<]*                           {  (*frente)->commentText =strdup( yytext); }
<TEXTO>{com_content_fim}                {  yy_pop_state(); }






(.|\n)                      {;}

%%



int yywrap(){
  return(1);
}


int contarr(Comment x,int n){
  int r=0;
  x=x->prox;
  while( x!=NULL && x->count > n){
    r++;
    x=x->prox;
  }
  return r;
}

void espaco(FILE *f,int n){
  for(int i=1;i<n;i++) fprintf(f,"        ");
}


void displayc(FILE *f,char *a,int x){
  int i=4,j=strlen(a)-1;
  
  while( a[j]==' ' ||  a[j]=='\n' || a[j]=='\t') j--;
  while( a[i]==' ' ||  a[i]=='\n' || a[i]=='\t') i++;

  for(;a[i] && i<j  ;i++){
    if(a[i]=='\n') {fprintf(f,"\n");espaco(f,x);}
    else if(a[i]=='\"') fprintf(f,"\\\"");
    else fprintf(f,"%c",a[i]);
  }
}


void displayR(FILE *f,Comment s,int n){
  int i;

  espaco(f,s->count);
  fprintf(f,"\"id\": \"%s\",\n", s->id);

  espaco(f,s->count);
  fprintf(f,"\"user\": \"%s\",\n", s->userid);

  espaco(f,s->count);
  fprintf(f,"\"date\": \"%s\",\n", s->date);

  espaco(f,s->count);
  fprintf(f,"\"timestamp\": \"NA\",\n");

  espaco(f,s->count);
  fprintf(f,"\"commentText\": \"");
  displayc(f,s->commentText,s->count);
  fprintf(f,"\",\n");

  espaco(f,s->count);
  fprintf(f,"\"likes\": 0,\n");

  int x=contarr(s,s->count);
 
  espaco(f,s->count);
  fprintf(f,"\"hasreplies\": ");

  if(x==0) fprintf(f,"false,\n");
  else fprintf(f,"true,\n");

  espaco(f,s->count);
  fprintf(f,"\"numberOfReplies\":%d,\n",x);

  espaco(f,s->count);
  fprintf(f,"\"replies\": [");
  if(x==0) fprintf(f,"],");
  else fprintf(f,"  {");
  fprintf(f,"\n\n");
}



int main(){
  inicio=newcomment(numero);
  frente=&inicio;
  
  yylex();
  inicio=inicio->prox;
  

  frente=&inicio;
  FILE *f;
  f=fopen("convertidos/out.json","w+");


  fprintf(f,"\n\"commentThread\": [\n");
  fprintf(f,"{\n");

  
  while(*frente!=NULL){

    displayR(f,*frente,(*frente)->count);
    
    if ((*frente)->prox!=NULL) {
      if((*frente)->count > (*frente)->prox->count) {
        fprintf(f,"\n"); 
        espaco(f,(*frente)->count);
        fprintf(f,"} ],\n");
      }
    }
    else {
      numero=(*frente)->count;
      while(numero > 1){
        fprintf(f,"\n"); 
        espaco(f,numero);
        fprintf(f,"}  ]\n");
        numero--;
      }
    }

    frente=&((*frente)->prox);
  
  }
  fprintf(f,"}\n];");
  fclose(f);

  return 0;
}