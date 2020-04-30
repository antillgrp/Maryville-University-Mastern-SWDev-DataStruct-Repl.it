import CuadraticSortingAnimation
import Heap_And_BST_BuildingAnimation

def main():

  while True:
    
    print("Menu:")
    print("(1) CuadraticSortingAnimation")
    print("(2) Heap-And-BST-BuildingAnimation ")
    
    tasks = [
      CuadraticSortingAnimation.run,
      Heap_And_BST_BuildingAnimation.run
    ]
    
    ans = input("Run number: ")
    
    while ans not in ['1', '2']:
      ans = input("Run number: ")
    
    tasks[int(ans)-1]()
 

main()

