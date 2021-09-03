%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Comment {
    const char* id;
    const char* user;
    const char* date;
    const char* commentText;
    const char* likes;
    int numberOfReplies;
    struct Comment* cTreeArr[100];
} *CTree, Comment;

CTree cTree;
CTree cTreeTMP;

int depth = 0;
int flag = 0;
int flag2 = 0;
int cTreePos[100];

void cTreeInserter(CTree*, int*, CTree);
void cTreeInserterAUX(CTree*, int*, int, CTree);
CTree cloneComment(CTree);
CTree createComment();
void setID(CTree, char*);
void setUser(CTree, char*);
void setDate(CTree, char*);
void setCommentText(CTree, char*);
void setLikes(CTree, char*);
int setNumberOfReplies(CTree);
void printComs(CTree, int);
void fillcTreePos(int*);
void indentation(int);
char* replaceWord(const char*, const char*, const char*);

void cTreeInserter(CTree* cTreeLoc, int pos[], CTree cTreeTMP) {
    if(!*cTreeLoc) *cTreeLoc = cloneComment(cTreeTMP);
    else cTreeInserterAUX(cTreeLoc, pos, 1, cTreeTMP);
}

void cTreeInserterAUX(CTree* cTreeLoc, int pos[], int i, CTree cTreeTMP) {
    if (pos[i] == -1) return;
    if (!(*cTreeLoc)->cTreeArr[pos[i]]) {
        (*cTreeLoc)->cTreeArr[pos[i]] = cloneComment(cTreeTMP);
    } else cTreeInserterAUX(&(*cTreeLoc)->cTreeArr[pos[i]], pos, i+1, cTreeTMP);
}

CTree cloneComment(CTree cTreeTMP) {
    CTree cTree = malloc(sizeof(Comment));
    cTree->id = strdup(cTreeTMP->id);
    cTree->user = strdup(cTreeTMP->user);
    cTree->date = strdup(cTreeTMP->date);
    cTree->commentText = strdup(cTreeTMP->commentText);
    cTree->likes = strdup(cTreeTMP->likes);
    cTree->numberOfReplies = cTreeTMP->numberOfReplies;
    return cTree;
}

CTree createComment() {
    CTree cTree = malloc(sizeof(Comment));
    for(int i=0;i<100;i++) cTree->cTreeArr[i] = NULL;
    return cTree;
}

void setID(CTree cTree, char* id) {cTree->id = strdup(id);}
void setUser(CTree cTree, char* user) {cTree->user = strdup(user);}
void setDate(CTree cTree, char* date) {cTree->date = strdup(date);}
void setCommentText(CTree cTree, char* commentText) {cTree->commentText = strdup(commentText);}
void setLikes(CTree cTree, char* likes) {cTree->likes = strdup(likes);}

int setNumberOfReplies(CTree cTree) {
    int numberOfReplies = 0;
    for (int i=0;i<100;i++) {
        if (cTree->cTreeArr[i]) numberOfReplies += setNumberOfReplies(cTree->cTreeArr[i]);
        else break;
    }
    cTree->numberOfReplies = numberOfReplies;
    return numberOfReplies+1;
}

void printComs(CTree cTree, int depth) {

    cTree->commentText = replaceWord(cTree->commentText, "\n", "");
    cTree->commentText = replaceWord(cTree->commentText, "\"", "\\\"");
    cTree->commentText = replaceWord(cTree->commentText, "<b>", "");
    cTree->commentText = replaceWord(cTree->commentText, "</b>", "");
    cTree->commentText = replaceWord(cTree->commentText, "<p>", "");
    cTree->commentText = replaceWord(cTree->commentText, "</p>", "\\n");
    cTree->commentText = replaceWord(cTree->commentText, "<u>", "");
    cTree->commentText = replaceWord(cTree->commentText, "</u>", "");
    cTree->commentText = replaceWord(cTree->commentText, "<i>", "");
    cTree->commentText = replaceWord(cTree->commentText, "</i>", "");
    cTree->commentText = replaceWord(cTree->commentText, "<br>", "");

    indentation(depth+1); printf("\"id\": \"%s\",\n", cTree->id);
    indentation(depth+1); printf("\"user\": \"%s\",\n", cTree->user);
    indentation(depth+1); printf("\"date\": \"%s\",\n", cTree->date);
    indentation(depth+1); printf("\"timestamp\": \"%s\",\n", "NA");
    indentation(depth+1); printf("\"commentText\": \"%s\",\n", cTree->commentText);
    indentation(depth+1); printf("\"likes\": %s,\n", cTree->likes);
    indentation(depth+1); printf("\"hasReplies\": ");
    if (!cTree->numberOfReplies) printf("false,\n"); else printf("true,\n");
    indentation(depth+1); printf("\"numberOfReplies\": %i,\n", cTree->numberOfReplies);
    if (!cTree->numberOfReplies) {
        indentation(depth+1); printf("\"replies\": []\n");
    } else {
        indentation(depth+1); printf("\"replies\": [\n");
        for (int i=0;i<100;i++) {
            if (cTree->cTreeArr[i]) {
                indentation(depth+2); printf("{\n");
                printComs(cTree->cTreeArr[i], depth+2);
                indentation(depth+2); printf("}");
                if (cTree->cTreeArr[i+1] != NULL) printf(",\n");
                else printf("\n");
            } else break;

        }
        indentation(depth+1); printf("]\n");
    }
}

