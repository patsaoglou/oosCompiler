#include <stdio.h>
#include <stdlib.h>

typedef struct BankAccount 
{
	int balance;
	int account_number;
} BankAccount;

BankAccount* BankAccount$1$init(BankAccount *self$, int account_number)
{
	if(self$ == NULL)
	{
		self$ = (BankAccount *)malloc(sizeof(BankAccount));
	}

	self$ -> balance = 0;
	self$ -> account_number = account_number;
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

int get_account_number$1(BankAccount *self$)
{
	return self$ -> account_number;

}

typedef struct Customer 
{
	struct BankAccount *account;
	int id;
} Customer;

Customer* Customer$1$init(Customer *self$, int id, int account_number)
{
	if(self$ == NULL)
	{
		self$ = (Customer *)malloc(sizeof(Customer));
	}

	self$ -> id = id;
	self$ -> account = BankAccount$1$init(self$ -> account, account_number);
	return self$;

}

int get_customer_id$1(Customer *self$)
{
	return self$ -> id;

}

void deposit_to_account$1(Customer *self$, int amount)
{
	deposit$1(self$ -> account, amount);

}

void withdraw_from_account$1(Customer *self$, int amount)
{
	withdraw$1(self$ -> account, amount);

}

int get_account_balance$1(Customer *self$)
{
	return get_balance$1(self$ ->account);

}

typedef struct PremiumCustomer 
{
	Customer Customer$self;
	int cashback_percent;
} PremiumCustomer;

PremiumCustomer* PremiumCustomer$1$init(PremiumCustomer *self$, int id, int account_number, int cashback_percent)
{
	if(self$ == NULL)
	{
		self$ = (PremiumCustomer *)malloc(sizeof(PremiumCustomer));
	}

	self$ -> Customer$self.id = id;
	self$ -> Customer$self.account = BankAccount$1$init(self$ -> Customer$self.account, account_number);
	self$ -> cashback_percent = cashback_percent;
	return self$;

}

void withdraw_with_cashback$1(PremiumCustomer *self$, int amount)
{
	int cashback;
	withdraw$1(self$ -> Customer$self.account, amount);
	cashback = (amount * self$ -> cashback_percent) / 100;
	deposit$1(self$ -> Customer$self.account, cashback);

}

int get_cashback_percent$1(PremiumCustomer *self$)
{
	return self$ -> cashback_percent;

}

int main(void)
{
	struct Customer *regular_customer = NULL;
	struct PremiumCustomer *premium_customer = NULL;
	int deposit_amount, withdraw_amount, cashback_percent;
	regular_customer = Customer$1$init(regular_customer, 1, 101);
	deposit_amount = 200;
	withdraw_amount = 50;
	deposit_to_account$1(regular_customer, deposit_amount);
	printf("%d \n", get_account_balance$1(regular_customer));
	withdraw_from_account$1(regular_customer, withdraw_amount);
	printf("%d \n", get_account_balance$1(regular_customer));
	withdraw_from_account$1(regular_customer, 300);
	printf("%d \n", get_customer_id$1(regular_customer));
	cashback_percent = 10;
	premium_customer = PremiumCustomer$1$init(premium_customer, 2, 102, cashback_percent);
	deposit_to_account$1(&premium_customer -> Customer$self,  500);
	printf("%d \n", get_account_balance$1(&premium_customer -> Customer$self));
	withdraw_with_cashback$1(premium_customer, 100);
	printf("%d \n", get_account_balance$1(&premium_customer -> Customer$self));
	printf("%d \n", get_cashback_percent$1(premium_customer));


	return 0;
}