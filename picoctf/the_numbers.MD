**The Numbers** | Danny

We are given one file, `the_numbers.png`:
![Image](https://i.imgur.com/pV99qbe.png)

First, let's analyze the file-type using `file flag`. 

The first thing I notice are the brackets `{}` shown in the image. Counting the numbers before the first bracket, `16 9 3 15 3 20 6`, which is a set of 7. That is the same number of characters in `picoCTF`, so I am assumning the numbers represent a letter. 

With this, it isn't hard to notice that it is an A1Z26 cipher, with 16 representing P, 9 representing I, 3 representing C, and so on. So, we can simply decode the set of numbers using the A1Z26 cipher, and we get a flag of `picoCTF{THENUMBERSMASON}`. 
