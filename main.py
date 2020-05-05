import CuadraticSortingAnimation
import Heap_And_BST_BuildingAnimation
import Crossing_the_River

def main():

  while True:
    
    print("Menu:")
    print("(1) CuadraticSortingAnimation")
    print("(2) Heap-And-BST-BuildingAnimation ")
    print("(3) Crossing_the_River ")
    
    tasks = [
      CuadraticSortingAnimation.run,
      Heap_And_BST_BuildingAnimation.run,
      Crossing_the_River.run
    ]
    
    ans = input("Run number: ")
    
    while ans not in ['1', '2', '3']:
      ans = input("Run number: ")
    
    tasks[int(ans)-1]()
 

main()

