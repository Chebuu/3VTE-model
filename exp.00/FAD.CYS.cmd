# Delete Cys176 S hydrogen
deleteBond complex.176.HG complex.176.SG
remove complex complex.176.HG

# Delete FAD C6 hydrogen
deleteBond complex.546.H13 complex.546.C15
remove complex complex.546.H13

# Cys176-FAD bond S-C6
bond complex.546.C15 complex.176.SG S

