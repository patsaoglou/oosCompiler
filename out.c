#include <stdio.h>
#include <stdlib.h>

typedef struct Shape 
{
	int x, y;
	int color;
} Shape;

Shape* Shape$1$init(Shape *self$, int x, int y)
{
	if(self$ == NULL)
	{
		self$ = (Shape *)malloc(sizeof(Shape));
	}

	self$ -> x = x;
	self$ -> y = y;

}

Shape* Shape$2$init(Shape *self$, int x, int y, int color)
{
	if(self$ == NULL)
	{
		self$ = (Shape *)malloc(sizeof(Shape));
	}

	self$ -> x = x;
	self$ -> y = y;
	self$ -> color = color;

}

void move$1(Shape *self$, int dx, int dy)
{
	self$ -> x = self$ -> x + dx;
	self$ -> y = self$ -> y + dy;

}

void move$2(Shape *self$, int dx)
{
	self$ -> x = self$ -> x + dx;

}

void set_x$1(Shape *self$, int x)
{
	self$ -> x = x;

}

int get_x$1(Shape *self$)
{
	return self$ -> x;

}

typedef struct Circle 
{
	Shape Shape$self;
	int radius;
	int color;
} Circle;

Circle* Circle$1$init(Circle *self$, int radius)
{
	if(self$ == NULL)
	{
		self$ = (Circle *)malloc(sizeof(Circle));
	}

	self$ -> radius = radius;

}

Circle* Circle$2$init(Circle *self$, int x, int y, int color, int radius)
{
	if(self$ == NULL)
	{
		self$ = (Circle *)malloc(sizeof(Circle));
	}

	self$ -> Shape$self.x = x;
	self$ -> Shape$self.y = y;
	self$ -> color = color;
	self$ -> radius = radius;

}

int get_radius$1(Circle *self$)
{
	return self$ -> radius;

}

int area$1(Circle *self$)
{
	int int_pi;
	int_pi = 3;
	return int_pi * self$ -> radius * self$ -> radius;

}

typedef struct Square 
{
	Shape Shape$self;
	int side;
} Square;

Square* Square$1$init(Square *self$, int side)
{
	if(self$ == NULL)
	{
		self$ = (Square *)malloc(sizeof(Square));
	}

	self$ -> side = side;

}

int get_side$1(Square *self$)
{
	return self$ -> side;

}

int area$2(Square *self$)
{
	return self$ -> side * self$ -> side;

}

typedef struct SquareWithCirclesOnCorners 
{
	Square Square$self;
	Circle Circle$self;
} SquareWithCirclesOnCorners;

SquareWithCirclesOnCorners* SquareWithCirclesOnCorners$1$init(SquareWithCirclesOnCorners *self$, int side, int radius)
{
	if(self$ == NULL)
	{
		self$ = (SquareWithCirclesOnCorners *)malloc(sizeof(SquareWithCirclesOnCorners));
	}

	self$ -> Square$self.side = side;
	self$ -> Circle$self.radius = radius;

}

int area$3(SquareWithCirclesOnCorners *self$)
{
	int int_pi;
	int_pi = 3;
	return get_side$1(&self$ -> Square$self) * get_side$1(&self$ -> Square$self) + 3 * int_pi * get_radius$1(&self$ -> Circle$self) * get_radius$1(&self$ -> Circle$self);

}

typedef struct SquareWithCirclesOnCorners2 
{
	struct Square *s;
	struct Circle *c;
} SquareWithCirclesOnCorners2;

SquareWithCirclesOnCorners2* SquareWithCirclesOnCorners2$1$init(SquareWithCirclesOnCorners2 *self$, int side, int radius)
{
	if(self$ == NULL)
	{
		self$ = (SquareWithCirclesOnCorners2 *)malloc(sizeof(SquareWithCirclesOnCorners2));
	}

	self$ -> s = Square$1$init(self$ -> s, side);
	self$ -> c = Circle$1$init(self$ -> c, radius);

}

int area$4(SquareWithCirclesOnCorners2 *self$)
{
	int int_pi_part;
	int_pi_part = 3;
	return get_side$1(self$ ->s) * get_side$1(self$ ->s) + 3 * int_pi_part * get_radius$1(self$ ->c) * get_radius$1(self$ ->c);

}

int main(void)
{
	struct Circle *c = NULL;
	struct Square *s = NULL;
	struct SquareWithCirclesOnCorners *s1 = NULL;
	struct SquareWithCirclesOnCorners2 *s2 = NULL;
	c = Circle$1$init(c, 4);
	printf("%d \n", area$1(c));
	s = Square$1$init(s, 4);
	printf("%d \n", area$2(s));
	s1 = SquareWithCirclesOnCorners$1$init(s1, 3, 5);
	s2 = SquareWithCirclesOnCorners2$1$init(s2, 3, 5);
	printf("%d \n", area$3(s1));
	printf("%d \n", area$4(s2));


	return 0;
}