import random


sarmaye_avvalie = int(input("please enter sarmaye avvalie :"))    
hadaf = int(input("please enter hadaf :"))            
ehtemal_bord = float(input("please enter ehtemal bord : "))      
tedad_shabihsazi = int(input("please enter tedad_shabihsazi :")) 


behtarin_x = 1
kamtarin_varshakasti = 1.0

print("Shoroo-e mohasebe baraye x haye mokhtalef...\n")

for x in range(1, sarmaye_avvalie + 1):
    tedad_varshakasti = 0
    
  
    for i in range(tedad_shabihsazi):
        pool_e_feli = sarmaye_avvalie
        
       
        while pool_e_feli > 0 and pool_e_feli < hadaf:
            shans = random.random() 
            
            if shans < ehtemal_bord:
                pool_e_feli = pool_e_feli + x 
            else:
                pool_e_feli = pool_e_feli - x
        
      
        if pool_e_feli <= 0:
            tedad_varshakasti = tedad_varshakasti + 1
            
   
    ehtemal_feli = tedad_varshakasti / tedad_shabihsazi
    print(f"Meghdar x = {x} | Ehtemal Varshakasti = {ehtemal_feli:.3f}")
    
   
    if ehtemal_feli <= kamtarin_varshakasti:
        kamtarin_varshakasti = ehtemal_feli
        behtarin_x = x

print("-" * 40)
print(f"Natije Nahayi: Behtarin meghdar baraye x = {behtarin_x}")
print(f"Kamtarin ehtemal varshakasti: {kamtarin_varshakasti:.3f}")