#define MAXLEN  200
int Codeline = 0, NumberLable = 0;
char code[MAXLEN][MAXLEN];
int addresslable[10], counter = 0;
const char* INSTRUCTIONS[] = { "add", "sub", "slt", "or", "nand","addi", "ori", "slti", "lui", "lw", "sw", "beq", "jalr", "j", "halt" };
struct SymbolTable
{
	char LABLE[7];
	int ADDRESS;
	int access;
};
struct INSTRUCTION
{
	char* NAME;
	int OP;
	int RT;
	int RS;
	int OFFSET;
	int RD;
	int ADDRESS[32];
};
