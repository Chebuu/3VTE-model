
###
# Link FAD to His114 at delta nitrogen
###

# Delete C8Me hydrogen nearest His114 Npi
deleteBond complex.546.H18 complex.546.C19
remove complex complex.546.H18

# Create His114-FAD bond Nd-C8a
bond complex.546.C19 complex.114.ND1 S


###
# Oxidize His114 epsilon carbon (E1)
###

# Delete E1 hydrogen
deleteBond complex.114.HE1 complex.114.CE1
remove complex complex.114.HE1

# Delete E2 hydrogen
deleteBond complex.114.HE2 complex.114.NE2
remove complex complex.114.HE2

# Replace E1-E2 single bond with aromatic
deleteBond complex.114.CE1 complex.114.NE2 
bond complex.114.CE1 complex.114.NE2 A

# Change resname to HID to reflect neutral charge
set complex.114 name HID
