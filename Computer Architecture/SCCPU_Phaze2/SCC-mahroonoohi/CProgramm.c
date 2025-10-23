//structs & C Function
struct INstruction
{
    char instruction[32];
    int PC;
};

char * bin(int ins,int pc)
{
    char * instruction=(char *)malloc(32*sizeof (char));
    for(int i=0;ins>0;i++)
    {
        instruction[i]=ins%2;
        ins=ins/2;
    }
}
