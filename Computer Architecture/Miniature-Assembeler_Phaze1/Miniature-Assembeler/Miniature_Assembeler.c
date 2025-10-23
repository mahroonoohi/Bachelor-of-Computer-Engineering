#include<stdio.h>
#include<stdlib.h>
#include "Miniature.h"
int ISLABLE(const char* ch) {
	if (isalpha(*ch) || 65 <= *ch && *ch <= 90 || 97 <= *ch && *ch <= 122)
		return  1;
	else
		return -1;
}
void CREATTABLE(struct  SymbolTable* ptri, int NumberLable, int* addresslable)
{
	char str[7], counter = 0, count = 0;
	for (int i = 0; i < NumberLable; i++)
	{
		while (code[addresslable[i]][count] != '\t' && code[addresslable[i]][count] != ' ')
		{
			counter++;
			count++;
		}
		memcpy(str, code[addresslable[i]], counter);
		if (counter < 7)
			str[counter] = '\0';
		ptri[i].ADDRESS = addresslable[i];
		memcpy(ptri[i].LABLE, str, counter);
		if (counter < 7)
			ptri[i].LABLE[counter] = '\0';
		counter = 0; count = 0;
	}
}
void PRINTTABLE(struct SymbolTable* ptrr, int NumberLable)
{
	printf("Table are as fallows: \n");
	for (int i = 0; i < NumberLable; i++)
	{
		printf("\t"); printf("%s", ptrr[i].LABLE); printf("\t");
		printf("%d", ptrr[i].ADDRESS); printf("%s", " \n");
	}
}
int GETInsInDecimal(int addres[32]) {
	int result = 0;
	for (int i = 31; i > -1; --i) {
		if (addres[i] == 1)
			result |= (1 << i);
	}
	return result;
}
int TYPE(const char* INSTRUC)
{
	int i = 0;
	for (int j = 0; j < 15; j++)
	{
		if (strcmp(INSTRUCTIONS[j], INSTRUC) == 0)
		{
			i = j;
			if (i == 0 || i == 1 || i == 2 || i == 3 || i == 4)
				return 0;
			else if (i == 5 || i == 6 || i == 7 || i == 8 || i == 9 || i == 10 || i == 11 || i == 12)
				return 1;
			else if (i == 13 || i == 14)
				return 2;
		}
	}
	return -1;
}
int TYPEi(const char* INSTRUC)
{
	int i = 0;
	for (int j = 0; j < 15; j++)
	{
		if (strcmp(INSTRUCTIONS[j], INSTRUC) == 0)
		{
			i = j;
			if (i == 0 || i == 1 || i == 2 || i == 3 || i == 4 || i == 5 || i == 6 || i == 7 || i == 8 || i == 9 || i == 10 || i == 11 || i == 12 || i == 13 || i == 14)
				return i;
		}
	}
	return -1;
}
void SETINSTRUCTIONi(struct INSTRUCTION* iset, int offset, int rs, int rt, int opcode)
{
	int binaryoffset[16], counter = 0;
	int i = 0;
	while (offset > 0)
	{
		binaryoffset[i] = offset % 2;
		offset = offset / 2;
		i++;
	}
	for (int j = i; j < 16; j++)
		binaryoffset[j] = 0;
	for (int i = 0; i < 16; i++)
	{
		iset->ADDRESS[i] = binaryoffset[counter];
		counter++;
	}
	//rt
	int binrt[4]; i = 0;
	while (rt > 0)
	{
		binrt[i] = rt % 2;
		rt = rt / 2;
		i++;
	}
	for (int j = i; j < 4; j++)
		binrt[j] = 0;
	counter = 0;
	for (int i = 16; i < 20; i++)
	{
		iset->ADDRESS[i] = binrt[counter];
		counter++;
	}
	//rs
	int binrs[4]; i = 0;
	while (rs > 0)
	{
		binrs[i] = rs % 2;
		rs = rs / 2;
		i++;
	}
	for (int j = i; j < 4; j++)
		binrs[j] = 0;
	counter = 0;
	for (int i = 20; i < 24; i++)
	{
		iset->ADDRESS[i] = binrs[counter];
		counter++;
	}
	//opcode
	int binop[4]; i = 0;
	while (opcode > 0)
	{
		binop[i] = opcode % 2;
		opcode = opcode / 2;
		i++;
	}
	for (int j = i; j < 4; j++)
		binop[j] = 0;
	counter = 0;
	for (int i = 24; i < 28; i++)
	{
		iset->ADDRESS[i] = binop[counter];
		counter++;
	}
	iset->ADDRESS[28] = 0; iset->ADDRESS[29] = 0; iset->ADDRESS[30] = 0; iset->ADDRESS[31] = 0;
}
void SETINSTRUCTIONj(struct INSTRUCTION* jset, int offset, int opcode)
{
	int binaryoffset[16], counter = 0;
	int i = 0;
	while (offset > 0)
	{
		binaryoffset[i] = offset % 2;
		offset = offset / 2;
		i++;
	}
	for (int j = i; j < 16; j++)
		binaryoffset[j] = 0;
	for (int i = 0; i < 16; i++)
	{
		jset->ADDRESS[i] = binaryoffset[counter];
		counter++;
	}
	//UNKONWN
	int Unknown[8];
	for (int i = 16; i < 24; i++)
		jset->ADDRESS[i] = 0;
	//opcode
	int binop[4]; i = 0;
	while (opcode > 0)
	{
		binop[i] = opcode % 2;
		opcode = opcode / 2;
		i++;
	}
	for (int j = i; j < 4; j++)
		binop[j] = 0;
	counter = 0;
	for (int i = 24; i < 28; i++)
	{
		jset->ADDRESS[i] = binop[counter];
		counter++;
	}
	//UNKONWN4
	int Unkown4[4];
	for (int i = 28; i < 32; i++)
		jset->ADDRESS[i] = 0;
}
void SETINSTRUCTIONR(struct INSTRUCTION* Rset, int rd, int rs, int rt, int opcode)
{
	for (int i = 0; i < 12; i++)
		Rset->ADDRESS[i] = 0;
	//rd
	int binrd[4]; int i = 0;
	while (rd > 0)
	{
		binrd[i] = rd % 2;
		rd = rd / 2;
		i++;
	}
	for (int j = i; j < 4; j++)
		binrd[j] = 0;
	counter = 0;
	for (int i = 12; i < 16; i++)
	{
		Rset->ADDRESS[i] = binrd[counter];
		counter++;
	}
	//rt
	int binrt[4]; i = 0;
	while (rt > 0)
	{
		binrt[i] = rt % 2;
		rt = rt / 2;
		i++;
	}
	for (int j = i; j < 4; j++)
		binrt[j] = 0;
	counter = 0;
	for (int i = 16; i < 20; i++)
	{
		Rset->ADDRESS[i] = binrt[counter];
		counter++;
	}
	//rs
	int binrs[4]; i = 0;
	while (rs > 0)
	{
		binrs[i] = rs % 2;
		rs = rs / 2;
		i++;
	}
	for (int j = i; j < 4; j++)
		binrs[j] = 0;
	counter = 0;
	for (int i = 20; i < 24; i++)
	{
		Rset->ADDRESS[i] = binrs[counter];
		counter++;
	}
	//opcode
	int binop[4]; i = 0;
	while (opcode > 0)
	{
		binop[i] = opcode % 2;
		opcode = opcode / 2;
		i++;
	}
	for (int j = i; j < 4; j++)
		binop[j] = 0;
	counter = 0;
	for (int i = 24; i < 28; i++)
	{
		Rset->ADDRESS[i] = binop[counter];
		counter++;
	}
	Rset->ADDRESS[28] = 0; Rset->ADDRESS[29] = 0; Rset->ADDRESS[30] = 0; Rset->ADDRESS[31] = 0;
}
void main(int argc, char** argv) {
	FILE* assp, * machp, * fopen();
	if (argc < 3) {
		printf("***** Please run this program as follows:\n");
		printf("***** %s assprog.as machprog.m\n", argv[0]);
		printf("***** where assprog.as is your assembly program\n");
		printf("***** and machprog.m will be your machine code.\n");
		exit(1);
	}
	if ((assp = fopen(argv[1], "r")) == NULL) {
		printf("%s cannot be openned\n", argv[1]);
		exit(1);
	}
	if ((machp = fopen(argv[2], "w+")) == NULL) {
		printf("%s cannot be openned\n", argv[2]);
		exit(1);
	}
	//assp = fopen("test2.as", "r");
	while (!feof(assp)) {
		fgets(code[Codeline], MAXLEN, (FILE*)assp);
		int Result = ISLABLE(code[Codeline]);
		if (Result == 1)
		{
			NumberLable++;
			addresslable[counter] = Codeline;
			counter++;
		}
		Codeline++;
	}
	//machp = fopen("test2.mc", "w");
	struct SymbolTable* ptr = NULL;
	ptr = (struct SymbolTable*)malloc(NumberLable * sizeof(struct  SymbolTable));
	CREATTABLE(ptr, NumberLable, addresslable);
	PRINTTABLE(ptr, NumberLable);
	for (int i = 0; i < Codeline; i++)
	{
		int j = 0, counter = 0, count = 0; int numberofwords = 0, numbercounter = 0;
		char INS[6];
		int Result = ISLABLE(code[i]);
		if (Result == -1)   //is not lable so it is instruction 
		{
			while (code[i][j] != '\0' &&code[i][j] != '\n' && code[i][j] != '#')
			{
				if (isalpha(code[i][j]))
				{
					INS[count] = code[i][j];
					count++;
					counter = 1;
				}
				if (counter == 1 && (code[i][j] == ' ' || code[i][j] == "  " || code[i][j] == "   " || code[i][j] == "    " || code[i][j] == "     " || code[i][j] == "      " || code[i][j] == "       " || code[i][j] == '\t'))
				{
					numbercounter = j;
					break;
				}
				j++;
			}
			INS[count] = '\0';
			int result = TYPE(INS);
			if (result == -1)
			{
				printf("INSTRUCTION IS NOT FOUND THERE IS NO OPCODE FOR THIS\n");
				exit(1);
			}
			if (result == 0)
			{
				struct INSTRUCTION* INStwo = NULL; int Tcounter = 0, pc1 = 0, pc2 = 0, pc3 = 0, rsthwo, rdthwo, rtthwo; char rs[50], rt[50], rd[50];
				INStwo = (struct INSTRUCTION*)malloc(1 * sizeof(struct INSTRUCTION));
				INStwo->NAME = (char*)malloc((count + 1) * sizeof(char));
				memcpy(INStwo->NAME, INS, count + 1);
				INStwo->NAME[count + 1] = '\0';
				while (code[i][numbercounter + 1] != '\0' && code[i][numbercounter + 1] != '\n')
				{
					if (isdigit(code[i][numbercounter + 1]) && Tcounter == 0)
					{
						rd[pc1] = code[i][numbercounter + 1];
						pc1++;
					}
					else if (isdigit(code[i][numbercounter + 1]) && Tcounter == 1)
					{
						rs[pc2] = code[i][numbercounter + 1];
						pc2++;
					}
					else if (isdigit(code[i][numbercounter + 1]) && Tcounter == 2)
					{
						rt[pc3] = code[i][numbercounter + 1];
						pc3++;
					}
					else if (code[i][numbercounter + 1] == ',')
						Tcounter++;
					numbercounter++;
				}
				rd[pc1] = '\0'; rs[pc2] = '\0'; rt[pc3] = '\0';
				rsthwo = atoi(rs);
				rdthwo = atoi(rd);
				rtthwo = atoi(rt);
				int opcode = TYPEi(INStwo->NAME);
				SETINSTRUCTIONR(INStwo, rdthwo, rsthwo, rtthwo, opcode);
				int result = GETInsInDecimal(INStwo->ADDRESS);
				printf("%d", result);
				printf("\n");
				fprintf(machp, "%d\n", result);
			}
			else if (result == 1)
			{
				struct INSTRUCTION* INSone = NULL; char rt[50], rs[50], offset[50]; int Tcounter = 0, check = 0, offsett, rtone, rsone, opcode, pc1 = 0, pc2 = 0, pc3 = 0;
				INSone = (struct INSTRUCTION_I*)malloc(1 * sizeof(struct INSTRUCTION));
				INSone->NAME = (char*)malloc((count + 1) * sizeof(char));
				memcpy(INSone->NAME, INS, count);
				INSone->NAME[count] = '\0';
				while (code[i][numbercounter + 1] != '\0' && code[i][numbercounter + 1] != '\n')
				{
					if (isdigit(code[i][numbercounter + 1]) && Tcounter == 0)
					{
						rt[pc1] = code[i][numbercounter + 1];
						pc1++;
					}
					else if (isdigit(code[i][numbercounter + 1]) && Tcounter == 1)
					{
						rs[pc2] = code[i][numbercounter + 1];
						pc2++;
					}
					else if (isdigit(code[i][numbercounter + 1]) && Tcounter == 2)
					{
						offset[numberofwords] = code[i][numbercounter + 1];
						numberofwords++;
					}
					else if (code[i][numbercounter + 1] == ',')
						Tcounter++;
					else if (isalpha(code[i][numbercounter + 1]))
					{
						offset[numberofwords] = code[i][numbercounter + 1];
						numberofwords++;
						check = 1;
					}
					else if (code[i][numbercounter + 1] == '\t'||code[i][numbercounter+1]==' '&&Tcounter==2)
						break;
					numbercounter++;
				}
				offset[numberofwords] = '\0'; rs[pc2] = '\0'; rt[pc1] = '\0';
				if (check == 1 && isalpha(offset[0]))  //islable
				{
					check = 0;
					if (strcmp(INSone->NAME, "beq") == 0) //beq
					{
						for (int k = 0; k < NumberLable; k++)
						{
							if (strcmp(ptr[k].LABLE, offset) == 0)
							{
								if (ptr[k].access == 1)
								{
									printf("THE LABLE IS USED FOR MANY TIMES\n");
									exit(1);
								}
								else
								{
									offsett = (ptr[k].ADDRESS) - i - 1;
									check = 1;
									ptr[k].access = 1;
									break;
								}
							}
						}
						if (check == 0)
						{
							printf("OFFSET IS BIGGER THAN 16 BITS \n");
							exit(1);
						}
						rtone = atoi(rt);
						rsone = atoi(rs);
						opcode = TYPEi(INS);
						INSone->OP = opcode;
						INSone->RS = rsone;
						INSone->RT = rtone;
						INSone->OFFSET = offsett;
						SETINSTRUCTIONi(INSone, offsett, rtone, rsone, opcode);
						//printf_s("%d",INSone->ADDRESS);
						int re = GETInsInDecimal(INSone->ADDRESS);
						printf("%d", re);
						printf("\n");
						fprintf(machp, "%d\n", re);
						continue;
					}
					else
					{
						for (int r = 0; r < NumberLable; r++)
						{
							if (strcmp(ptr[r].LABLE, offset) == 0)
							{
								if (ptr[r].access == 1)
								{
									printf("THE LABLE IS USED FOR MANY TIMES\n");
									exit(1);
								}
								else
								{
									offsett = ptr[r].ADDRESS;
									check = 1;
									ptr[r].access = 1;
									break;
								}
							}
						}
					}
					if (check == 0)
					{
						printf("LABLE IS NOT DEFIENED");
						exit(1);
					}
				}
				else
				{
					if ((atoi(offset)) > 65536)
					{
						printf("OFFSET IS BIGGER THAN 16 BITS \n");
						exit(1);
				    }
					if (strcmp(INSone->NAME, "lui") == 0)  //lui
					{
						int imm = atoi(offset);
						rsone = 0;
						rtone = atoi(rt);
						opcode = TYPEi(INS);
						INSone->OP = opcode;
						INSone->RS = rsone;
						INSone->RT = rtone;
						INSone->OFFSET = offsett;
						SETINSTRUCTIONi(INSone, imm, rsone, rtone, opcode);
						int re = GETInsInDecimal(INSone->ADDRESS);
						printf("%d", re);
						printf("\n");
						fprintf(machp, "%d\n", re);
						continue;
					}
					else if (strcmp(INSone->NAME, "jalr") == 0)
					{
						rtone = atoi(rt);
						rsone = atoi(rs);
						opcode = TYPEi(INS);
						INSone->OP = opcode;
						INSone->RS = rsone;
						INSone->RT = rtone;
						SETINSTRUCTIONi(INSone, 0, rsone, rtone, opcode);
						int re = GETInsInDecimal(INSone->ADDRESS);
						printf("%d", re);
						printf("\n");
						fprintf(machp, "%d\n", re);
						continue;
					}
					else
						offsett = atoi(offset);
				}
				rtone = atoi(rt);
				rsone = atoi(rs);
				opcode = TYPEi(INS);
				INSone->OP = opcode;
				INSone->RS = rsone;
				INSone->RT = rtone;
				INSone->OFFSET = offsett;
				SETINSTRUCTIONi(INSone, offsett, rsone, rtone, opcode);
				//printf_s("%d",INSone->ADDRESS);
				int re = GETInsInDecimal(INSone->ADDRESS);
				printf("%d", re);
				printf("\n");
				fprintf(machp, "%d\n", re);
			}
			else if (result == 2)
			{
				struct INSTRUCTION* INSthree = NULL; char offset[10]; int Tcount = 0, opcodee = 0, countoffset = 0, checkthree = 0;
				INSthree = (struct INSTRUCTION_J*)malloc(1 * sizeof(struct INSTRUCTION));
				INSthree->NAME = (char*)malloc((counter) * sizeof(char));
				memcpy(INSthree->NAME, INS, counter);
				INSthree->NAME[counter] = '\0';
				if (strcmp(INSthree->NAME, "j") == 0)
				{
					while (code[i][numbercounter + 1] != '\0' && code[i][numbercounter + 1] != '\n')
					{
						if (isdigit(code[i][numbercounter + 1]) || isalpha(code[i][numbercounter + 1]) || code[i][numbercounter + 1] == '-')
						{
							offset[Tcount] = code[i][numbercounter + 1];
							Tcount++;
						}
						numbercounter++;
					}
					offset[Tcount] = '\0';
					opcodee = 13;
					if (isalpha(offset[0]) && offset != '-') // so it is lable 
					{
						for (int i = 0; i < NumberLable; i++)
						{
							if (strcmp(ptr[i].LABLE, offset) == 0)
							{
								if (ptr[i].access == 1)
								{
									printf("THE LABLE IS USED FOR MANY TIMES\n");
									exit(1);
								}
								else
								{
									countoffset = ptr[i].ADDRESS;
									checkthree = 1;
									SETINSTRUCTIONj(INSthree, countoffset, opcodee);
									int result = (GETInsInDecimal(INSthree->ADDRESS));
									printf("%d", result);
									printf("\n");
									fprintf(machp, "%d\n", result);
									ptr[i].access = 1;
									break;
								}
							}
							else if (strcmp(offset, "halt") == 0)
							{
								countoffset = 14;
								SETINSTRUCTIONj(INSthree, countoffset, opcodee);
								int result = GETInsInDecimal(INSthree->ADDRESS);
								printf("%d", result);
								printf("\n");
								fprintf(machp, "%d\n", result);
								continue;
							}
						}
						if (!checkthree)
						{
							printf("LABLE IS NOT DEFIENED");
							exit(1);
						}

					}
					else
					{
						countoffset = atoi(offset);
						if (countoffset < 0)
						{
							countoffset * -1;
						}
						SETINSTRUCTIONj(INSthree, countoffset, opcodee);
						int result = (GETInsInDecimal(INSthree->ADDRESS));
						printf("%d", result);
						printf("\n");
						fprintf(machp, "%d\n", result);
					}
				}
				else if (strcmp(INSthree->NAME, "halt") == 0)
				{
					int opcode = 14;
					for (int p = 0; p < 24; p++)
						INSthree->ADDRESS[p] = 0;
					int binop[4], s = 0;
					while (opcode > 0)
					{
						binop[s] = opcode % 2;
						opcode = opcode / 2;
						s++;
					}
					for (int j = i; j < 4; j++)
						binop[j] = 0;
					counter = 0;
					for (int r = 24; r < 28; r++)
					{
						INSthree->ADDRESS[r] = binop[counter];
						counter++;
					}
					for (int q = 28; q < 32; q++)
					{
						INSthree->ADDRESS[q] = 0;
					}
					int result = (GETInsInDecimal(INSthree->ADDRESS));
					printf("%d", result);
					printf("\n");
					fprintf(machp, "%d\n", result);
				}
			}
		}
		else
		{
			int j = 0, Tcounter = 0, Mcounter = 0, Pcounter = 0, Ocounter = 0, check = 0, Kcounter = 0; char lable[7], secendstr[50], threestr[50]; int mnumber = 0;
			while (code[i] != '\0' && code[i] != '\n')
			{
				if (isalpha(code[i][j]) || isdigit(code[i][j]))
				{
					lable[Mcounter] = code[i][j];
					Mcounter++;
				}
				if (code[i][j] == ' ' || code[i][j] == " " || code[i][j] == "  " || code[i][j] == "   " || code[i][j] == "    " || code[i][j] == "     " || code[i][j] == "      " || code[i][j] == "       " || code[i][j] == '\t')
				{
					lable[Mcounter] = '\0';
					Tcounter = j;
					break;
				}
				j++;
			}
			while (code[i][j] != '\0' && code[i][j] != '\n')
			{
				if (isalpha(code[i][j]) || code[i][j] == '.')
				{
					secendstr[Pcounter] = code[i][j];
					Pcounter++;
					mnumber = 1;
				}
				if (mnumber == 1 && (code[i][j] == ' ' || code[i][j] == " " || code[i][j] == "  " || code[i][j] == "   " || code[i][j] == "    " || code[i][j] == "     " || code[i][j] == "      " || code[i][j] == "       " || code[i][j] == '\t' || code[i][j] == '\n'))
				{
					secendstr[Pcounter] = '\0';
					Ocounter = j;
					break;
				}
				j++;
			}
			secendstr[Pcounter] = '\0';
			if (strcmp(secendstr, ".fill") == 0) // it is directive 
			{
				Ocounter = 0; int qnumber = 0;
				while (code[i][j] != '\0' && code[i][j] != '\n' && code[i][j] != '#')
				{
					if (isalpha(code[i][j]) || isdigit(code[i][j]) || code[i][j] == '-')
					{
						threestr[Ocounter] = code[i][j];
						Ocounter++; qnumber = 1;
					}
					if (qnumber == 1 && (code[i][j] == ' ' || code[i][j] == " " || code[i][j] == "  " || code[i][j] == "   " || code[i][j] == "    " || code[i][j] == "     " || code[i][j] == "      " || code[i][j] == "       " || code[i][j] == '\t' || code[i][j] == '\n' || code[i][j] == '\0'))
						break;
					j++;
				}
				threestr[Ocounter] = '\0';
				if (isalpha(threestr[0])) // so it is lable 
				{
					for (int i = 0; i < NumberLable; i++)
					{
						if (strcmp(ptr[i].LABLE, threestr) == 0)
						{
								int result = ptr[i].ADDRESS;
								printf("%d", result);
								printf("\n");
								fprintf(machp, "%d\n", result);
								check = 1;
								ptr[i].access = 1;
								break;
						}
					}
					if (!check)
					{
						printf("LABLE IS NOT DEFIENED\n");
						exit(1);
					}
				}
				else if (threestr[0] == '-' || isdigit(threestr[0]))// so it is number  in the directive
				{
					int re = atoi(threestr);
					if (re > 65536)
					{
						printf("OFFSET IS BIGGER THAN 16 BITS \n");
						exit(1);
					}
					printf("%d", re); printf("\n");
					fprintf(machp, "%d\n", re);
				}
			}
			else  //so it is instruction 
			{
				int resu = TYPE(secendstr);
				if (resu==-1)
				{
					printf("INSTRUCTION IS NOT FOUND THERE IS NO OPCODE FOR THIS\n");
					exit(1);
				}
				if (resu == 0)
				{
					struct INSTRUCTION* INStwo = NULL; int Tcounter = 0, check = 0, rsthwo, rdthwo, rtthwo, pc1 = 0, pc2 = 0, pc3 = 0; char rs[50], rt[50], rd[50];
					INStwo = (struct INSTRUCTION*)malloc(1 * sizeof(struct INSTRUCTION));
					INStwo->NAME = (char*)malloc((Pcounter) * sizeof(char));
					memcpy(INStwo->NAME, secendstr, Pcounter);
					INStwo->NAME[Pcounter] = '\0'; j = j++;
					while (code[i][j] != '\0' && code[i][j] != '\n' && code[i][j] != '#')
					{
						if (isdigit(code[i][j]) && Tcounter == 0)
						{
							rd[pc1] = code[i][j];
							pc1++;
						}
						else if (isdigit(code[i][j]) && Tcounter == 1)
						{
							rs[pc2] = code[i][j];
							pc2++;
						}
						else if (isdigit(code[i][j]) && Tcounter == 2)
						{
							rt[pc3] = code[i][j];
							pc3++;
						}
						else if (code[i][j] == ',')
							Tcounter++;
						if (code[i][j] == ' ' || code[i][j] == "  " || code[i][j] == "   " || code[i][j] == "    " || code[i][j] == "     " || code[i][j] == "      " || code[i][j] == "       " || code[i][j] == '\t')
							break;
						j++;
					}
					int opcode = TYPEi(secendstr);
					rt[pc3] = '\0'; 
					rs[pc2] = '\0'; 
					rd[pc1] = '\0';
					rsthwo = atoi(rs);
					rdthwo = atoi(rd);
					rtthwo = atoi(rt);
					SETINSTRUCTIONR(INStwo, rdthwo, rsthwo, rtthwo, opcode);
					int result = GETInsInDecimal(INStwo->ADDRESS);
					printf("%d", result);
					printf("\n");
					fprintf(machp, "%d\n", result);
				}
				else if (resu == 1)
				{
					struct INSTRUCTION* INSone = NULL; char rt[50], rs[50]; char offset[50]; int Tcounter = 0, check = 0, pc1 = 0, pc2 = 0, pc3 = 0, offsett, rtone, rsone, opcode;
					INSone = (struct INSTRUCTION_I*)malloc(1 * sizeof(struct INSTRUCTION));
					INSone->NAME = (char*)malloc((Pcounter) * sizeof(char));
					memcpy(INSone->NAME, secendstr, Pcounter);
					INSone->NAME[counter] = '\0'; j = j++; numberofwords = 0;
					while (code[i][j] != '\0' && code[i][j] != '\n')
					{
						if (isdigit(code[i][j]) && Tcounter == 0)
						{
							rt[pc1] = code[i][j];
							pc1++;
						}
						else if (isdigit(code[i][j]) && Tcounter == 1)
						{
							rs[pc2] = code[i][j];
							pc2++;
						}
						else if (isdigit(code[i][j]) && Tcounter == 2)
						{
							offset[numberofwords] = code[i][j];
							numberofwords++;
						}
						else if (code[i][j] == ',')
							Tcounter++;
						else if (isalpha(code[i][j]))
						{
							offset[numberofwords] = code[i][j];
							numberofwords++;
							check = 1;
						}
						j++;
					}
					offset[numberofwords] = '\0'; rt[pc1] = '\0'; rs[pc2] = '\0';
					if (check == 1 && isalpha(offset[0]))  //islable
					{
						check = 0;
						if (strcmp(INSone->NAME, "beq") == 0) //beq
						{
							for (int k = 0; k < NumberLable; k++)
							{
								if (strcmp(ptr[k].LABLE, offset) == 0)
								{
									if (ptr[k].access == 1)
									{
										printf("THE LABLE IS USED FOR MANY TIMES\n");
										exit(1);
									}
									else
									{
										offsett = (ptr[k].ADDRESS) - i - 1;
										check = 1;
										ptr[k].access = 1;
										break;
									}
								}
							}
							rtone = atoi(rt);
							rsone = atoi(rs);
							opcode = TYPEi(INS);
							INSone->OP = opcode;
							INSone->RS = rsone;
							INSone->RT = rtone;
							INSone->OFFSET = offsett;
							SETINSTRUCTIONi(INSone, offsett, rtone, rsone, opcode);
							//printf_s("%d",INSone->ADDRESS);
							int re = GETInsInDecimal(INSone->ADDRESS);
							printf("%d", re);
							printf("\n");
							fprintf(machp, "%d\n", re);
							continue;
						}
						else
						{
							for (int r = 0; r < NumberLable; r++)
							{
								if (strcmp(ptr[r].LABLE, offset) == 0)
								{
									if (ptr[r].access == 1)
									{
										printf("THE LABLE IS USED FOR MANY TIMES\n");
										exit(1);
									}
									offsett = ptr[r].ADDRESS;
									check = 1;
									ptr[r].access = 1;
									break;
								}
							}
						}
						if (check == 0)
						{
							printf("LABLE IS NOT DEFIENED");
							exit(1);
						}
					}
					else
					{
						if (atoi(offset) > 65536)
						{
							printf("OFFSET IS BIGGER THAN 16 BITS \n");
							exit(1);
						}
						if (strcmp(INSone->NAME, "lui") == 0)  //lui
						{
							int imm = atoi(rs);
							rsone = 0;
							rtone = atoi(rt);
							opcode = TYPEi(INS);
							INSone->OP = opcode;
							INSone->RS = rsone;
							INSone->RT = rtone;
							INSone->OFFSET = offsett;
							SETINSTRUCTIONi(INSone, imm, rsone, rtone, opcode);
							int re = GETInsInDecimal(INSone->ADDRESS);
							printf("%d", re);
							printf("\n");
							continue;
						}
						else if (strcmp(INSone->NAME, "jalr") == 0)
						{
							rtone = atoi(rt);
							rsone = atoi(rs);
							opcode = TYPEi(INS);
							INSone->OP = opcode;
							INSone->RS = rsone;
							INSone->RT = rtone;
							SETINSTRUCTIONi(INSone, 0, rsone, rtone, opcode);
							int re = GETInsInDecimal(INSone->ADDRESS);
							printf("%d", re);
							printf("\n");
							fprintf(machp, "%d\n", re);
							continue;
						}
						else
							offsett = atoi(offset);
					}
					rtone = atoi(rt);
					rsone = atoi(rs);
					opcode = TYPEi(INS);
					INSone->OP = opcode;
					INSone->RS = rsone;
					INSone->RT = rtone;
					INSone->OFFSET = offsett;
					SETINSTRUCTIONi(INSone, offsett, rsone, rtone, opcode);
					//printf_s("%d",INSone->ADDRESS);
					int re = GETInsInDecimal(INSone->ADDRESS);
					printf("%d", re);
					printf("\n");
					fprintf(machp, "%d\n", re);
				}
				else if (resu == 2)
				{
					struct INSTRUCTION* INSthree = NULL; char offset[10]; int Tcount = 0, opcodee = 0, countoffset = 0, checkthree = 0;
					INSthree = (struct INSTRUCTION*)malloc(1 * sizeof(struct INSTRUCTION));
					INSthree->NAME = (char*)malloc((Pcounter) * sizeof(char));
					memcpy(INSthree->NAME, secendstr, Pcounter);
					INSthree->NAME[Pcounter] = '\0'; j = j++;
					if (strcmp(INSthree->NAME, "j") == 0)
					{
						while (code[i][j] != '\0' && code[i][j] != '\n')
						{
							if (isdigit(code[i][j]) || isalpha(code[i][j]))
							{
								offset[Tcount] = code[i][j];
								Tcount++;
							}
							j++;
						}
						offset[Tcount] = '\0';
						if (atoi(offset) > 65536)
						{
							printf("OFFSET IS BIGGER THAN 16 BITS \n");
							exit(1);
						}
						opcodee = 13;
						if (isalpha(offset[0]) && offset[0] != '-') // so it is lable 
						{
							for (int i = 0; i < NumberLable; i++)
							{
								if (strcmp(ptr[i].LABLE,offset) == 0)
								{
									countoffset = ptr[i].ADDRESS;
									checkthree = 1;
									SETINSTRUCTIONj(INSthree, countoffset, opcodee);
									int result = (GETInsInDecimal(INSthree->ADDRESS));
									printf("%d", result);
									printf("\n");
									fprintf(machp, "%d\n", result);
									ptr[i].access = 1;
									break;
								}
								else if (strcmp(offset, "halt") == 0)
								{
									countoffset = 14;
									SETINSTRUCTIONj(INSthree, countoffset, opcodee);
									int result = GETInsInDecimal(INSthree->ADDRESS);
									printf("%d", result);
									printf("\n");
									fprintf(machp, "%d\n", result);
									continue;
								}
								if (!checkthree)
								{
									printf("LABLE IS NOT DEFIENED");
									exit(1);
								}
							}
						}
						else
						{
							countoffset = atoi(offset);
							if (countoffset > 65536)
							{
								printf("OFFSET IS BIGGER THAN 16 BITS \n");
								exit(1);
							}
							SETINSTRUCTIONj(INSthree, countoffset, opcodee);
							int result = (GETInsInDecimal(INSthree->ADDRESS));
							printf("%d", result);
							printf("\n");
							fprintf(machp, "%d\n", result);
						}
					}
					else if (strcmp(INSthree->NAME, "halt") == 0)
					{
						int opcode = 14;
						for (int s = 0; s < 24; s++)
							INSthree->ADDRESS[s] = 0;
						int binop[4]; int s = 0;
						while (opcode > 0)
						{
							binop[s] = opcode % 2;
							opcode = opcode / 2;
							s++;
						}
						for (int j = s; j < 4; j++)
							binop[j] = 0;
						counter = 0;
						for (int s = 24; s < 28; s++)
						{
							INSthree->ADDRESS[s] = binop[counter];
							counter++;
						}
						for (int s = 28; s < 32; s++)
						{
							INSthree->ADDRESS[s] = 0;
						}
						int result = (GETInsInDecimal(INSthree->ADDRESS));
						printf("%d", result);
						printf("\n");
						fprintf(machp, "%d\n", result);
					}
				}
			}
		}
	}
	fclose(assp);
	fclose(machp);
	exit(0);
}