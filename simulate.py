# name -> [0.3-1, 1-3, 3-10]
FILTERS={
  'MERV-11': [.20,  .65, .85],
  'MERV-12': [.35,  .80, .90 ],
  'MERV-13': [.50,  .85, .90],
  'MERV-14': [.75,  .90, .95],
  'MERV-15': [.85,  .90, .95],
  'MERV-16': [.95,  .95, .95],
  'HEPA':    [.9997, 1,  1],
}

VIRUS=[.20, .29, .51]

def proportion_removed(purifier_cfm, room_size_cf, filtration):
  return purifier_cfm/room_size_cf*filtration

def simulate(room_size_cf=1150,
             natural_ventilation_ach=2,
             duration=60,
             purifier_cfm=0,
             purifier_filter='MERV-14'):
  natural_ventilation_cfm = room_size_cf / 60 * natural_ventilation_ach
  
  air = [0, 0, 0]
  
  for timestep in range(duration):
    for particle_size in range(len(air)):
      # infected person exhales
      air[particle_size] += VIRUS[particle_size]
      
      # natural ventilation operates
      air[particle_size] *= 1 - proportion_removed(
        natural_ventilation_cfm, room_size_cf, 1.0)
          
      # purifier operates
      air[particle_size] *= 1 - proportion_removed(
        purifier_cfm, room_size_cf, FILTERS[purifier_filter][particle_size])

    print("%s\t%s\t%.2f" % (
      timestep,
      "\t".join("%.2f" % x for x in air),
      sum(air)))
    
if __name__ == "__main__":
  simulate()
