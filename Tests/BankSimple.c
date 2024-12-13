#include <stdio.h>
#include <stdlib.h>

typedef struct BankAccount 
{
	int balance;
} BankAccount;

BankAccount* BankAccount$1$init(BankAccount *self$)
{
	if(self$ == NULL)
	{
		self$ = (BankAccount *)malloc(sizeof(BankAccount));
	}

	self$ -> balance = 0;
	return self$;

}

void deposit$1(BankAccount *self$, int amount)
{
	self$ -> balance = self$ -> balance + amount;

}

void withdraw$1(BankAccount *self$, int amount)
{

	if(self$ -> balance >= amount)
	{
		self$ -> balance = self$ -> balance - amount;

	}
	else
	{
		printf("%d \n", 0);

	}


}

int get_balance$1(BankAccount *self$)
{
	return self$ -> balance;

}

int main(void)
{
	struct BankAccount *acc1 = NULL;
	int deposit_amount, withdraw_amount, final_balance;
	acc1 = BankAccount$1$init(acc1);
	deposit_amount = 100;
	withdraw_amount = 30;
	deposit$1(acc1, deposit_amount);
	printf("%d \n", get_balance$1(acc1));
	withdraw$1(acc1, withdraw_amount);
	printf("%d \n", get_balance$1(acc1));
	withdraw$1(acc1, 200);
	final_balance = get_balance$1(acc1);

	if(final_balance > 0)
	{
		printf("%d \n", final_balance);

	}
	else
	{
		printf("%d \n", 0);

	}



	return 0;
}