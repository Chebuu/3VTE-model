## TODO:
### Add model components
- O2
- NAG
- HOOH
- Ions
- Water

### Replace hasty param hacks
- Most FAD-His torsions are contrived/wrong

### Verify hetero connections
- Bond angles for FAD C8Me hydrygens are bad

### Verify protons
- CBGA is curently potonated but need anion
- All His residues are HIE including His114 
- Protonation states need to reflect H-bonds
    - [View ligand interaction](https://www.rcsb.org/3d-view/3VTE?preset=ligandInteraction&sele=FAD)

### Verify parameters
- Correct parameters for atom types
- Correct assignment of atom types
    - H+/RES mismatches will throw

### Refine ligand coordinates
#### 
- Use a SwissDock pose for initial substrate coords
    - NOTE: SwissDock drops FAD so many poses clash
    - Any valid pose in the active site will be fine
    
### Refine protein coordinaes
- Use the [3VTE PDB-REDO](https://pdb-redo.eu/db/3vte) model



# 
## Propsed FAD-dependent Oxidative Cyclization 
Tyr484 abstracts a proton from CBGA forming an alkoxide nucleophile.        
FAD accepts a hydride to form a tertiary carbocation that arranges the ring closure.        
- Mutations at the catalytic base Tyr484 are detrimental.
- Mutations at either covalent FAD binding site His114 or Cys176 are detrimental.
- Mutations at Tyr417 and His292 attenuate catalysis but are not detrimental.

<p align='center'>
    <img alt='' src='img/benda-mech.png' width='450px'>
    <p align='center'>
        BRENDA:
        <a href='https://www.brenda-enzymes.org/enzyme.php?ecno=1.21.3.7'>
            EC 1.21.3.7
        </a>
    <p>
</p>

<p align='center'>
    <img alt='' src='img/Fig8_5-Sirikantramas2017.png' width='450px'>
    <p align='center'>
        DOI:
        <a href='https://doi.org/10.1007/978-3-319-54564-6_8'>
             10.1007/978-3-319-54564-6_8
        </a>
    <p>
</p>

<p align='center'>
    <img alt='' src='img/asite.png' width='450px'>
    <p align='center'> 
        Active-site + FAD + substrate
    </p>
</p>