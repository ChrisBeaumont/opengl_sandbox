%.o: %.c
	gcc -c -g -Wall -I/opt/local/include -I/System/Library/Frameworks/GLUT.framework/Headers -o $@ $^

mirror: mirror.o
	gcc -framework GLUT -framework OpenGL -framework Carbon $^ -o mirror
