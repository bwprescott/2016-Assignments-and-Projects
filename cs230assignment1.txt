#include <stdio.h>
//do not add any other library

int network_order(void) {
  // return value:
  // 0: little endian 
  // 1: big endian (also network order)
  // do not modify.
  unsigned int i = 459521;
  unsigned char * pi = (unsigned char *) &i;
  if (*pi == 0){
    return 1;
  }else{
    return 0;
  }
}

unsigned int htonl (unsigned int h){
  //your code
  // print: whether the local host is little endian or big endian
  // if the local host is little endian, convert the input h to network order
  if (network_order() == 1){
    printf("The host is big endian \n");
    return h;
  }else{
    printf("The host is little endian \n");
    unsigned int k;
    unsigned char * pc = (unsigned char *)&h;
    unsigned char * pd = (unsigned char *)&k;
    *(pd+3) = *pc;
    *(pd+2) = *(pc+1);
    *(pd+1) = *(pc+2);
    *(pd) = *(pc+3);
    return k;
    
    
  }
  
}

void byte_to_binary(unsigned char c, unsigned char * byte){
  //your code
  //store the binary representation of c as a string in the memory space pointed to by the pointer "byte"
  //note: the memory space contains exactly 8 bytes, so do not add  '\0' at the end.
  for(unsigned int i = 0; i<8;i++){
   if(c>>(8-i-1) &1 == 1){
    byte[i] = '1';
   }else{
    byte[i] = '0';
   }
  }
}

void dtobl (unsigned int d, unsigned char * b){
  //your code
  //store the binary representaiton of d as a string in the memory space pointed to by the pointer "b"
  //note: the momory space contains exactly 32 bytes, so do not add '\0' at the end.
  for(unsigned int i = 0; i<32;i++){
   if(((d>>(32-i-1))&1) == 1){
    b[i] = '1';
   }else{
    b[i] = '0';
   }
  }
}

int main() {
  //do not modify when you submit
  
  //you should try different i values to test out your code before submission;
  //but when you actually submit it, do not modify anything in main().
  unsigned int i = 459532;
  unsigned char b[33];

  //ensures the entires string is properly ended.
  //no need to insert '\0' in the dtobl() or byte_to_binary() functions above
  b[32] = 0;

  dtobl(i, b);

  //%s tells the printf() to print out a string
  //your program should print the following:
  //host order:     00001100000000110000011100000000
  printf("host order:\t%s\n", b);

  unsigned int j = htonl(i);

  dtobl(j, b);

  //your program should print the following:
  //network order:  00000000000001110000001100001100
  printf("network order:\t%s\n",b); 

  return 0;
}