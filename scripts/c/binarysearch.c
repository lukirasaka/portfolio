#include <stdio.h>
#include <stdlib.h>


int BinarySearch(int arr[], int key, int size, int *steps) {
    int l = 0, p = size - 1;
    *steps = 0;

    while (l <= p) {
      (*steps)++;
      int s = (l + p) / 2;  

      if (arr[s] == key)
        return s;

      if (arr[s] > key)
        p = s - 1;

      else  
        l = s + 1;
    }
        return -1;
}

int main() {
    int size, key, steps;

    printf("Zadejte velikost pole: ");
    scanf("%d", &size);

    int arr[size];
    printf("Zadejte prvky pole: ");
    for (int i = 0; i < size; i++) {
        scanf("%d", &arr[i]);
    }
    printf("Zadejte klíč: ");
    scanf("%d", &key);
    
    int index = BinarySearch(arr, key, size, &steps);

    if (index != -1) 
        printf("Klíč byl nalezen na indexu %d, délka %d\n", index, steps);
    else
        printf("Klíč nebyl nalezen. Délka kroků %d\n", steps);

    return 0;    

}