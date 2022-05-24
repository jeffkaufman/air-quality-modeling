import math

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

# https://www.jefftk.com/p/how-big-are-covid-particles
VIRUS=[.20, .29, .51]

# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7579175/
PARTICLE_HALF_LIVES = [
  # 0.1-1, half life ~4hr
  4*60,
  # 1-3, half life ~20min
  20,
  # 3-10, half life ~5min
  5]

PARTICLE_DECAY_RATES=[math.log(2) / half_life
                      for half_life in PARTICLE_HALF_LIVES]

def proportion_removed(purifier_cfm, room_size_cf, filtration):
  return purifier_cfm/room_size_cf*filtration

def simulate(purifier_ach=5,
             ventilation_ach=2,
             duration=60,
             purifier_filter='MERV-14',
             should_print=True):
  room_size_cf = 1000
  purifier_cfm = room_size_cf / 60 * purifier_ach
  ventilation_cfm = room_size_cf / 60 * ventilation_ach


  air = [0, 0, 0]

  totals = []

  if should_print:
    print ("\t".join([
      "timestamp", "0.3-1μm", "1-3μm", "3-10μm", "total"]))

  for timestep in range(duration):
    for particle_size in range(len(air)):
      # infected person exhales
      air[particle_size] += VIRUS[particle_size]

      # natural ventilation operates
      air[particle_size] *= 1 - proportion_removed(
        ventilation_cfm, room_size_cf, 1.0)

      # purifier operates
      air[particle_size] *= 1 - proportion_removed(
        purifier_cfm, room_size_cf, FILTERS[purifier_filter][particle_size])

      # particles settle
      air[particle_size] *= 1 - PARTICLE_DECAY_RATES[particle_size]

    if should_print:
      print("%s\t%s\t%.6f" % (
        timestep,
        "\t".join("%.6f" % x for x in air),
        sum(air)))

    totals.append(sum(air))
  return totals

def simulate_multiple():
  duration = 60
  ventilation_ach = 2

  baseline_risk = simulate(
    purifier_ach=0,
    ventilation_ach=ventilation_ach,
    duration=duration,
    purifier_filter='HEPA', # ignored
    should_print=False)

  columns = []
  rows = [["timestamp", "no purifier"]]

  for filter_name in FILTERS:
    rows[0].append(filter_name)

  for filter_name in FILTERS:
    rows[0].append(filter_name)

  for filter_name in FILTERS:
    columns.append(simulate(
      purifier_ach=5,
      ventilation_ach=ventilation_ach,
      duration=duration,
      purifier_filter=filter_name,
      should_print=False))

  for i in range(duration):
    rows.append([str(i)])

  for i in range(duration):
    rows[i+1].append("%.6f" % baseline_risk[i])

    for j in range(len(columns)):
      rows[i+1].append("%.6f" % columns[j][i])
    for j in range(len(columns)):
      rows[i+1].append("%.6f" % (columns[j][i] / baseline_risk[i]))

  for row in rows:
    print("\t".join(row))

if __name__ == "__main__":
  #simulate()
  simulate_multiple()
