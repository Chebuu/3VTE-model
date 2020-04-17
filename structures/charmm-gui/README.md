>>>>>>>>>>>>> # **CHARMM-GUI Annotations**		

 
> # PDB Reader
>				Crystal structure of tetrahydrocannabinolic acid synthase from Cannabis sativa			
> 		  
>				 			Download PDB File: 3VTE		   	    Method: X-Ray		
> 				 			Download Source:   RCSB		   	    Type:   Protein   
>
>	
>> ## [**JobID**: 8605984625](http://www.charmm-gui.org/?doc=input/pdbreader&jobid=8606142583&project=pdbreader) 
>> ### 1. Select Model/Chain	
>> - Model/Chain Selection Option
>>    - Select Model
>>        - Read all models
>>            - True
>>    - Residue ID
>>        - Protein 
>>            - SEGID = PROA / PDBID = A
>>                - First = 28
>>                - Last  = 545
>>                - Engineered Residues = None
>>        - Glycan
>>            - SEGID = CARA / PDBID = B
>>                - Engineered Residues
>>                    - bDGlcNAc(1→)PROA-65	
>>            - SEGID = CARB / PDBID = C
>>                - Engineered Residues
>>                    - bDGlcNAc(1→)PROA-89	
>>            - SEGID = CARC /  PDBID = D
>>                - Engineered Residues
>>                    - bDGlcNAc(1→)PROA-168
>>            - SEGID = CARD /  PDBID = E
>>                - Engineered Residues
>>                    - bDGlcNAc(1→)PROA-329
>>            - SEGID = CARE /  PDBID = F
>>                - Engineered Residues
>>                    - bDGlcNAc(1→)PROA-467
>>            - SEGID = CARF /  PDBID = G
>>                - Engineered Residues
>>                    - bDGlcNAc(1→)PROA-499
>>        - Hetero
>>            - SEGID = HETA / PDBID = H
>>                - Engineered Residues
>>                    - FAD
>>        - Water
>>            - SEGID = WATA / PDBID = I
>> 
>> ### 2. Manipulate PDB	
>> - PDB Manipulation Options
>>     -  Reading Hetero Chain Residues
>>         - Use CHARMM General Force Field to generate CHARMM top & par files
>>             - the SDF file from RCSB
>>     - Terminal group patching
>>         -  PROA
>>             - N-terminus = NTER
>>             - C-terminus = CTER
>>     - Model missing residues
>>         - PROA-45  : PROS-48
>>         - PROA-300 : PROS-306
>>         - PROA-360 : PROS-364
>>     - Disulfide bonds
>>         - Bond
>>             - PROA-37
>>             - PROA-99
>>     - Glycosylation / Glycan Ligand(s)
>>         - CARA
>>             - bDGlcNAc(1→)PROA-65
>>                 - n-linked
>>         - CARB
>>             - bDGlcNAc(1→)PROA-89
>>                 - n-linked
>>         - CARC
>>             - bDGlcNAc(1→)PROA-168
>>                 - n-linked
>>         - CARD
>>             - bDGlcNAc(1→)PROA-329
>>                 - n-linked
>>         - CARE
>>             - bDGlcNAc(1→)PROA-467
>>                 - n-linked
>>         - CARF
>>             - bDGlcNAc(1→)PROA-499
>>                 - n-linked
>> - **Symmetry Operation Options**
>>     - Generation of Crystal Packing
>>         - Space Group P 4 3 2
>>             - False
>>     - Generation of Full Unit Cell
>>         - Space Group P 4 3 2
>>             - False