void fillcTreePos(int cTreePos[]) {for (int i=0;i<100;i++) cTreePos[i] = -1;}

void indentation(int n) {for (int i=0;i<n;i++) printf("    ");}

char* replaceWord(const char* s, const char* oldW, const char* newW) {
    char* result;
    int i, cnt = 0;
    int newWlen = strlen(newW);
    int oldWlen = strlen(oldW);
    for (i = 0; s[i] != '\0'; i++) { 
        if (strstr(&s[i], oldW) == &s[i]) { 
            cnt++; 
            i += oldWlen - 1; 
        }
    }
    result = (char*)malloc(i + cnt * (newWlen - oldWlen) + 1);
    i = 0; 
    while (*s) {
        if (strstr(s, oldW) == s) { 
            strcpy(&result[i], newW); 
            i += newWlen; 
            s += oldWlen; 
        } else result[i++] = *s++; 
    }
    result[i] = '\0'; 
    return result; 
} 

%}

START_COMMENT               \<li[' ']class=\"post\"[' ']id=\"post-
ID_RE                       \"\>\<div[' ']role=\"alert\"\>\<\/div\>
END_COMMENT                 Show[' ']more[' ']replies\<\/a\>\n\<\/div\>\n\<\/div\>\n\<\/li\>

START_USERNAME              \<a[' ']data-action=\"profile\"[' ']data-username=\"
END_USERNAME                \"[' ']href

START_DATE                  \<a[' ']class=\"time-ago.+\"\>

START_COMMENT_TEXT          \<div[' ']class=\"post-message\"[' ']data-role=\"message\"[' ']dir=\"auto\"\>\<div\>\<p\>
END_COMMENT_TEXT            \<\/p\>\n\<\/div\>\n<\/div\>

START_LIKES                 data-role=\"likes\"\>

%option stack
%s COMMENT USERNAME DATE CONTENT LIKE

%%

{START_COMMENT} {
    cTreePos[depth++]++;
    cTreeTMP = createComment();
    yy_push_state(COMMENT);
}

<COMMENT>[0-9]{10}/{ID_RE} {
    setID(cTreeTMP, yytext);
}

<COMMENT>{START_USERNAME} {
    flag2 = 1;
    yy_push_state(USERNAME);
}

<USERNAME>.+/{END_USERNAME} {
    setUser(cTreeTMP, yytext);
    yy_pop_state();
}

<COMMENT>{START_DATE} {
    yy_push_state(DATE);
}

<DATE>.+ago {
    setDate(cTreeTMP, yytext);
    yy_pop_state();
}

<COMMENT>{START_COMMENT_TEXT} {
    yy_push_state(CONTENT);
}

<CONTENT>(\<\/[^d]|\<[^\/]|[^\<])*/{END_COMMENT_TEXT} {
    setCommentText(cTreeTMP, yytext);
    yy_pop_state();
}

<COMMENT>{START_LIKES} {
    yy_push_state(LIKE);
}

<LIKE>[0-9]+ {
    setLikes(cTreeTMP, yytext);
    if (flag2 == 0) setUser(cTreeTMP, "Guest"); else flag2 = 0;
    cTreeInserter(&cTree, cTreePos, cTreeTMP);
    free(cTreeTMP);
    yy_pop_state();
}

<COMMENT>{END_COMMENT} {
    cTreePos[depth--] = -1;
    if (!depth) {
        if (flag) printf(",\n"); else flag = 1;
        indentation(2); printf("{\n");
        setNumberOfReplies(cTree);
        printComs(cTree, 2);
        indentation(2); printf("}");
        cTree = NULL;
        fillcTreePos(cTreePos);
        
    }
    yy_pop_state();
}

.|\n { ; }

%%

int yywrap() {
    printf("\n    ]\n}\n");
    return(1);
}

int main(){
    cTree = NULL;
    fillcTreePos(cTreePos);
    printf("{\n    \"commentThread\": [\n");
    yylex(); return 0;
}
