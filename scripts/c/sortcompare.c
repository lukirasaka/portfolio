#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define LIMIT 100000

void swap(int* a, int* b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

void make_arr(int* parr)
{
    for (long long int i = 0; i < LIMIT; i++)
    {
        *(parr + i) = (rand() % LIMIT);
    }
}

long long int insertion_sort_with_counting(int pole[], long long int velikost, int poradi)
{
    long long int count = 0;
    for (long long int i = 1; i < velikost; i++)
    {
        int key = pole[i];
        long long int j = i - 1;
        while (j >= 0)
        {
            count++;
            if ((poradi < 0) ? (pole[j] < key) : (pole[j] > key))
            {
                pole[j + 1] = pole[j];
                j--;
            }
            else
            {
                break;
            }
        }
        pole[j + 1] = key;
    }
    return count;
}


void merge(int pole[], long long int left, long long int mid, long long int right, long long int* count, int poradi)
{
    long long int n1 = mid - left + 1;
    long long int n2 = right - mid;
    int* L = (int*)malloc(n1 * sizeof(int));
    int* R = (int*)malloc(n2 * sizeof(int));

    for (long long int i = 0; i < n1; i++)
        L[i] = pole[left + i];
    for (long long int j = 0; j < n2; j++)
        R[j] = pole[mid + 1 + j];

    long long int i = 0, j = 0, k = left;
    while (i < n1 && j < n2)
    {
        if ((poradi < 0) ? (L[i] > R[j]) : (L[i] <= R[j]))
        {
            pole[k] = L[i];
            i++;
        }
        else
        {
            pole[k] = R[j];
            j++;
        }
        (*count)++;
        k++;
    }

    while (i < n1)
    {
        pole[k] = L[i];
        i++;
        k++;
    }
    while (j < n2)
    {
        pole[k] = R[j];
        j++;
        k++;
    }

    free(L);
    free(R);
}

void merge_sort_with_counting(int pole[], long long int left, long long int right, long long int* count, int poradi)
{
    if (left < right)
    {
        long long int mid = left + (right - left) / 2;
        merge_sort_with_counting(pole, left, mid, count, poradi);
        merge_sort_with_counting(pole, mid + 1, right, count, poradi);
        merge(pole, left, mid, right, count, poradi);
    }
}

long long int merge_sort(int pole[], long long int velikost, int poradi)
{
    long long int count = 0;
    merge_sort_with_counting(pole, 0, velikost - 1, &count, poradi);
    return count;
}

void merge_insertion_sort(int pole[], long long int left, long long int right, long long int mezni_velikost, long long int* count, int poradi)
{
    if (right - left + 1 <= mezni_velikost)
    {
        for (long long int i = left + 1; i <= right; i++)
        {
            int key = pole[i];
            long long int j = i - 1;
            while (j >= left && ((poradi < 0) ? (pole[j] < key) : (pole[j] > key)))
            {
                pole[j + 1] = pole[j];
                (*count)++;
                j--;
            }
            pole[j + 1] = key;
        }
    }
    else
    {
        long long int mid = left + (right - left) / 2;
        merge_insertion_sort(pole, left, mid, mezni_velikost, count, poradi);
        merge_insertion_sort(pole, mid + 1, right, mezni_velikost, count, poradi);
        merge(pole, left, mid, right, count, poradi);
    }
}

long long int merge_insertion_sort_count(int pole[], long long int velikost, long long int mezni_velikost, int poradi)
{
    long long int count = 0;
    merge_insertion_sort(pole, 0, velikost - 1, mezni_velikost, &count, poradi);
    return count;
}

int main()
{
    srand((unsigned)time(NULL));

    int* arr = (int*)malloc(LIMIT * sizeof(int));
    int* arr1 = (int*)malloc(LIMIT * sizeof(int));
    int* arr2 = (int*)malloc(LIMIT * sizeof(int));
    long long int mezni_velikost = 50; //Zaměnitelná, 32-64 by měla být optimální 
    int poradi = 1; 

    make_arr(arr);
    for (long long int i = 0; i < LIMIT; i++)
    {
        arr1[i] = arr[i];
        arr2[i] = arr[i];
    }

    printf("Insertion Sort:\n");
    long long int count_insertion = insertion_sort_with_counting(arr, LIMIT, poradi);
    printf("Pocet porovnani: %lld\n", count_insertion);

    printf("\nMerge Sort:\n");
    long long int count_merge = merge_sort(arr1, LIMIT, poradi);
    printf("Pocet porovnani: %lld\n", count_merge);

    printf("\nMerge-Insertion Sort (mezni_velikost = %lld):\n", mezni_velikost);
    long long int count_merge_insertion = merge_insertion_sort_count(arr2, LIMIT, mezni_velikost, poradi);
    printf("Pocet porovnani: %lld\n", count_merge_insertion);

    free(arr);
    free(arr1);
    free(arr2);

    return 0;
}
