#include <stdio.h>
#include <stdlib.h>

typedef struct Complex 
{
	int real, img;
} Complex;

Complex* Complex$1$init(Complex *self$)
{
	if(self$ == NULL)
	{
		self$ = (Complex *)malloc(sizeof(Complex));
	}

	self$ -> real = 0;
	self$ -> img = 0;
	return self$;

}

Complex* Complex$2$init(Complex *self$, int real, int img)
{
	if(self$ == NULL)
	{
		self$ = (Complex *)malloc(sizeof(Complex));
	}

	self$ -> real = real;
	self$ -> img = img;
	return self$;

}

void set_real$1(Complex *self$, int real)
{
	self$ -> real = real;

}

void set_img$1(Complex *self$, int img)
{
	self$ -> img = img;

}

Complex* get_complex$1(Complex *self$)
{
	return self$;

}

void set_complex$1(Complex *self$, int real, int img)
{
	self$ -> real = real;
	self$ -> img = img;

}

int get_real$1(Complex *self$)
{
	return self$ -> real;

}

int get_img$1(Complex *self$)
{
	return self$ -> img;

}

int squared_modulus$1(Complex *self$)
{
	return self$ -> real * self$ -> real + self$ -> img * self$ -> img;

}

void add$1(Complex *self$, Complex *c1, Complex *c2)
{
	self$ -> real = c1 -> real + c2 -> real;
	self$ -> img = c1 -> img + c2 -> img;

}

void print_complex$1(Complex *self$)
{
	printf("%d %d \n", self$ -> real, self$ -> img);

}

int main(void)
{
	struct Complex *c1 = NULL, *c2 = NULL, *c3 = NULL;
	c1 = Complex$2$init(c1, 1, 2);
	c2 = Complex$2$init(c2, 3, 4);
	c3 = Complex$1$init(c3);
	print_complex$1(c1);
	print_complex$1(c2);
	add$1(c3, c1, c2);
	print_complex$1(c3);
	set_real$1(c3, squared_modulus$1(c1));
	set_img$1(c3, squared_modulus$1(c2));
	print_complex$1(c3);


	return 0;
}