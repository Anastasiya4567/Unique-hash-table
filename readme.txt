Task: to construct a hash table with the own hash function. The size of the table must be variable (K parameter).
If collision appears, the elements must be places under following free places in the subarray of variable size N.
The effect of the program is two-dimensional array H[K][N]. If the array has no free place, the element must be thrown away.
With the help of text generator based on real letter structure in Polish we must represent filled 2D-array. In addition,
we must analyze the time complicity of the array enumeration (display on the screen)

The program takes 3 arguments. The first two arguments are K and N. The third argument is responsible for a mode of acting.
The possible values are:
    input - read data from the standard input (or file eventually):
    2
    anna tykwa
    4
    mop ser dusza syf

    file - with the forth argument (file name)
    gen - with the forth argument (the number of words to generate)

Example executions:
    python3 main.py 1000 1000 gen 100000
    python3 main.py 1000 1000 input < example_input.txt
    python3 main.py 1000 1000 file example_tekst.txt