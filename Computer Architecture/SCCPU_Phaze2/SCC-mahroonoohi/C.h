#ifndef C_H
#define C_H
#include<stdio.h>
#include<stdlib.h>
#include<QString>
//structs & C Function
struct INstruction
{
    int rs,rd,rt,imm;
    QString instruction,OPcode; // decimal in fetch
    int PC;
    //show for graphic
    bool  Use=false;
    int Step[5];
};
int GETInsInDecimal4(QString bin)
{
    int address[4];
    int result = 0;
    for (int i =3; i > -1; --i) {
        if (bin[i] == '1')
            address[i]=1;
        else
            address[i]=0;
    }
    for (int i =3; i > -1; --i) {
        if (address[i] == 1)
            result  += pow(2,3-i);
    }
    return result;
}
int GETInsInDecimal16(QString bin)
{
    int address[16];
    int result = 0;
    for (int i =15; i > -1; --i) {
        if (bin[i] == '1')
            address[i]=1;
        else
            address[i]=0;
    }
    for (int i =15; i > -1; --i) {
        if (address[i] == 1)
            result  += pow(2,16-i);
    }
    return result;
}
int GETInsInDecimal32(QString bin)
{
    int address[32];
    int result = 0;
    for (int i =31; i > -1; --i) {
        if (bin[i] == '1')
            address[i]=1;
        else
            address[i]=0;
    }
    for (int i =31; i > -1; --i) {
        if (address[i] == 1)
            result  += pow(2,31-i);
    }
    return result;
}
char * bin(int ins)
{
    int i,save=ins;
    char * instruction=(char *)malloc(32*sizeof (char));
    for(i=0;ins>0;i++)
    {
        instruction[i]=ins%2;
        instruction[i]=instruction[i]+48;
        ins=ins/2;
    }
    if(save>0)
        for(int c=i;c<32;c++)
        {
            instruction[c]=0;
            instruction[c]=instruction[c]+48;
            i++;
        }
    else
        for(int c=i;c<32;c++)
        {
            instruction[c]=1;
            instruction[c]=instruction[c]+48;
            i++;
        }
    return instruction;
}
#endif // C_H
